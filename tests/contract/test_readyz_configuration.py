"""STORY-AIBRIDGE-33 — READY-001…015 /readyz configuration contract tests.

Fixture-driven Settings overrides. Bounded reasons from readiness.py.
No live Telegram / Railway invent. Preference A fake-PG for READY-013.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import ConfirmationGuard, reset_confirmation_guard
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import GatewayExecutor, RecordingGatewayTransport
from aibridge.interview import default_recording_engine
from aibridge.migrate import list_migration_files
from aibridge.readiness import evaluate_readiness
from aibridge.registry import MemoryBundleRegistry
from aibridge.sessions import MemorySessionStore

_TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))
from fixture_loader import load_fixture  # noqa: E402

STORY = "STORY-AIBRIDGE-33-qa-readiness-configuration"
READY_IDS = {f"READY-{i:03d}" for i in range(1, 16)}
PKG_FIXTURES = (
    _TESTS_ROOT.parents[0]
    / "docs"
    / "tasks"
    / "backlog-stories"
    / "qa-inbound-outbound-data-flow"
    / "fixtures"
)
REPO = _TESTS_ROOT.parents[0]

FIXTURE_NAMES = [
    "ready-ok",
    "ready-ok-migrated-pg",
    "ready-missing-channel-bearer",
    "ready-missing-gateway-bearer",
    "ready-bearers-equal",
    "ready-intake-not-https",
    "ready-intake-missing",
    "ready-redirect-invalid",
    "ready-openai-missing",
    "ready-openai-store-true",
    "ready-dry-run-required",
    "ready-content-bundle-not-ready",
    "ready-tool-gen-failed",
    "ready-database-unreachable",
    "ready-migration-mismatch",
    "ready-migration-version-missing",
    "ready-migrations-missing",
    "ready-database-not-postgres",
    "ready-no-side-effects",
]


def _hash(path: Path) -> bytes:
    return hashlib.sha256(path.read_bytes()).digest()


def _resolve_path(value: object) -> object:
    if isinstance(value, str) and (
        value.startswith("tests/")
        or value.startswith("docs/")
        or value.startswith("src/")
    ):
        return str(REPO / value)
    return value


def _settings_from_overrides(overrides: dict[str, Any]) -> Settings:
    reset_settings_cache()
    resolved = {k: _resolve_path(v) for k, v in overrides.items()}
    return Settings(_env_file=None, **resolved)


def _memory_app(
    settings: Settings,
    *,
    interview_engine: Any | None = None,
    confirmation_guard: ConfirmationGuard | None = None,
) -> Any:
    """create_app with memory stores injected (skips PG apply_migrations on boot)."""
    engine = interview_engine or default_recording_engine()
    # When DATABASE_URL is postgres + memory forbidden, create_app would call
    # apply_migrations unless confirmation_guard (and dedupe) are injected.
    guard = confirmation_guard
    if guard is None:
        guard = reset_confirmation_guard(
            ConfirmationGuard(interview_engine=engine)
        )
    return create_app(
        settings=settings,
        dedupe_store=EventDedupeStore(),
        bundle_registry=MemoryBundleRegistry(),
        session_store=MemorySessionStore(),
        interview_engine=engine,
        confirmation_guard=guard,
    )


class _FakeMigResult:
    def __init__(self, rows: list[tuple[str]]) -> None:
        self._rows = rows

    def fetchall(self) -> list[tuple[str]]:
        return list(self._rows)


class _FakeMigConn:
    """Preference A — SELECT schema_migrations (stale / ok / empty / raise)."""

    def __init__(
        self,
        version: str | None = "0000_stale",
        *,
        empty: bool = False,
        raise_on_select: bool = False,
    ) -> None:
        self._version = version
        self._empty = empty
        self._raise_on_select = raise_on_select

    def execute(self, sql: str, params: Any = None) -> _FakeMigResult:
        if "schema_migrations" in sql:
            if self._raise_on_select:
                raise RuntimeError("schema_migrations unavailable")
            if self._empty:
                return _FakeMigResult([])
            assert self._version is not None
            return _FakeMigResult([(self._version,)])
        return _FakeMigResult([])

    def close(self) -> None:
        return None


def test_traceability_ready_ids_via_fixtures() -> None:
    seen: set[str] = set()
    for name in FIXTURE_NAMES:
        env = load_fixture("settings", name)
        assert STORY in env["story_keys"]
        assert env["cluster"] == "settings"
        assert env["schema_version"] == "1.0"
        seen.update(i for i in env["matrix_ids"] if i.startswith("READY-"))
    assert READY_IDS == seen


def test_package_originals_hash_eq_copies() -> None:
    for name in FIXTURE_NAMES:
        pkg = PKG_FIXTURES / f"{name}.json"
        copy = _TESTS_ROOT / "fixtures" / "settings" / f"{name}.json"
        assert pkg.is_file(), f"missing package original {pkg}"
        assert copy.is_file(), f"missing promoted copy {copy}"
        assert _hash(pkg) == _hash(copy)


def test_ready_001_complete_config_ready() -> None:
    env = load_fixture("settings", "ready-ok")
    assert "READY-001" in env["matrix_ids"]
    settings = _settings_from_overrides(env["payload"]["overrides"])
    client = TestClient(_memory_app(settings))
    response = client.get("/readyz")
    expect = env["payload"]["expect_readyz"]
    assert response.status_code == expect["http_status"]
    assert response.json()["status"] == expect["status"]


def test_ready_001_migrated_pg_preference_a(monkeypatch: pytest.MonkeyPatch) -> None:
    """G-01: Preference A fake-PG returns expected migration → /readyz 200."""
    env = load_fixture("settings", "ready-ok-migrated-pg")
    assert "READY-001" in env["matrix_ids"]
    assert env["payload"].get("harness") == "fake_pg_migration_ok"
    settings = _settings_from_overrides(env["payload"]["overrides"])
    expected = list_migration_files()
    assert expected, "migrations must exist for migrated-ok assert"
    stem = expected[-1].stem

    monkeypatch.setattr(
        "aibridge.readiness.connect_postgres",
        lambda _url: _FakeMigConn(stem),
    )
    client = TestClient(_memory_app(settings))
    response = client.get("/readyz")
    expect = env["payload"]["expect_readyz"]
    assert response.status_code == expect["http_status"]
    assert response.json()["status"] == expect["status"]
    # Unit path also ready (same Preference A).
    result = evaluate_readiness(settings, deployment=None)
    assert result.ready is True


@pytest.mark.parametrize(
    "name,matrix_id",
    [
        ("ready-missing-channel-bearer", "READY-002"),
        ("ready-missing-gateway-bearer", "READY-003"),
        ("ready-bearers-equal", "READY-004"),
        ("ready-intake-not-https", "READY-005"),
        ("ready-intake-missing", "READY-005"),
        ("ready-redirect-invalid", "READY-006"),
        ("ready-openai-missing", "READY-007"),
        ("ready-dry-run-required", "READY-009"),
        ("ready-database-not-postgres", "READY-014"),
    ],
)
def test_ready_bounded_reasons_from_fixtures(name: str, matrix_id: str) -> None:
    env = load_fixture("settings", name)
    assert matrix_id in env["matrix_ids"]
    settings = _settings_from_overrides(env["payload"]["overrides"])
    client = TestClient(_memory_app(settings))
    response = client.get("/readyz")
    expect = env["payload"]["expect_readyz"]
    assert response.status_code == expect["http_status"]
    assert response.json()["reason"] == expect["reason"]


def test_ready_008_openai_store_true_fails_closed() -> None:
    env = load_fixture("settings", "ready-openai-store-true")
    assert "READY-008" in env["matrix_ids"]
    expect = env["payload"]["expect"]
    with pytest.raises(ValidationError) as excinfo:
        _settings_from_overrides(env["payload"]["overrides"])
    assert expect["error_substring"] in str(excinfo.value)


def test_ready_010_content_bundle_reason() -> None:
    env = load_fixture("settings", "ready-content-bundle-not-ready")
    assert "READY-010" in env["matrix_ids"]
    settings = _settings_from_overrides(env["payload"]["overrides"])
    assert settings.content_configured()
    client = TestClient(_memory_app(settings))
    response = client.get("/readyz")
    assert response.status_code == 503
    reason = response.json()["reason"]
    needles = env["payload"].get("reason_contains_any", ["content_"])
    assert any(n in reason for n in needles), reason


def test_ready_011_tool_gen_failed() -> None:
    env = load_fixture("settings", "ready-tool-gen-failed")
    assert "READY-011" in env["matrix_ids"]
    settings = _settings_from_overrides(env["payload"]["overrides"])
    assert settings.content_configured()
    client = TestClient(_memory_app(settings))
    response = client.get("/readyz")
    expect = env["payload"]["expect_readyz"]
    assert response.status_code == expect["http_status"]
    reason = response.json()["reason"]
    assert reason.startswith(expect["reason_prefix"]), reason


def test_ready_012_database_unreachable() -> None:
    env = load_fixture("settings", "ready-database-unreachable")
    assert "READY-012" in env["matrix_ids"]
    settings = _settings_from_overrides(env["payload"]["overrides"])
    # Inject memory stores so create_app does not apply_migrations; /readyz still
    # evaluates Postgres connectivity via readiness._postgres_migration_ok.
    client = TestClient(_memory_app(settings))
    response = client.get("/readyz")
    expect = env["payload"]["expect_readyz"]
    assert response.status_code == expect["http_status"]
    assert response.json()["reason"] == expect["reason"]


def test_ready_013_migration_mismatch_fake_pg(monkeypatch: pytest.MonkeyPatch) -> None:
    """G-02: Preference A mismatch via evaluate_readiness + /readyz."""
    env = load_fixture("settings", "ready-migration-mismatch")
    assert "READY-013" in env["matrix_ids"]
    assert env["payload"].get("harness") == "fake_pg_migration_mismatch"
    settings = _settings_from_overrides(env["payload"]["overrides"])
    expected = list_migration_files()
    assert expected, "migrations must exist for mismatch assert"

    monkeypatch.setattr(
        "aibridge.readiness.connect_postgres",
        lambda _url: _FakeMigConn("0000_stale"),
    )
    result = evaluate_readiness(settings, deployment=None)
    expect = env["payload"]["expect_readyz"]
    assert result.ready is False
    assert result.reason == expect["reason"]

    client = TestClient(_memory_app(settings))
    response = client.get("/readyz")
    assert response.status_code == expect["http_status"]
    assert response.json()["reason"] == expect["reason"]


def test_ready_013_migration_version_missing_readyz(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """G-02: empty schema_migrations → migration_version_missing on /readyz."""
    env = load_fixture("settings", "ready-migration-version-missing")
    assert "READY-013" in env["matrix_ids"]
    assert env["payload"].get("harness") == "fake_pg_migration_version_missing"
    settings = _settings_from_overrides(env["payload"]["overrides"])
    monkeypatch.setattr(
        "aibridge.readiness.connect_postgres",
        lambda _url: _FakeMigConn(empty=True),
    )
    client = TestClient(_memory_app(settings))
    response = client.get("/readyz")
    expect = env["payload"]["expect_readyz"]
    assert response.status_code == expect["http_status"]
    assert response.json()["reason"] == expect["reason"]


def test_ready_013_migrations_missing_readyz(monkeypatch: pytest.MonkeyPatch) -> None:
    """G-02: empty list_migration_files → migrations_missing on /readyz."""
    env = load_fixture("settings", "ready-migrations-missing")
    assert "READY-013" in env["matrix_ids"]
    assert env["payload"].get("harness") == "fake_pg_migrations_missing"
    settings = _settings_from_overrides(env["payload"]["overrides"])
    monkeypatch.setattr(
        "aibridge.readiness.connect_postgres",
        lambda _url: _FakeMigConn("0001_any"),
    )
    monkeypatch.setattr("aibridge.readiness.list_migration_files", lambda: [])
    client = TestClient(_memory_app(settings))
    response = client.get("/readyz")
    expect = env["payload"]["expect_readyz"]
    assert response.status_code == expect["http_status"]
    assert response.json()["reason"] == expect["reason"]


def test_ready_015_no_openai_no_gateway_side_effects() -> None:
    env = load_fixture("settings", "ready-no-side-effects")
    assert "READY-015" in env["matrix_ids"]
    settings = _settings_from_overrides(env["payload"]["overrides"])
    engine = default_recording_engine()
    transport = RecordingGatewayTransport()
    executor = GatewayExecutor(
        origin=settings.intake_base_url(),
        gateway_bearer=settings.dogestonia_api_bearer_token,
        channel_bearer=settings.aibridge_channel_bearer_token,
        transport=transport,
    )
    guard = reset_confirmation_guard(
        ConfirmationGuard(executor=executor, interview_engine=engine)
    )
    app = _memory_app(settings, interview_engine=engine, confirmation_guard=guard)
    client = TestClient(app)
    response = client.get("/readyz")
    expect = env["payload"]["expect_readyz"]
    assert response.status_code == expect["http_status"]
    assert response.json()["status"] == expect["status"]
    side = env["payload"]["expect"]
    assert len(getattr(engine.client, "calls", [])) == side["openai_calls"]
    assert len(transport.calls) == side["gateway_calls"]
