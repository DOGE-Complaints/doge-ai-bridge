"""Privacy retention — TTL slide, narrative minimize, ops session-delete (R3-P1-10).

Ops delete is **not** a channel OpenAPI route (HTTP path Unknown). Callers must
present ``AIBRIDGE_OPS_BEARER_TOKEN``; mismatch/absent → fail-closed.
"""

from __future__ import annotations

import secrets
import time
from dataclasses import dataclass, field
from typing import Any, Protocol

from aibridge.action_tokens import (
    ActionTokenStore,
    TokenConflictError,
    TokenNotFoundError,
    TokenRecordState,
)
from aibridge.audit import audit_event
from aibridge.history import HistoryStore

# REQ-03 §6.2 / privacy-pilot — pilot default 7 days.
PILOT_SESSION_TTL_SECONDS = 604_800

# Minimized non-PII replay tombstone (may be retained for audit window).
TOMBSTONE_ITEM: dict[str, Any] = {
    "type": "privacy_tombstone",
    "redacted": True,
    "pii": False,
}


class OpsAuthError(PermissionError):
    """Ops session-delete authz failure (fail-closed)."""


@dataclass
class SessionActivityClock:
    """Sliding TTL clock — advances only via explicit ``touch`` (legitimate activity)."""

    ttl_seconds: int = PILOT_SESSION_TTL_SECONDS
    _last: dict[str, float] = field(default_factory=dict)

    def seed(self, session_id: str, last_activity: float) -> None:
        """Restore durable last-activity (e.g. confirm_session.updated_at) after restart."""
        self._last[session_id] = float(last_activity)

    def touch(self, session_id: str, *, now: float | None = None) -> None:
        self._last[session_id] = now if now is not None else time.time()

    def last_activity(self, session_id: str) -> float | None:
        return self._last.get(session_id)

    def is_expired(self, session_id: str, *, now: float | None = None) -> bool:
        ts = now if now is not None else time.time()
        last = self._last.get(session_id)
        if last is None:
            return False
        return (ts - last) > self.ttl_seconds

    def clear(self, session_id: str) -> None:
        self._last.pop(session_id, None)


def minimize_narrative(history: HistoryStore, session_id: str) -> None:
    """Delete narrative body; retain a single non-PII tombstone."""
    history.replace(session_id, [dict(TOMBSTONE_ITEM)])


def purge_expired_pending_tokens(
    tokens: Any,
    *,
    now: float | None = None,
) -> int:
    """Drop pending tokens past ``expires_at``. Keep CONSUMED (tombstone / non-usable)."""
    purge = getattr(tokens, "purge_expired_pending", None)
    if callable(purge):
        return int(purge(now=now))
    ts = now if now is not None else time.time()
    to_drop: list[str] = []
    by_hash = getattr(tokens, "_by_hash", None)
    if not isinstance(by_hash, dict):
        return 0
    for th, rec in list(by_hash.items()):
        if rec.state is TokenRecordState.PENDING and ts > rec.expires_at:
            to_drop.append(th)
    for th in to_drop:
        del by_hash[th]
    return len(to_drop)


def assert_consumed_unusable(tokens: ActionTokenStore, raw: str) -> None:
    """Target #2 — consumed token must not verify for consume."""
    try:
        rec = tokens.lookup(raw)
    except TokenNotFoundError:
        return
    if rec.state is TokenRecordState.CONSUMED:
        try:
            tokens.verify_for_consume(
                raw, user_id=rec.user_id, chat_id=rec.chat_id
            )
        except TokenConflictError:
            return
        raise AssertionError("consumed token became usable")
    raise AssertionError(f"expected consumed state, got {rec.state}")


def verify_ops_bearer(*, presented: str, expected: str) -> None:
    """Fail-closed: empty expected or mismatch → OpsAuthError."""
    if not expected or not presented:
        raise OpsAuthError("ops bearer required")
    if not secrets.compare_digest(presented, expected):
        raise OpsAuthError("ops bearer mismatch")


@dataclass
class OpsDeleteResult:
    session_id: str
    narrative_minimized: bool
    tokens_invalidated: int
    session_deactivated: bool
    confirm_dropped: bool


class _ConfirmGuardProto(Protocol):
    tokens: ActionTokenStore
    _sessions: dict[str, Any]
    _by_principal: dict[tuple[str, str], str]

    def get_session(self, session_id: str) -> Any: ...


def ops_delete_session(
    *,
    session_id: str,
    ops_bearer_presented: str,
    ops_bearer_expected: str,
    history: HistoryStore | None = None,
    tokens: ActionTokenStore | None = None,
    guard: _ConfirmGuardProto | None = None,
    session_store: Any | None = None,
    activity_clock: SessionActivityClock | None = None,
) -> OpsDeleteResult:
    """Authenticated ops-only session delete — covers history, pending tokens, confirm.

    Does **not** register a channel OpenAPI path.
    """
    verify_ops_bearer(
        presented=ops_bearer_presented, expected=ops_bearer_expected
    )
    narrative_minimized = False
    if history is not None:
        minimize_narrative(history, session_id)
        narrative_minimized = True

    tokens_invalidated = 0
    token_store = tokens
    if token_store is None and guard is not None:
        token_store = guard.tokens
    if token_store is not None:
        tokens_invalidated = token_store.invalidate_session_revision(session_id)

    confirm_dropped = False
    if guard is not None:
        sess = guard.get_session(session_id)
        if sess is not None:
            key = (sess.user_id, sess.chat_id)
            guard._sessions.pop(session_id, None)
            if guard._by_principal.get(key) == session_id:
                guard._by_principal.pop(key, None)
            confirm_dropped = True
        cs = getattr(guard, "confirm_sessions", None)
        if cs is not None and hasattr(cs, "delete"):
            cs.delete(session_id)
            confirm_dropped = True

    session_deactivated = False
    if session_store is not None and hasattr(session_store, "deactivate"):
        session_store.deactivate(session_id)
        session_deactivated = True

    if activity_clock is not None:
        activity_clock.clear(session_id)

    audit_event(
        "ops_session_delete",
        detail=f"session_id_len={len(session_id)} invalidated={tokens_invalidated}",
    )
    return OpsDeleteResult(
        session_id=session_id,
        narrative_minimized=narrative_minimized,
        tokens_invalidated=tokens_invalidated,
        session_deactivated=session_deactivated,
        confirm_dropped=confirm_dropped,
    )


def expire_idle_session_narrative(
    *,
    session_id: str,
    activity_clock: SessionActivityClock,
    history: HistoryStore | None,
    tokens: ActionTokenStore | None = None,
    now: float | None = None,
) -> bool:
    """If idle past TTL: minimize narrative and purge expired pending tokens.

    Returns True when expiry actions ran.
    """
    if not activity_clock.is_expired(session_id, now=now):
        return False
    if history is not None:
        minimize_narrative(history, session_id)
    if tokens is not None:
        purge_expired_pending_tokens(tokens, now=now)
        tokens.invalidate_session_revision(session_id)
    activity_clock.clear(session_id)
    audit_event("session_ttl_expired", detail=f"session_id_len={len(session_id)}")
    return True
