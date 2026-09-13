"""Confirmation guard — FSM + tokens; gateway authorize only on Send consume."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from aibridge.action_tokens import (
    ActionTokenStore,
    TokenActionKind,
    TokenConflictError,
    TokenError,
    TokenNotFoundError,
    TokenOwnershipError,
)
from aibridge.confirm_fsm import (
    ConfirmAction,
    IllegalTransitionError,
    SessionState,
    next_state,
)
from aibridge.gateway import GatewayExecutor, GatewayOutcome, GatewayResult


@dataclass
class ConfirmSession:
    session_id: str
    user_id: str
    chat_id: str
    deployment_id: str
    state: SessionState = SessionState.INTERVIEWING
    revision: int = 1
    frozen_tool_intent: dict[str, Any] | None = None
    draft_hash: str | None = None
    gateway_authorized: bool = False
    gateway_invocations: int = 0
    last_outcome: str | None = None
    draft_id: str | None = None
    continuation_url: str | None = None
    unknown_outcome_revision: int | None = None


@dataclass
class ConfirmationGuard:
    """Issues tokens, applies dual-confirm; never equates tool intent with Send."""

    tokens: ActionTokenStore = field(default_factory=ActionTokenStore)
    executor: GatewayExecutor | None = None
    gateway_attempts: Any | None = None  # GatewayAttemptStore when PG-wired
    confirm_sessions: Any | None = None  # PostgresConfirmSessionStore when PG-wired
    _sessions: dict[str, ConfirmSession] = field(default_factory=dict)
    _by_principal: dict[tuple[str, str], str] = field(default_factory=dict)

    def call_gateway(
        self,
        session: ConfirmSession,
        *,
        body: dict[str, Any] | None = None,
    ) -> GatewayResult:
        """Gateway call site — only when gateway_authorized (Send consumed).

        REQ-03 §5.3: when gateway_attempts is wired, create+commit ``executing``
        **before** HTTPS; store outcome after. Duplicate revision fails closed
        (no second HTTPS).
        """
        if not session.gateway_authorized:
            raise RuntimeError("gateway not authorized — Send token required")
        if self.executor is None:
            # Legacy counter-only path (tests without HTTP executor).
            session.gateway_invocations += 1
            return GatewayResult(
                outcome=GatewayOutcome.STASHED,  # unused when executor is None
                reply_text="Send authorized (gateway call site).",
                http_posted=False,
            )
        if self.gateway_attempts is not None:
            # Commit-before-HTTPS — UniqueViolation → RuntimeError (fail-closed).
            self.gateway_attempts.create_executing(
                session_id=session.session_id, revision=session.revision
            )
        stash_body = body if body is not None else dict(session.frozen_tool_intent or {})
        try:
            result = self.executor.execute_stash(
                stash_body,
                gateway_authorized=session.gateway_authorized,
            )
        except Exception:
            if self.gateway_attempts is not None:
                try:
                    self.gateway_attempts.set_outcome(
                        session_id=session.session_id,
                        revision=session.revision,
                        outcome=GatewayOutcome.INTERNAL_BRIDGE_ERROR.value,
                    )
                except Exception:
                    pass
            raise
        if self.gateway_attempts is not None:
            self.gateway_attempts.set_outcome(
                session_id=session.session_id,
                revision=session.revision,
                outcome=result.outcome.value,
            )
        if result.http_posted:
            session.gateway_invocations += 1
        return result

    def authorize_from_tool_intent_alone(self, _intent: dict[str, Any]) -> bool:
        """Tool intent alone never equals Send permission."""
        return False

    def send_blocked_for_revision(self, session: ConfirmSession) -> bool:
        """AC: unknown_outcome blocks auto Send retry for same revision."""
        return (
            session.state is SessionState.UNKNOWN_OUTCOME
            or session.unknown_outcome_revision == session.revision
        )

    def _persist_session(self, sess: ConfirmSession) -> None:
        if self.confirm_sessions is None:
            return
        self.confirm_sessions.upsert(
            session_id=sess.session_id,
            user_id=sess.user_id,
            chat_id=sess.chat_id,
            state={
                "state": sess.state.value,
                "revision": sess.revision,
                "deployment_id": sess.deployment_id,
                "frozen_tool_intent": sess.frozen_tool_intent,
                "draft_hash": sess.draft_hash,
                "gateway_authorized": sess.gateway_authorized,
                "gateway_invocations": sess.gateway_invocations,
                "last_outcome": sess.last_outcome,
                "draft_id": sess.draft_id,
                "continuation_url": sess.continuation_url,
                "unknown_outcome_revision": sess.unknown_outcome_revision,
            },
        )

    def _hydrate_from_row(self, row: dict[str, Any]) -> ConfirmSession:
        st = dict(row.get("state") or {})
        sess = ConfirmSession(
            session_id=str(row["session_id"]),
            user_id=str(row["user_id"]),
            chat_id=str(row["chat_id"]),
            deployment_id=str(st.get("deployment_id") or "local"),
            state=SessionState(str(st.get("state") or SessionState.INTERVIEWING.value)),
            revision=int(st.get("revision") or 1),
            frozen_tool_intent=st.get("frozen_tool_intent"),
            draft_hash=st.get("draft_hash"),
            gateway_authorized=bool(st.get("gateway_authorized") or False),
            gateway_invocations=int(st.get("gateway_invocations") or 0),
            last_outcome=st.get("last_outcome"),
            draft_id=st.get("draft_id"),
            continuation_url=st.get("continuation_url"),
            unknown_outcome_revision=st.get("unknown_outcome_revision"),
        )
        self._sessions[sess.session_id] = sess
        self._by_principal[(sess.user_id, sess.chat_id)] = sess.session_id
        return sess

    def get_or_create_session(
        self,
        *,
        user_id: str,
        chat_id: str,
        deployment_id: str = "local",
        session_id: str | None = None,
    ) -> ConfirmSession:
        key = (user_id, chat_id)
        existing = self._by_principal.get(key)
        if existing and existing in self._sessions:
            return self._sessions[existing]
        if self.confirm_sessions is not None:
            row = self.confirm_sessions.get_by_principal(user_id=user_id, chat_id=chat_id)
            if row is not None:
                return self._hydrate_from_row(row)
        sid = session_id or f"sess_{uuid.uuid4().hex[:16]}"
        sess = ConfirmSession(
            session_id=sid,
            user_id=user_id,
            chat_id=chat_id,
            deployment_id=deployment_id,
        )
        self._sessions[sid] = sess
        self._by_principal[key] = sid
        self._persist_session(sess)
        return sess

    def get_session(self, session_id: str) -> ConfirmSession | None:
        if session_id in self._sessions:
            return self._sessions[session_id]
        if self.confirm_sessions is not None:
            row = self.confirm_sessions.get(session_id)
            if row is not None:
                return self._hydrate_from_row(row)
        return None

    def set_frozen_tool_intent(
        self,
        session_id: str,
        intent: dict[str, Any],
        *,
        draft_hash: str | None = None,
    ) -> None:
        sess = self._sessions[session_id]
        sess.frozen_tool_intent = dict(intent)
        if draft_hash is not None:
            sess.draft_hash = draft_hash

    def offer_interpretation_confirm(self, session_id: str) -> list[dict[str, str]]:
        sess = self._sessions[session_id]
        sess.state = next_state(sess.state, ConfirmAction.OFFER_INTERPRETATION)
        return self._mint_bundle(
            sess,
            kinds=(
                TokenActionKind.CONFIRM_INTERPRETATION,
                TokenActionKind.EDIT,
                TokenActionKind.CANCEL,
            ),
            labels={
                TokenActionKind.CONFIRM_INTERPRETATION: ("Looks right", "success"),
                TokenActionKind.EDIT: ("Edit", "default"),
                TokenActionKind.CANCEL: ("Cancel", "danger"),
            },
        )

    def offer_send_confirm(self, session_id: str) -> list[dict[str, str]]:
        sess = self._sessions[session_id]
        if self.send_blocked_for_revision(sess):
            raise IllegalTransitionError(sess.state, ConfirmAction.OFFER_SEND)
        if sess.frozen_tool_intent is None:
            raise IllegalTransitionError(sess.state, ConfirmAction.OFFER_SEND)
        # Tool intent alone must not authorize gateway.
        assert self.authorize_from_tool_intent_alone(sess.frozen_tool_intent) is False
        sess.state = next_state(sess.state, ConfirmAction.OFFER_SEND)
        return self._mint_bundle(
            sess,
            kinds=(
                TokenActionKind.CONFIRM_SEND,
                TokenActionKind.EDIT,
                TokenActionKind.CANCEL,
            ),
            labels={
                TokenActionKind.CONFIRM_SEND: ("Send to DOGEstonia", "primary"),
                TokenActionKind.EDIT: ("Edit", "default"),
                TokenActionKind.CANCEL: ("Cancel", "danger"),
            },
        )

    def _mint_bundle(
        self,
        sess: ConfirmSession,
        *,
        kinds: tuple[TokenActionKind, ...],
        labels: dict[TokenActionKind, tuple[str, str]],
    ) -> list[dict[str, str]]:
        actions: list[dict[str, str]] = []
        for kind in kinds:
            raw, _rec = self.tokens.issue(
                action=kind,
                session_id=sess.session_id,
                user_id=sess.user_id,
                chat_id=sess.chat_id,
                deployment_id=sess.deployment_id,
                revision=sess.revision,
                expected_state=sess.state.value,
                draft_hash=sess.draft_hash,
            )
            label, style = labels[kind]
            actions.append({"label": label, "token": raw, "style": style})
        return actions

    def apply_edit(self, session_id: str) -> ConfirmSession:
        sess = self._sessions[session_id]
        old_rev = sess.revision
        sess.state = next_state(sess.state, ConfirmAction.EDIT)
        self.tokens.invalidate_session_revision(session_id, revision=old_rev)
        sess.revision += 1
        sess.frozen_tool_intent = None
        sess.draft_hash = None
        sess.gateway_authorized = False
        sess.last_outcome = None
        sess.draft_id = None
        sess.continuation_url = None
        # Edit increments revision — clears unknown block for *old* revision only.
        if sess.unknown_outcome_revision == old_rev:
            sess.unknown_outcome_revision = None
        self._persist_session(sess)
        return sess

    def apply_cancel(self, session_id: str) -> ConfirmSession:
        sess = self._sessions[session_id]
        sess.state = next_state(sess.state, ConfirmAction.CANCEL)
        self.tokens.invalidate_session_revision(session_id)
        sess.draft_hash = None
        sess.gateway_authorized = False
        sess.last_outcome = GatewayOutcome.CANCELLED.value
        sess.draft_id = None
        sess.continuation_url = None
        self._persist_session(sess)
        return sess

    def _apply_gateway_result(self, sess: ConfirmSession, result: GatewayResult) -> str:
        sess.last_outcome = result.outcome.value
        sess.draft_id = result.draft_id
        sess.continuation_url = result.continuation_url
        if result.outcome is GatewayOutcome.STASHED:
            sess.state = next_state(sess.state, ConfirmAction.MARK_STASHED)
            sess.gateway_authorized = False
        elif result.outcome is GatewayOutcome.UNKNOWN_OUTCOME:
            sess.state = next_state(sess.state, ConfirmAction.MARK_UNKNOWN_OUTCOME)
            sess.unknown_outcome_revision = sess.revision
            sess.gateway_authorized = False
        elif result.outcome is GatewayOutcome.DRY_RUN_OK:
            # Wave-1: validated locally, no stash, no published claim.
            sess.gateway_authorized = False
        elif result.outcome is GatewayOutcome.BLOCKED_BY_CONFIRMATION:
            sess.gateway_authorized = False
        else:
            # Other failures from EXECUTING → FAILED when transition exists.
            if sess.state is SessionState.EXECUTING:
                sess.state = next_state(sess.state, ConfirmAction.MARK_FAILED)
            sess.gateway_authorized = False
            sess.draft_id = None
            sess.continuation_url = None
        return result.reply_text

    def consume_action_token(
        self,
        raw_token: str,
        *,
        user_id: str,
        chat_id: str,
    ) -> dict[str, Any]:
        """Verify + apply token. Returns result dict for channel envelope."""
        try:
            rec = self.tokens.verify_for_consume(
                raw_token, user_id=user_id, chat_id=chat_id
            )
        except TokenOwnershipError as exc:
            return {"ok": False, "http_status": 403, "code": exc.code, "message": exc.message}
        except TokenNotFoundError as exc:
            return {"ok": False, "http_status": 404, "code": exc.code, "message": exc.message}
        except TokenConflictError as exc:
            return {"ok": False, "http_status": 409, "code": exc.code, "message": exc.message}
        except TokenError as exc:
            return {"ok": False, "http_status": 409, "code": exc.code, "message": exc.message}

        sess = self.get_session(rec.session_id)
        if sess is None:
            return {
                "ok": False,
                "http_status": 404,
                "code": "not_found",
                "message": "Session unavailable",
            }
        if rec.revision != sess.revision:
            return {
                "ok": False,
                "http_status": 409,
                "code": "conflict",
                "message": "Token revision mismatch",
            }
        if sess.state.value != rec.expected_state:
            return {
                "ok": False,
                "http_status": 409,
                "code": "conflict",
                "message": "Invalid state for token",
            }

        try:
            if rec.action is TokenActionKind.CONFIRM_INTERPRETATION:
                sess.state = next_state(sess.state, ConfirmAction.CONFIRM_INTERPRETATION)
                sess.gateway_authorized = False
                self.tokens.consume(raw_token)
                self.tokens.invalidate_session_revision(sess.session_id, revision=sess.revision)
                reply = "Interpretation confirmed."
                actions: list[dict[str, str]] = []
            elif rec.action is TokenActionKind.CONFIRM_SEND:
                if self.send_blocked_for_revision(sess):
                    return {
                        "ok": False,
                        "http_status": 409,
                        "code": "conflict",
                        "message": (
                            "unknown_outcome blocks auto Send for this revision; "
                            "see docs/runbooks/unknown-outcome-reconciliation.md"
                        ),
                    }
                if sess.frozen_tool_intent is None:
                    return {
                        "ok": False,
                        "http_status": 409,
                        "code": "conflict",
                        "message": "Frozen tool intent required for Send",
                    }
                sess.state = next_state(sess.state, ConfirmAction.CONFIRM_SEND)
                self.tokens.consume(raw_token)
                self.tokens.invalidate_session_revision(sess.session_id, revision=sess.revision)
                sess.gateway_authorized = True
                try:
                    result = self.call_gateway(sess, body=dict(sess.frozen_tool_intent))
                except RuntimeError as exc:
                    # Duplicate gateway_attempt / fail-closed before HTTPS.
                    self._persist_session(sess)
                    return {
                        "ok": False,
                        "http_status": 409,
                        "code": "conflict",
                        "message": str(exc),
                    }
                if self.executor is None:
                    # Story 04 call-site only (no HTTP executor).
                    reply = "Send authorized (gateway call site)."
                else:
                    reply = self._apply_gateway_result(sess, result)
                actions = []
            elif rec.action is TokenActionKind.EDIT:
                self.tokens.consume(raw_token)
                self.apply_edit(sess.session_id)
                reply = "Edit started — prior actions invalidated."
                actions = []
            elif rec.action is TokenActionKind.CANCEL:
                self.tokens.consume(raw_token)
                self.apply_cancel(sess.session_id)
                reply = "Cancelled."
                actions = []
            else:
                return {
                    "ok": False,
                    "http_status": 409,
                    "code": "conflict",
                    "message": "Unknown action kind",
                }
        except IllegalTransitionError:
            return {
                "ok": False,
                "http_status": 409,
                "code": "conflict",
                "message": "Invalid state transition",
            }

        self._persist_session(sess)
        return {
            "ok": True,
            "http_status": 200,
            "session_id": sess.session_id,
            "state": sess.state.value,
            "reply_text": reply,
            "actions": actions,
            "gateway_authorized": sess.gateway_authorized,
            "gateway_invocations": sess.gateway_invocations,
            "revision": sess.revision,
            "outcome": sess.last_outcome,
            "draft_id": sess.draft_id,
            "continuation_url": sess.continuation_url,
        }


# Process-local default for ASGI (tests may inject).
_default_guard: ConfirmationGuard | None = None


def get_confirmation_guard() -> ConfirmationGuard:
    global _default_guard
    if _default_guard is None:
        _default_guard = ConfirmationGuard()
    return _default_guard


def reset_confirmation_guard(guard: ConfirmationGuard | None = None) -> ConfirmationGuard:
    global _default_guard
    _default_guard = guard if guard is not None else ConfirmationGuard()
    return _default_guard
