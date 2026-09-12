"""Content bundle registry — register-once by bundle_hash (immutable rows).

Offline-capable SQLite / Memory mirror the Postgres logical model from
`02-content-packaging.md` §4. Production ``DATABASE_URL=postgresql://…`` uses
:class:`PostgresBundleRegistry` (psycopg).
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

from aibridge.content import LoadedContentBundle


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class ContentBundleRow:
    bundle_hash: str
    source_commit: str
    bundle_version: str
    instructions_hash: str
    wire_oas_hash: str
    pack_hash: str
    tool_schema_hash: str
    verified_at: datetime
    components_json: str


class BundleRegistry(Protocol):
    def get(self, bundle_hash: str) -> ContentBundleRow | None: ...

    def register_once(self, loaded: LoadedContentBundle) -> ContentBundleRow: ...

    def list_hashes(self) -> list[str]: ...

    def delete(self, bundle_hash: str) -> bool: ...

    def close(self) -> None: ...


class MemoryBundleRegistry:
    """In-process registry for unit tests."""

    def __init__(self) -> None:
        self._rows: dict[str, ContentBundleRow] = {}

    def get(self, bundle_hash: str) -> ContentBundleRow | None:
        return self._rows.get(bundle_hash)

    def register_once(self, loaded: LoadedContentBundle) -> ContentBundleRow:
        existing = self._rows.get(loaded.bundle_hash)
        if existing is not None:
            return existing
        row = ContentBundleRow(
            bundle_hash=loaded.bundle_hash,
            source_commit=loaded.source_commit,
            bundle_version=loaded.bundle_version,
            instructions_hash=loaded.instructions_hash,
            wire_oas_hash=loaded.wire_oas_hash,
            pack_hash=loaded.pack_hash,
            tool_schema_hash=loaded.tool_schema_hash,
            verified_at=_utc_now(),
            components_json=json.dumps(loaded.components, sort_keys=True),
        )
        self._rows[loaded.bundle_hash] = row
        return row

    def list_hashes(self) -> list[str]:
        return list(self._rows.keys())

    def delete(self, bundle_hash: str) -> bool:
        return self._rows.pop(bundle_hash, None) is not None

    def close(self) -> None:
        return None


_SCHEMA = """
CREATE TABLE IF NOT EXISTS content_bundle (
  bundle_hash TEXT PRIMARY KEY,
  source_commit TEXT NOT NULL,
  bundle_version TEXT NOT NULL,
  instructions_hash TEXT NOT NULL,
  wire_oas_hash TEXT NOT NULL,
  pack_hash TEXT NOT NULL,
  tool_schema_hash TEXT NOT NULL,
  verified_at TEXT NOT NULL,
  components_json TEXT NOT NULL
);
"""

_PG_SCHEMA = """
CREATE TABLE IF NOT EXISTS content_bundle (
  bundle_hash TEXT PRIMARY KEY,
  source_commit TEXT NOT NULL,
  bundle_version TEXT NOT NULL,
  instructions_hash TEXT NOT NULL,
  wire_oas_hash TEXT NOT NULL,
  pack_hash TEXT NOT NULL,
  tool_schema_hash TEXT NOT NULL,
  verified_at TIMESTAMPTZ NOT NULL,
  components_json TEXT NOT NULL
);
"""


class SqliteBundleRegistry:
    """SQLite-backed register-once store (offline CI / local)."""

    def __init__(self, path: str | Path) -> None:
        self._path = str(path)
        self._conn = sqlite3.connect(self._path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(_SCHEMA)
        self._conn.commit()

    def get(self, bundle_hash: str) -> ContentBundleRow | None:
        cur = self._conn.execute(
            "SELECT * FROM content_bundle WHERE bundle_hash = ?",
            (bundle_hash,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return self._from_row(row)

    def register_once(self, loaded: LoadedContentBundle) -> ContentBundleRow:
        existing = self.get(loaded.bundle_hash)
        if existing is not None:
            return existing
        verified = _utc_now().isoformat()
        components_json = json.dumps(loaded.components, sort_keys=True)
        try:
            self._conn.execute(
                """
                INSERT INTO content_bundle (
                  bundle_hash, source_commit, bundle_version,
                  instructions_hash, wire_oas_hash, pack_hash, tool_schema_hash,
                  verified_at, components_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    loaded.bundle_hash,
                    loaded.source_commit,
                    loaded.bundle_version,
                    loaded.instructions_hash,
                    loaded.wire_oas_hash,
                    loaded.pack_hash,
                    loaded.tool_schema_hash,
                    verified,
                    components_json,
                ),
            )
            self._conn.commit()
        except sqlite3.IntegrityError:
            existing = self.get(loaded.bundle_hash)
            if existing is None:
                raise
            return existing
        row = self.get(loaded.bundle_hash)
        assert row is not None
        return row

    def list_hashes(self) -> list[str]:
        cur = self._conn.execute("SELECT bundle_hash FROM content_bundle")
        return [str(r[0]) for r in cur.fetchall()]

    def delete(self, bundle_hash: str) -> bool:
        cur = self._conn.execute(
            "DELETE FROM content_bundle WHERE bundle_hash = ?",
            (bundle_hash,),
        )
        self._conn.commit()
        return cur.rowcount > 0

    def close(self) -> None:
        self._conn.close()

    @staticmethod
    def _from_row(row: sqlite3.Row) -> ContentBundleRow:
        return ContentBundleRow(
            bundle_hash=str(row["bundle_hash"]),
            source_commit=str(row["source_commit"]),
            bundle_version=str(row["bundle_version"]),
            instructions_hash=str(row["instructions_hash"]),
            wire_oas_hash=str(row["wire_oas_hash"]),
            pack_hash=str(row["pack_hash"]),
            tool_schema_hash=str(row["tool_schema_hash"]),
            verified_at=datetime.fromisoformat(str(row["verified_at"])),
            components_json=str(row["components_json"]),
        )


def _require_psycopg() -> Any:
    try:
        import psycopg
        from psycopg import errors as pg_errors
    except ImportError as exc:  # pragma: no cover - exercised when dep missing
        raise ImportError(
            "psycopg is required for postgresql:// DATABASE_URL; "
            "pip install 'doge-ai-bridge[postgres]' or install psycopg"
        ) from exc
    return psycopg, pg_errors


class PostgresBundleRegistry:
    """PostgreSQL register-once store (production / multi-instance)."""

    def __init__(self, database_url: str, *, conn: Any | None = None) -> None:
        psycopg, _pg_errors = _require_psycopg()
        self._pg_errors = _pg_errors
        self._url = database_url
        self._conn = conn if conn is not None else psycopg.connect(database_url)
        self._conn.execute(_PG_SCHEMA)
        self._conn.commit()

    def get(self, bundle_hash: str) -> ContentBundleRow | None:
        row = self._conn.execute(
            "SELECT * FROM content_bundle WHERE bundle_hash = %s",
            (bundle_hash,),
        ).fetchone()
        if row is None:
            return None
        return self._from_row(row)

    def register_once(self, loaded: LoadedContentBundle) -> ContentBundleRow:
        existing = self.get(loaded.bundle_hash)
        if existing is not None:
            return existing
        verified = _utc_now()
        components_json = json.dumps(loaded.components, sort_keys=True)
        try:
            self._conn.execute(
                """
                INSERT INTO content_bundle (
                  bundle_hash, source_commit, bundle_version,
                  instructions_hash, wire_oas_hash, pack_hash, tool_schema_hash,
                  verified_at, components_json
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    loaded.bundle_hash,
                    loaded.source_commit,
                    loaded.bundle_version,
                    loaded.instructions_hash,
                    loaded.wire_oas_hash,
                    loaded.pack_hash,
                    loaded.tool_schema_hash,
                    verified,
                    components_json,
                ),
            )
            self._conn.commit()
        except self._pg_errors.UniqueViolation:
            self._conn.rollback()
            existing = self.get(loaded.bundle_hash)
            if existing is None:
                raise
            return existing
        row = self.get(loaded.bundle_hash)
        assert row is not None
        return row

    def list_hashes(self) -> list[str]:
        rows = self._conn.execute("SELECT bundle_hash FROM content_bundle").fetchall()
        return [str(r[0]) for r in rows]

    def delete(self, bundle_hash: str) -> bool:
        cur = self._conn.execute(
            "DELETE FROM content_bundle WHERE bundle_hash = %s",
            (bundle_hash,),
        )
        self._conn.commit()
        return cur.rowcount > 0

    def close(self) -> None:
        self._conn.close()

    @staticmethod
    def _from_row(row: Any) -> ContentBundleRow:
        # psycopg Row supports index + mapping access
        verified = row["verified_at"]
        if isinstance(verified, datetime):
            verified_at = verified
        else:
            verified_at = datetime.fromisoformat(str(verified))
        return ContentBundleRow(
            bundle_hash=str(row["bundle_hash"]),
            source_commit=str(row["source_commit"]),
            bundle_version=str(row["bundle_version"]),
            instructions_hash=str(row["instructions_hash"]),
            wire_oas_hash=str(row["wire_oas_hash"]),
            pack_hash=str(row["pack_hash"]),
            tool_schema_hash=str(row["tool_schema_hash"]),
            verified_at=verified_at,
            components_json=str(row["components_json"]),
        )


def open_bundle_registry(database_url: str) -> BundleRegistry:
    """Open registry from DATABASE_URL.

    - empty / ``memory`` / ``:memory:`` → MemoryBundleRegistry
    - ``sqlite:`` / ``sqlite://`` → SqliteBundleRegistry
    - ``postgresql://`` / ``postgres://`` → PostgresBundleRegistry (psycopg)
    """
    url = (database_url or "").strip()
    if not url or url in {":memory:", "memory"}:
        return MemoryBundleRegistry()
    if url.startswith("sqlite:///"):
        path = url.removeprefix("sqlite:///")
        return SqliteBundleRegistry(path)
    if url.startswith("sqlite://"):
        path = url.removeprefix("sqlite://")
        if path in {"", ":memory:"}:
            return SqliteBundleRegistry(":memory:")
        return SqliteBundleRegistry(path)
    if url.startswith("postgresql://") or url.startswith("postgres://"):
        return PostgresBundleRegistry(url)
    return SqliteBundleRegistry(url)
