"""Channel turn/action processing (façade stub — no OpenAI / gateway in story 01)."""

from __future__ import annotations

import uuid
from typing import Any

from aibridge.dedupe import EventDedupeStore
from aibridge.schemas import (
    ChannelActionRequest,
    ChannelSuccessResponse,
    ChannelTurnRequest,
)


def _new_request_id() -> str:
    return str(uuid.uuid4())


def build_stub_success(
    *,
    request_id: str | None = None,
    state: str = "interviewing",
    reply_text: str = "Acknowledged.",
) -> ChannelSuccessResponse:
    """Bounded OAS envelope for story-01 façade without Responses loop."""
    return ChannelSuccessResponse(
        request_id=request_id or _new_request_id(),
        session_id=f"sess_{uuid.uuid4().hex[:16]}",
        state=state,
        reply_text=reply_text,
        actions=[],
        outcome=None,
        draft_id=None,
        continuation_url=None,
    )


def process_turn(
    body: ChannelTurnRequest, store: EventDedupeStore
) -> tuple[dict[str, Any], bool]:
    """Process turn with dedupe. Returns (response_dict, is_new_side_effect)."""

    def _side_effect() -> dict[str, Any]:
        return build_stub_success(
            reply_text=f"Received: {body.message.text[:200]}"
        ).model_dump()

    return store.get_or_create(body.channel, body.event_id, _side_effect)


def process_action(
    body: ChannelActionRequest, store: EventDedupeStore
) -> tuple[dict[str, Any], bool]:
    """Process action with dedupe. Accepts action_token shape only (no FSM)."""

    def _side_effect() -> dict[str, Any]:
        _ = body.action_token
        return build_stub_success(
            state="awaiting_confirm",
            reply_text="Action accepted.",
        ).model_dump()

    return store.get_or_create(body.channel, body.event_id, _side_effect)
