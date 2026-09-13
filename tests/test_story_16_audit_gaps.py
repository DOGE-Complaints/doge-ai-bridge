"""STORY-AIBRIDGE-16 P6 audit gaps G-01/G-02/G-03."""

from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from aibridge.action_tokens import ActionTokenStore, TokenActionKind, TokenRecordState
from aibridge.confirm import ConfirmationGuard
from aibridge.history import HistoryStore
from aibridge.privacy_retention import SessionActivityClock, TOMBSTONE_ITEM
from tests.story13_e2e_helpers import DISPOSABLE_URL, pg_available, truncate_pg

pytestmark_pg = pytest.mark.skipif(
    not pg_available(),
    reason="disposable Postgres (.pgdata-test) not running — ./scripts/start-disposable-pg.sh",
)


def test_g01_expire_idle_minimizes_history_on_confirm_path() -> None:
    """G-01: idle expiry must minimize narrative, not only pop maps."""
    clock = SessionActivityClock(ttl_seconds=1)
    hist = HistoryStore()
    tokens = ActionTokenStore(ttl_seconds=60)
    guard = ConfirmationGuard(tokens=tokens, activity_clock=clock, history=hist)
    sess = guard.get_or_create_session(
        user_id="u", chat_id="c", session_id="sess_idle"
    )
    hist.append(sess.session_id, {"content": "RESIDENT_SECRET_PHRASE"})
    raw, _ = tokens.issue(
        action=TokenActionKind.CANCEL,
        session_id=sess.session_id,
        user_id="u",
        chat_id="c",
        deployment_id="d",
        revision=1,
        expected_state="interviewing",
    )
    clock.seed(sess.session_id, time.time() - 10)
    sess2 = guard.get_or_create_session(user_id="u", chat_id="c")
    assert sess2.session_id != sess.session_id
    items = hist.list_items(sess.session_id)
    assert items and items[0]["type"] == TOMBSTONE_ITEM["type"]
    assert "RESIDENT_SECRET_PHRASE" not in str(items)
    assert tokens.lookup(raw).state is TokenRecordState.INVALIDATED


def test_g01_durable_updated_at_expiry_without_process_clock() -> None:
    """G-01: durable confirm updated_at drives expiry even when clock empty."""

    class FakeConfirmStore:
        def __init__(self) -> None:
            self.rows: dict[str, dict] = {}
            self.deleted: list[str] = []

        def get_by_principal(self, *, user_id: str, chat_id: str):
            for r in self.rows.values():
                if r["user_id"] == user_id and r["chat_id"] == chat_id:
                    return r
            return None

        def get(self, session_id: str):
            return self.rows.get(session_id)

        def upsert(self, **kwargs):
            return None

        def delete(self, session_id: str) -> None:
            self.deleted.append(session_id)
            self.rows.pop(session_id, None)

    store = FakeConfirmStore()
    store.rows["old"] = {
        "session_id": "old",
        "user_id": "u",
        "chat_id": "c",
        "state": {
            "state": "interviewing",
            "revision": 1,
            "deployment_id": "d",
            "frozen_tool_intent": None,
            "draft_hash": None,
            "gateway_authorized": False,
            "gateway_invocations": 0,
            "last_outcome": None,
            "draft_id": None,
            "continuation_url": None,
            "unknown_outcome_revision": None,
            "pending_call_id": None,
            "pending_replay_items": None,
        },
        "updated_at": datetime.now(timezone.utc) - timedelta(seconds=100),
    }
    hist = HistoryStore()
    hist.append("old", {"text": "stale narrative"})
    clock = SessionActivityClock(ttl_seconds=10)
    guard = ConfirmationGuard(
        confirm_sessions=store,
        activity_clock=clock,
        history=hist,
        tokens=ActionTokenStore(),
    )
    sess = guard.get_or_create_session(user_id="u", chat_id="c")
    assert sess.session_id != "old"
    assert hist.list_items("old")[0]["type"] == "privacy_tombstone"
    assert "old" in store.deleted


def test_g02_ops_cli_requires_postgres_after_authz(monkeypatch: pytest.MonkeyPatch) -> None:
    from aibridge import ops_session_delete as mod
    from aibridge.config import get_settings

    monkeypatch.setenv("AIBRIDGE_OPS_BEARER_TOKEN", "ops-secret")
    monkeypatch.setenv("DATABASE_URL", "")
    get_settings.cache_clear()
    code = mod.main(["--session-id", "s1", "--ops-bearer", "ops-secret"])
    assert code == 3
    get_settings.cache_clear()


@pytestmark_pg
def test_g02_ops_cli_pg_minimizes_history(monkeypatch: pytest.MonkeyPatch) -> None:
    truncate_pg()
    monkeypatch.setenv("AIBRIDGE_OPS_BEARER_TOKEN", "ops-secret")
    monkeypatch.setenv("DATABASE_URL", DISPOSABLE_URL)
    from aibridge.config import get_settings
    from aibridge.migrate import apply_migrations
    from aibridge.ops_session_delete import main
    from aibridge.pg_runtime import PostgresHistoryStore

    get_settings.cache_clear()
    apply_migrations(DISPOSABLE_URL)
    hist = PostgresHistoryStore(DISPOSABLE_URL)
    hist.append("sess_pg", {"content": "PG_SECRET"})
    code = main(["--session-id", "sess_pg", "--ops-bearer", "ops-secret"])
    assert code == 0
    items = hist.list_items("sess_pg")
    assert items[0]["type"] == "privacy_tombstone"
    assert "PG_SECRET" not in str(items)
    get_settings.cache_clear()


def test_g03_privacy_pilot_documents_residual() -> None:
    text = (
        Path(__file__).resolve().parents[1] / "docs" / "runbooks" / "privacy-pilot.md"
    ).read_text(encoding="utf-8")
    assert "ops-before-residents" in text or "G-03" in text
    assert "n8n" in text.lower()
