"""STORY-AIBRIDGE-16 — privacy retention (TTL, minimize, ops delete, consumed invariant)."""

from __future__ import annotations

import time

import pytest

from aibridge.action_tokens import (
    ActionTokenStore,
    TokenActionKind,
    TokenConflictError,
    TokenRecordState,
)
from aibridge.audit import get_audit_buffer, reset_audit_buffer
from aibridge.config import DEFAULT_SESSION_TTL_SECONDS, Settings
from aibridge.confirm import ConfirmationGuard
from aibridge.history import HistoryStore
from aibridge.privacy_retention import (
    PILOT_SESSION_TTL_SECONDS,
    TOMBSTONE_ITEM,
    OpsAuthError,
    SessionActivityClock,
    assert_consumed_unusable,
    expire_idle_session_narrative,
    minimize_narrative,
    ops_delete_session,
    purge_expired_pending_tokens,
    verify_ops_bearer,
)
from aibridge.sessions import MemorySessionStore


def test_pilot_session_ttl_default_is_604800() -> None:
    assert DEFAULT_SESSION_TTL_SECONDS == 604_800
    assert PILOT_SESSION_TTL_SECONDS == 604_800
    settings = Settings(_env_file=None)
    assert settings.aibridge_session_ttl_seconds == 604_800


def test_activity_clock_slides_only_on_touch() -> None:
    clock = SessionActivityClock(ttl_seconds=10)
    clock.touch("s1", now=100.0)
    assert clock.is_expired("s1", now=105.0) is False
    # No touch — still based on last activity
    assert clock.is_expired("s1", now=111.0) is True
    clock.touch("s1", now=111.0)
    assert clock.is_expired("s1", now=115.0) is False


def test_memory_session_touch_slides_ttl() -> None:
    store = MemorySessionStore(ttl_seconds=5)
    store.create(session_id="s-touch", content_bundle_hash="h", deployment_id="d")
    from datetime import datetime, timedelta, timezone

    row = store._rows["s-touch"]
    store._rows["s-touch"] = type(row)(
        session_id=row.session_id,
        content_bundle_hash=row.content_bundle_hash,
        deployment_id=row.deployment_id,
        active=True,
        created_at=row.created_at,
        updated_at=datetime.now(timezone.utc) - timedelta(seconds=10),
    )
    assert store.get("s-touch").active is False  # type: ignore[union-attr]
    store.create(session_id="s-touch2", content_bundle_hash="h", deployment_id="d")
    store.touch("s-touch2")
    assert store.get("s-touch2").active is True  # type: ignore[union-attr]


def test_minimize_narrative_leaves_tombstone_only() -> None:
    hist = HistoryStore()
    hist.append("s1", {"role": "user", "content": "SECRET_PHRASE_XYZ"})
    hist.append("s1", {"role": "assistant", "content": "reply"})
    minimize_narrative(hist, "s1")
    items = hist.list_items("s1")
    assert len(items) == 1
    assert items[0]["type"] == TOMBSTONE_ITEM["type"]
    assert items[0]["pii"] is False
    assert "SECRET_PHRASE_XYZ" not in str(items)


def test_purge_expired_pending_keeps_consumed() -> None:
    store = ActionTokenStore(ttl_seconds=1)
    raw_p, _ = store.issue(
        action=TokenActionKind.CANCEL,
        session_id="s1",
        user_id="u",
        chat_id="c",
        deployment_id="d",
        revision=1,
        expected_state="interviewing",
        now=100.0,
    )
    raw_c, _ = store.issue(
        action=TokenActionKind.CONFIRM_SEND,
        session_id="s1",
        user_id="u",
        chat_id="c",
        deployment_id="d",
        revision=1,
        expected_state="awaiting_send",
        now=100.0,
    )
    store.consume(raw_c)
    n = purge_expired_pending_tokens(store, now=200.0)
    assert n == 1
    with pytest.raises(Exception):
        store.lookup(raw_p)
    rec = store.lookup(raw_c)
    assert rec.state is TokenRecordState.CONSUMED
    assert_consumed_unusable(store, raw_c)


def test_expire_idle_minimizes_and_invalidates() -> None:
    clock = SessionActivityClock(ttl_seconds=1)
    hist = HistoryStore()
    hist.append("s1", {"text": "resident narrative"})
    tokens = ActionTokenStore(ttl_seconds=60)
    raw, _ = tokens.issue(
        action=TokenActionKind.EDIT,
        session_id="s1",
        user_id="u",
        chat_id="c",
        deployment_id="d",
        revision=1,
        expected_state="interviewing",
        now=time.time(),
    )
    clock.touch("s1", now=1.0)
    assert expire_idle_session_narrative(
        session_id="s1",
        activity_clock=clock,
        history=hist,
        tokens=tokens,
        now=10.0,
    )
    assert hist.list_items("s1")[0]["type"] == "privacy_tombstone"
    assert tokens.lookup(raw).state is TokenRecordState.INVALIDATED


def test_ops_delete_failclosed_without_bearer() -> None:
    with pytest.raises(OpsAuthError):
        verify_ops_bearer(presented="", expected="secret")
    with pytest.raises(OpsAuthError):
        verify_ops_bearer(presented="wrong", expected="secret")
    verify_ops_bearer(presented="secret", expected="secret")


def test_ops_delete_covers_history_tokens_confirm() -> None:
    reset_audit_buffer()
    hist = HistoryStore()
    hist.append("sess_1", {"content": "PRIVATE"})
    guard = ConfirmationGuard()
    sess = guard.get_or_create_session(user_id="u1", chat_id="c1", session_id="sess_1")
    raw, _ = guard.tokens.issue(
        action=TokenActionKind.CANCEL,
        session_id=sess.session_id,
        user_id="u1",
        chat_id="c1",
        deployment_id="d",
        revision=1,
        expected_state="interviewing",
    )
    # Consume one token first — must stay unusable after delete.
    raw2, _ = guard.tokens.issue(
        action=TokenActionKind.EDIT,
        session_id=sess.session_id,
        user_id="u1",
        chat_id="c1",
        deployment_id="d",
        revision=1,
        expected_state="interviewing",
    )
    guard.tokens.consume(raw2)

    result = ops_delete_session(
        session_id=sess.session_id,
        ops_bearer_presented="ops-secret",
        ops_bearer_expected="ops-secret",
        history=hist,
        guard=guard,
        session_store=MemorySessionStore(),
    )
    assert result.narrative_minimized is True
    assert result.tokens_invalidated >= 1
    assert result.confirm_dropped is True
    assert "PRIVATE" not in str(hist.list_items(sess.session_id))
    assert guard.tokens.lookup(raw).state is TokenRecordState.INVALIDATED
    assert_consumed_unusable(guard.tokens, raw2)
    with pytest.raises(TokenConflictError):
        guard.tokens.verify_for_consume(raw2, user_id="u1", chat_id="c1")
    buf = get_audit_buffer().dump_text()
    assert "ops_session_delete" in buf
    assert "PRIVATE" not in buf


def test_ops_delete_cli_authz_module_importable() -> None:
    from aibridge.ops_session_delete import main

    # Missing/wrong bearer → exit 2 (fail-closed). Env expected empty by default.
    code = main(["--session-id", "sess_x", "--ops-bearer", "anything"])
    assert code == 2


def test_guard_activity_clock_touch_on_create() -> None:
    clock = SessionActivityClock(ttl_seconds=60)
    guard = ConfirmationGuard(activity_clock=clock)
    s1 = guard.get_or_create_session(user_id="u", chat_id="c")
    assert clock.last_activity(s1.session_id) is not None
    t0 = clock.last_activity(s1.session_id)
    time.sleep(0.01)
    s2 = guard.get_or_create_session(user_id="u", chat_id="c")
    assert s2.session_id == s1.session_id
    assert clock.last_activity(s1.session_id) >= t0  # type: ignore[operator]


def test_channel_openapi_has_no_session_delete_path() -> None:
    from pathlib import Path

    import yaml

    oas = (
        Path(__file__).resolve().parents[1]
        / "docs"
        / "openapi"
        / "aibridge-channel-v1.openapi.yaml"
    )
    doc = yaml.safe_load(oas.read_text(encoding="utf-8"))
    paths = doc.get("paths") or {}
    assert not any("session-delete" in p or "session_delete" in p for p in paths)
    for p, methods in paths.items():
        if not str(p).startswith("/v1/channel"):
            continue
        assert "delete" not in {str(k).lower() for k in (methods or {})}
