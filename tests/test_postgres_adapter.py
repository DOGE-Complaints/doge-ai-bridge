"""t07 — Postgres BundleRegistry / SessionStore adapter (offline-mocked + optional live)."""

from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from aibridge.content import load_content_bundle
from aibridge.registry import (
    PostgresBundleRegistry,
    open_bundle_registry,
)
from aibridge.sessions import PostgresSessionStore, open_session_store

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "content"
WIRE_OAS = (
    Path(__file__).resolve().parents[1]
    / "docs"
    / "openapi"
    / "story-intake-actions.openapi.yaml"
)


def _loaded():
    return load_content_bundle(
        instructions_dir=FIXTURES / "instructions",
        manifest_path=FIXTURES / "instructions.manifest.json",
        source_commit="pg-adapter-commit",
        wire_oas_path=WIRE_OAS,
        pack_schema_path=FIXTURES / "pack" / "payload.schema.json",
    )


class _FakeResult:
    def __init__(self, row: Any = None, rows: list[Any] | None = None, rowcount: int = 0):
        self._row = row
        self._rows = rows or ([] if row is None else [row])
        self.rowcount = rowcount

    def fetchone(self) -> Any:
        return self._row

    def fetchall(self) -> list[Any]:
        return list(self._rows)


class _FakePgConn:
    """Minimal stand-in for psycopg Connection used by Postgres adapters."""

    def __init__(self) -> None:
        self.bundles: dict[str, dict[str, Any]] = {}
        self.sessions: dict[str, dict[str, Any]] = {}
        self.closed = False

    def execute(self, sql: str, params: tuple[Any, ...] | None = None) -> _FakeResult:
        q = " ".join(sql.split()).lower()
        params = params or ()
        if q.startswith("create table"):
            return _FakeResult()
        if "from content_bundle where bundle_hash" in q and q.startswith("select"):
            row = self.bundles.get(params[0])
            return _FakeResult(row=row)
        if q.startswith("insert into content_bundle"):
            (
                bundle_hash,
                source_commit,
                bundle_version,
                instructions_hash,
                wire_oas_hash,
                pack_hash,
                tool_schema_hash,
                verified_at,
                components_json,
            ) = params
            if bundle_hash in self.bundles:
                from psycopg import errors as pg_errors

                raise pg_errors.UniqueViolation("duplicate bundle_hash")
            self.bundles[bundle_hash] = {
                "bundle_hash": bundle_hash,
                "source_commit": source_commit,
                "bundle_version": bundle_version,
                "instructions_hash": instructions_hash,
                "wire_oas_hash": wire_oas_hash,
                "pack_hash": pack_hash,
                "tool_schema_hash": tool_schema_hash,
                "verified_at": verified_at,
                "components_json": components_json,
            }
            return _FakeResult(rowcount=1)
        if q.startswith("select bundle_hash from content_bundle"):
            rows = [(h,) for h in self.bundles]
            return _FakeResult(rows=rows)
        if q.startswith("delete from content_bundle"):
            existed = params[0] in self.bundles
            self.bundles.pop(params[0], None)
            return _FakeResult(rowcount=1 if existed else 0)
        if "from session where session_id" in q and q.startswith("select"):
            row = self.sessions.get(params[0])
            return _FakeResult(row=row)
        if q.startswith("insert into session"):
            # VALUES (%s, %s, %s, TRUE, %s, %s) → 5 bind params
            session_id, content_bundle_hash, deployment_id, created, updated = params
            self.sessions[session_id] = {
                "session_id": session_id,
                "content_bundle_hash": content_bundle_hash,
                "deployment_id": deployment_id,
                "active": True,
                "created_at": created,
                "updated_at": updated,
            }
            return _FakeResult(rowcount=1)
        if "from session where active" in q:
            rows = [
                (s["content_bundle_hash"],)
                for s in self.sessions.values()
                if s["active"]
            ]
            return _FakeResult(rows=rows)
        if q.startswith("update session set active"):
            sid = params[1]
            if sid in self.sessions:
                self.sessions[sid]["active"] = False
                self.sessions[sid]["updated_at"] = params[0]
            return _FakeResult(rowcount=1)
        raise AssertionError(f"unexpected SQL: {sql!r} params={params!r}")

    def commit(self) -> None:
        return None

    def rollback(self) -> None:
        return None

    def close(self) -> None:
        self.closed = True


def test_open_bundle_registry_postgres_url_uses_adapter(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = _FakePgConn()
    monkeypatch.setattr(
        "psycopg.connect",
        lambda *_a, **_k: fake,
    )
    reg = open_bundle_registry(
        "postgresql://u:p@localhost:5432/aibridge", ensure_schema=True
    )
    assert isinstance(reg, PostgresBundleRegistry)
    loaded = _loaded()
    first = reg.register_once(loaded)
    second = reg.register_once(loaded)
    assert first.bundle_hash == second.bundle_hash == loaded.bundle_hash
    assert first.verified_at == second.verified_at
    assert reg.get(loaded.bundle_hash) is not None
    reg.close()
    assert fake.closed


def test_open_session_store_postgres_pin_resume(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = _FakePgConn()
    monkeypatch.setattr("psycopg.connect", lambda *_a, **_k: fake)
    reg = PostgresBundleRegistry("postgresql://u:p@localhost/db", conn=fake, ensure_schema=True)
    sessions = PostgresSessionStore("postgresql://u:p@localhost/db", conn=fake, ensure_schema=True)
    loaded = _loaded()
    row = reg.register_once(loaded)
    sessions.create(
        session_id="s-pg",
        content_bundle_hash=row.bundle_hash,
        deployment_id="dep-1",
    )
    resumed = sessions.resume_bundle("s-pg", reg)
    assert resumed.bundle_hash == row.bundle_hash
    assert sessions.active_bundle_hashes() == {row.bundle_hash}


def test_open_helpers_route_postgres_scheme(monkeypatch: pytest.MonkeyPatch) -> None:
    fake = _FakePgConn()
    monkeypatch.setattr("psycopg.connect", lambda *_a, **_k: fake)
    assert isinstance(
        open_bundle_registry("postgres://u:p@h/db", ensure_schema=True),
        PostgresBundleRegistry,
    )
    assert isinstance(
        open_session_store("postgres://u:p@h/db", ensure_schema=True),
        PostgresSessionStore,
    )


@pytest.mark.postgres
def test_live_postgres_register_once_if_configured() -> None:
    """Optional live DB — skip when DATABASE_URL is not postgresql://."""
    url = (os.environ.get("DATABASE_URL") or "").strip()
    if not (url.startswith("postgresql://") or url.startswith("postgres://")):
        pytest.skip("DATABASE_URL postgresql:// not set — no live PG in CI")
    reg = open_bundle_registry(url)
    sessions = open_session_store(url)
    try:
        loaded = _loaded()
        row = reg.register_once(loaded)
        assert reg.get(row.bundle_hash) is not None
        sessions.create(
            session_id=f"live-{row.bundle_hash[:8]}",
            content_bundle_hash=row.bundle_hash,
            deployment_id="live-test",
        )
        assert row.bundle_hash in sessions.active_bundle_hashes()
    finally:
        sessions.close()
        reg.close()
