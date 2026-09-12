"""Channel turn/action processing — dual-confirm wired for actions (story 04)."""

from __future__ import annotations

import uuid
from typing import Any

from aibridge.confirm import ConfirmationGuard, get_confirmation_guard
from aibridge.dedupe import EventDedupeStore
from aibridge.schemas import (
    ChannelAction,
    ChannelActionRequest,
    ChannelSuccessResponse,
    ChannelTurnRequest,
)


def _new_request_id() -> str:
    return str(uuid.uuid4())


def build_success(
    *,
    request_id: str | None = None,
    session_id: str | None = None,
    state: str = "interviewing",
    reply_text: str = "Acknowledged.",
    actions: list[dict[str, str]] | None = None,
    outcome: str | None = None,
    draft_id: str | None = None,
    continuation_url: str | None = None,
) -> ChannelSuccessResponse:
    """Bounded OAS envelope."""
    action_models = [
        ChannelAction.model_validate(a) for a in (actions or [])
    ]
    return ChannelSuccessResponse(
        request_id=request_id or _new_request_id(),
        session_id=session_id or f"sess_{uuid.uuid4().hex[:16]}",
        state=state,
        reply_text=reply_text,
        actions=action_models,
        outcome=outcome,
        draft_id=draft_id,
        continuation_url=continuation_url,
    )


# Back-compat alias for story 01 tests.
build_stub_success = build_success


def process_turn(
    body: ChannelTurnRequest,
    store: EventDedupeStore,
    *,
    guard: ConfirmationGuard | None = None,
) -> tuple[dict[str, Any], bool]:
    """Process turn with dedupe. Returns (response_dict, is_new_side_effect)."""
    g = guard or get_confirmation_guard()

    def _side_effect() -> dict[str, Any]:
        sess = g.get_or_create_session(
            user_id=body.principal.user_id,
            chat_id=body.principal.chat_id,
        )
        return build_success(
            session_id=sess.session_id,
            state=sess.state.value,
            reply_text=f"Received: {body.message.text[:200]}",
        ).model_dump()

    return store.get_or_create(body.channel, body.event_id, _side_effect)


def process_action(
    body: ChannelActionRequest,
    store: EventDedupeStore,
    *,
    guard: ConfirmationGuard | None = None,
) -> tuple[dict[str, Any] | None, bool, dict[str, Any] | None]:
    """Process action with dedupe + confirmation guard.

    Returns (success_body | None, is_new, error_info | None).
    error_info: {http_status, code, message} when fail-closed.
    """
    g = guard or get_confirmation_guard()

    def _side_effect() -> dict[str, Any]:
        result = g.consume_action_token(
            body.action_token,
            user_id=body.principal.user_id,
            chat_id=body.principal.chat_id,
        )
        if not result.get("ok"):
            # Signal failure via special marker — process_action unwraps.
            return {"__error__": result}
        return build_success(
            session_id=str(result["session_id"]),
            state=str(result["state"]),
            reply_text=str(result["reply_text"]),
            actions=list(result.get("actions") or []),
            outcome=result.get("outcome"),
            draft_id=result.get("draft_id"),
            continuation_url=result.get("continuation_url"),
        ).model_dump()

    body_out, created = store.get_or_create(body.channel, body.event_id, _side_effect)
    if isinstance(body_out, dict) and "__error__" in body_out:
        err = body_out["__error__"]
        return None, created, {
            "http_status": int(err["http_status"]),
            "code": str(err["code"]),
            "message": str(err["message"]),
        }
    return body_out, created, None
