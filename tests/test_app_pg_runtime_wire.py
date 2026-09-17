"""G-01 — create_app wires pg_runtime when postgres + !allow_memory."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.confirm import reset_confirmation_guard
from aibridge.db import is_postgres_url
from aibridge.dedupe import EventDedupeStore
from aibridge.migrate import apply_migrations
from aibridge.pg_runtime import (
    GatewayAttemptStore,
    PostgresActionTokenStore,
    PostgresConfirmSessionStore,
    PostgresEventDedupeStore,
    PostgresHistoryStore,
    PostgresTurnLock,
)

PGDATA = Path(__file__).resolve().parents[1] / ".pgdata-test"
PGPORT = "55432"
DISPOSABLE_URL = (
    f"postgresql://aibridge@/aibridge_test?host={PGDATA}&port={PGPORT}"
)


def _pg_available() -> bool:
    if not PGDATA.is_dir():
        return False
    try:
        from aibridge.db import connect_postgres

        conn = connect_postgres(DISPOSABLE_URL)
        conn.execute("SELECT 1")
        conn.close()
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _pg_available(),
    reason="disposable Postgres (.pgdata-test) not running",
)


@pytest.fixture()
def pg_url() -> str:
    assert is_postgres_url(DISPOSABLE_URL)
    apply_migrations(DISPOSABLE_URL)
    from aibridge.db import connect_postgres

    conn = connect_postgres(DISPOSABLE_URL)
    for table in (
        "event_dedupe",
        "action_token",
        "session_call",
        "gateway_attempt",
        "session_turn_lock",
        "conversation_history",
        "confirm_session",
        "session",
        "content_bundle",
    ):
        conn.execute(f"TRUNCATE {table} CASCADE")
    conn.commit()
    conn.close()
    return DISPOSABLE_URL


def test_create_app_wires_pg_runtime_without_manual_inject(pg_url: str) -> None:
    reset_settings_cache()
    reset_confirmation_guard()
    channel = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    settings = Settings(
        AIBRIDGE_CHANNEL_BEARER_TOKEN=channel,
        DOGESTONIA_API_BEARER_TOKEN="gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        DOGESTONIA_INTAKE_BASE_URL="https://gateway.example.invalid",
        AIBRIDGE_DRY_RUN=True,
        DATABASE_URL=pg_url,
        AIBRIDGE_ALLOW_MEMORY_STORES=False,
    )
    app = create_app(settings=settings)
    assert isinstance(app.state.dedupe_store, PostgresEventDedupeStore)
    guard = app.state.confirmation_guard
    assert isinstance(guard.tokens, PostgresActionTokenStore)
    assert isinstance(guard.gateway_attempts, GatewayAttemptStore)
    assert isinstance(guard.confirm_sessions, PostgresConfirmSessionStore)
    assert isinstance(app.state.turn_lock, PostgresTurnLock)
    assert isinstance(app.state.history_store, PostgresHistoryStore)

    client = TestClient(app)
    headers = {"Authorization": f"Bearer {channel}"}
    r = client.post(
        "/v1/channel/turns",
        json={
            "channel": "telegram",
            "event_id": "pg-wire-turn-1",
            "principal": {"user_id": "42", "chat_id": "99"},
            "message": {"message_id": "1", "text": "hello pg"},
        },
        headers=headers,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["session_id"]
    # Replay from PG dedupe (no second side effect)
    r2 = client.post(
        "/v1/channel/turns",
        json={
            "channel": "telegram",
            "event_id": "pg-wire-turn-1",
            "principal": {"user_id": "42", "chat_id": "99"},
            "message": {"message_id": "1", "text": "hello pg again"},
        },
        headers=headers,
    )
    assert r2.status_code == 200
    assert r2.json()["request_id"] == body["request_id"]


def test_create_app_keeps_memory_when_allow_memory(pg_url: str) -> None:
    reset_settings_cache()
    reset_confirmation_guard()
    settings = Settings(
        AIBRIDGE_CHANNEL_BEARER_TOKEN="channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        DATABASE_URL=pg_url,
        AIBRIDGE_ALLOW_MEMORY_STORES=True,
    )
    app = create_app(settings=settings, dedupe_store=EventDedupeStore())
    assert isinstance(app.state.dedupe_store, EventDedupeStore)
    assert app.state.turn_lock is None
