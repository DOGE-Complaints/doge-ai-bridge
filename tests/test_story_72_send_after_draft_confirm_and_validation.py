"""STORY-AIBRIDGE-72 — Send after draft confirm + validation (post-confirm chain).

Harness: Confirm → Send only after validate; Confirm alone never Send without FC;
fail/no-FC → CONTINUE/Edit; free-text send ≠ stash; FC before confirm blocked.
No invent live TG / Railway SUCCESS · no new TokenActionKind · Keep REQ-11.
"""

from __future__ import annotations

import json

import pytest

from aibridge.action_tokens import TokenActionKind
from aibridge.channel import process_action, process_turn
from aibridge.confirm import ConfirmationGuard, ConfirmSession
from aibridge.confirm_fsm import SessionState
from aibridge.coordinator import ToolValidationError, ValidationContext, validate_function_calls
from aibridge.dedupe import EventDedupeStore
from aibridge.gateway import (
    GatewayExecutor,
    RawHttpResponse,
    RecordingGatewayTransport,
)
from aibridge.interview import InterviewEngine
from aibridge.request_assembly import ServerConstants
from aibridge.responses_client import RecordingResponsesClient
from aibridge.schemas import ChannelActionRequest, ChannelTurnRequest

PACK_SCHEMA = {
    "type": "object",
    "properties": {"title": {"type": "string"}},
    "required": ["title"],
    "additionalProperties": False,
}
TOOL_PARAMS = {
    "type": "object",
    "additionalProperties": False,
    "required": ["narrative", "schema_binding"],
    "properties": {
        "narrative": {"type": "object", "additionalProperties": True},
        "schema_binding": {
            "type": "object",
            "additionalProperties": False,
            "required": ["structured_payload"],
            "properties": {
                "structured_payload": {"type": "object", "additionalProperties": True},
            },
        },
    },
}
WIRE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "narrative", "schema_binding", "origin"],
    "properties": {
        "schema_version": {"type": "string"},
        "narrative": {"type": "object", "additionalProperties": True},
        "schema_binding": {
            "type": "object",
            "additionalProperties": False,
            "required": ["schema_id", "schema_version", "structured_payload"],
            "properties": {
                "schema_id": {"type": "string"},
                "schema_version": {"type": "string"},
                "structured_payload": PACK_SCHEMA,
            },
        },
        "origin": {
            "type": "object",
            "additionalProperties": False,
            "required": ["source"],
            "properties": {"source": {"type": "string"}},
        },
    },
}


def _validation() -> ValidationContext:
    return ValidationContext(
        tool_parameters=TOOL_PARAMS,
        pack_schema=PACK_SCHEMA,
        wire_schema=WIRE_SCHEMA,
        constants=ServerConstants(schema_id="pack-72", schema_version_pack="v1"),
    )


def _good_args() -> dict:
    return {
        "narrative": {"note": "n72"},
        "schema_binding": {"structured_payload": {"title": "ok72"}},
    }


def _ok_201(draft_id: str = "draft-72") -> RawHttpResponse:
    body = json.dumps({"data": {"draft_id": draft_id}, "trace_id": "t72"}).encode()
    return RawHttpResponse(status_code=201, body=body)


def _fc_payload(*, call_id: str = "call_72") -> dict:
    return {
        "id": "resp_fc72",
        "output": [
            {
                "type": "function_call",
                "call_id": call_id,
                "name": "postStoryDraftStash",
                "arguments": json.dumps(_good_args()),
            },
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": "Ready to send."}],
            },
        ],
        "usage": {"input_tokens": 5, "output_tokens": 3},
    }


def _plain_payload(text: str = "Tell me more about the draft.") -> dict:
    return {
        "id": "resp_plain72",
        "output": [
            {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": text}],
            }
        ],
        "usage": {"input_tokens": 2, "output_tokens": 2},
    }


def _guard_with_engine(
    scripted: list[dict],
) -> tuple[ConfirmationGuard, RecordingGatewayTransport, InterviewEngine]:
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw-72",
        channel_bearer="ch-72",
        transport=transport,
        redirect_base="https://spa.example.invalid",
    )
    engine = InterviewEngine(client=RecordingResponsesClient(scripted=scripted))
    guard = ConfirmationGuard(
        executor=executor,
        interview_engine=engine,
        validation_context=_validation(),
    )
    return guard, transport, engine


def _confirm_action(
    g: ConfirmationGuard,
    *,
    user_id: str,
    chat_id: str,
    event_id: str,
    engine: InterviewEngine | None = None,
) -> tuple[dict, ConfirmSession]:
    sess = g.get_or_create_session(user_id=user_id, chat_id=chat_id)
    acts = g.offer_interpretation_confirm(sess.session_id)
    tok = next(a["token"] for a in acts if a["style"] == "success")
    body = ChannelActionRequest.model_validate(
        {
            "channel": "telegram",
            "event_id": event_id,
            "callback_query_id": f"cb-{event_id}",
            "principal": {"user_id": user_id, "chat_id": chat_id},
            "action_token": tok,
        }
    )
    out, _, err = process_action(
        body,
        EventDedupeStore(),
        guard=g,
        interview_engine=engine if engine is not None else g.interview_engine,
    )
    assert err is None
    assert out is not None
    return out, sess


# --- AC-72-02 success: Confirm → validate → Send on same /actions ---


def test_t05_confirm_then_send_after_validate_same_actions() -> None:
    g, transport, engine = _guard_with_engine([_fc_payload()])
    out, sess = _confirm_action(
        g, user_id="7201", chat_id="7201", event_id="e72-ok", engine=engine
    )
    kinds = {g.tokens.lookup(a["token"]).action for a in out["actions"]}
    assert TokenActionKind.CONFIRM_SEND in kinds
    assert sess.state is SessionState.AWAITING_SEND_CONFIRM
    assert sess.frozen_tool_intent is not None
    assert sess.gateway_authorized is False
    assert transport.calls == []  # stash only after Send consume


# --- AC-72-01 / AC-72-04 fail/no-FC: CONTINUE/Edit · no Send · no gateway ---


def test_t05_confirm_nofc_offers_continue_no_send() -> None:
    g, transport, engine = _guard_with_engine([_plain_payload()])
    out, sess = _confirm_action(
        g, user_id="7202", chat_id="7202", event_id="e72-nofc", engine=engine
    )
    kinds = {g.tokens.lookup(a["token"]).action for a in out["actions"]}
    assert TokenActionKind.CONTINUE in kinds
    assert TokenActionKind.EDIT in kinds
    assert TokenActionKind.CONFIRM_SEND not in kinds
    assert sess.gateway_authorized is False
    assert transport.calls == []


def test_t05_confirm_without_engine_continue_no_send() -> None:
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw-72",
        channel_bearer="ch-72",
        transport=transport,
    )
    g = ConfirmationGuard(executor=executor, validation_context=_validation())
    out, sess = _confirm_action(
        g, user_id="7203", chat_id="7203", event_id="e72-noeng", engine=None
    )
    kinds = {g.tokens.lookup(a["token"]).action for a in out["actions"]}
    assert TokenActionKind.CONTINUE in kinds
    assert TokenActionKind.CONFIRM_SEND not in kinds
    assert sess.gateway_authorized is False
    assert transport.calls == []


# --- consume alone Keep: no gateway · actions=[] · flag for chain ---


def test_t05_consume_alone_never_gateway_or_send() -> None:
    g, transport, _ = _guard_with_engine([_fc_payload()])
    sess = g.get_or_create_session(user_id="7204", chat_id="7204")
    acts = g.offer_interpretation_confirm(sess.session_id)
    tok = next(a["token"] for a in acts if a["style"] == "success")
    result = g.consume_action_token(tok, user_id="7204", chat_id="7204")
    assert result["ok"] is True
    assert result["gateway_authorized"] is False
    assert result["actions"] == []
    assert result.get("post_confirm_engine") is True
    assert transport.calls == []


# --- AC-72-01 FC before confirm blocked ---


def test_t05_fc_before_confirm_blocked() -> None:
    with pytest.raises(ToolValidationError, match="interpretation"):
        validate_function_calls(
            [
                {
                    "call_id": "early",
                    "name": "postStoryDraftStash",
                    "arguments": json.dumps(_good_args()),
                }
            ],
            session_state=SessionState.AWAITING_INTERPRETATION_CONFIRM,
            validation=_validation(),
        )


# --- AC-72-03 free-text send ≠ mint Send / stash ---


def test_t05_freetext_send_verb_does_not_stash() -> None:
    g, transport, engine = _guard_with_engine([_plain_payload("отправляй сейчас")])
    sess = g.get_or_create_session(user_id="7205", chat_id="7205")
    # Still interviewing — no interpret confirm yet.
    body = ChannelTurnRequest.model_validate(
        {
            "channel": "telegram",
            "event_id": "e72-ft",
            "principal": {"user_id": "7205", "chat_id": "7205"},
            "message": {"message_id": "1", "text": "отправляй"},
        }
    )
    out, _ = process_turn(
        body, EventDedupeStore(), guard=g, interview_engine=engine
    )
    kinds = {
        g.tokens.lookup(a["token"]).action for a in out.get("actions") or []
    }
    assert TokenActionKind.CONFIRM_SEND not in kinds
    assert transport.calls == []
    assert sess.gateway_authorized is False


# --- AC-72-04 stash only via Send consume after post-confirm ---


def test_t05_stash_only_via_send_after_post_confirm() -> None:
    g, transport, engine = _guard_with_engine([_fc_payload(call_id="call_72s")])
    out, sess = _confirm_action(
        g, user_id="7206", chat_id="7206", event_id="e72-send", engine=engine
    )
    send_tok = next(
        a["token"]
        for a in out["actions"]
        if g.tokens.lookup(a["token"]).action is TokenActionKind.CONFIRM_SEND
    )
    assert transport.calls == []
    result = g.consume_action_token(send_tok, user_id="7206", chat_id="7206")
    assert result["ok"] is True
    assert len(transport.calls) == 1
    assert result.get("continuation_url") or sess.continuation_url
