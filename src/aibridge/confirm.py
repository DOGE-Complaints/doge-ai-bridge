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


@dataclass
class ConfirmationGuard:
    """Issues tokens, applies dual-confirm; never equates tool intent with Send."""

    tokens: ActionTokenStore = field(default_factory=ActionTokenStore)
    _sessions: dict[str, ConfirmSession] = field(default_factory=dict)
    _by_principal: dict[tuple[str, str], str] = field(default_factory=dict)

    def call_gateway(self, session: ConfirmSession) -> None:
        """Gateway call site — only when gateway_authorized (Send consumed)."""
        if not session.gateway_authorized:
            raise RuntimeError("gateway not authorized — Send token required")
        session.gateway_invocations += 1

    def authorize_from_tool_intent_alone(self, _intent: dict[str, Any]) -> bool:
        """AC #5: tool intent alone never equals Send permission."""
        return False

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
        sid = session_id or f"sess_{uuid.uuid4().hex[:16]}"
        sess = ConfirmSession(
            session_id=sid,
            user_id=user_id,
            chat_id=chat_id,
            deployment_id=deployment_id,
        )
        self._sessions[sid] = sess
        self._by_principal[key] = sid
        return sess

    def get_session(self, session_id: str) -> ConfirmSession | None:
        return self._sessions.get(session_id)

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
        return sess

    def apply_cancel(self, session_id: str) -> ConfirmSession:
        sess = self._sessions[session_id]
        sess.state = next_state(sess.state, ConfirmAction.CANCEL)
        self.tokens.invalidate_session_revision(session_id)
        sess.draft_hash = None
        sess.gateway_authorized = False
        return sess

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

        sess = self._sessions.get(rec.session_id)
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
                # Never authorize gateway on interpretation.
                sess.gateway_authorized = False
                self.tokens.consume(raw_token)
                self.tokens.invalidate_session_revision(sess.session_id, revision=sess.revision)
                reply = "Interpretation confirmed."
                actions: list[dict[str, str]] = []
                # After interpretation, operator may freeze intent then offer send (P3 helper).
            elif rec.action is TokenActionKind.CONFIRM_SEND:
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
                # Call site gated — story 05 does real HTTP; here only increment if authorized.
                self.call_gateway(sess)
                # Wave-1: do not stash; leave executing (HTTP executor out of scope).
                reply = "Send authorized (gateway call site)."
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
