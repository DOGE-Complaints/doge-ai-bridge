"""STORY-AIBRIDGE-71 — awaiting interpretation always has Confirm/Edit actions.

Honesty: no invent Send/stash · no NL rewrite · Keep REQ-11 · 68/70 regression ·
no invent live TG/Railway · STORY-72 / GPT ROL-07 OOS.
"""

from __future__ import annotations

import json

from aibridge.action_tokens import TokenActionKind
from aibridge.confirm import ConfirmationGuard
from aibridge.confirm_fsm import SessionState
from aibridge.coordinator import ValidationContext, build_turn_from_engine
from aibridge.gateway import (
    GatewayExecutor,
    RawHttpResponse,
    RecordingGatewayTransport,
)
from aibridge.request_assembly import ServerConstants
from aibridge.seam_policy import needs_control_surface, reply_claims_send_control

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

# Ordinary free-text — no Send-claim / vague-interface markers (live residual shape).
PLAIN_REPLY = "Спасибо, уточнил формулировку черновика. Жду вашего решения."


def _validation() -> ValidationContext:
    return ValidationContext(
        tool_parameters=TOOL_PARAMS,
        pack_schema=PACK_SCHEMA,
        wire_schema=WIRE_SCHEMA,
        constants=ServerConstants(schema_id="pack-71", schema_version_pack="v1"),
    )


def _ok_201(draft_id: str = "draft-71") -> RawHttpResponse:
    body = json.dumps({"data": {"draft_id": draft_id}, "trace_id": "t71"}).encode()
    return RawHttpResponse(status_code=201, body=body)


def _guard_recording() -> tuple[ConfirmationGuard, RecordingGatewayTransport]:
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw-71",
        channel_bearer="ch-71",
        transport=transport,
        redirect_base="https://spa.example.invalid",
    )
    return (
        ConfirmationGuard(executor=executor, validation_context=_validation()),
        transport,
    )


def test_t05_awaiting_plain_reply_no_markers_remints_confirm_edit() -> None:
    """AC-71-01…03 — state-invariant remint without Send-claim markers."""
    assert not reply_claims_send_control(PLAIN_REPLY)
    assert not needs_control_surface(
        reply_text=PLAIN_REPLY,
        actions=[],
        continuation_url=None,
    )

    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="u71", chat_id="c71")
    g.offer_interpretation_confirm(sess.session_id)
    assert sess.state is SessionState.AWAITING_INTERPRETATION_CONFIRM

    out = build_turn_from_engine(
        g,
        sess,
        {
            "ok": True,
            "reply_text": PLAIN_REPLY,
            "function_calls": [],
        },
    )
    assert out["actions"], "awaiting interpret + empty must remint Confirm/Edit"
    assert out["reply_text"] == PLAIN_REPLY  # no NL rewrite
    kinds = {g.tokens.lookup(a["token"]).action for a in out["actions"]}
    assert TokenActionKind.CONFIRM_INTERPRETATION in kinds
    assert TokenActionKind.EDIT in kinds
    assert TokenActionKind.CANCEL in kinds
    assert TokenActionKind.CONFIRM_SEND not in kinds  # no invent Send
    assert transport.calls == []
    assert sess.gateway_authorized is False
    assert sess.continuation_url is None
    assert sess.state is SessionState.AWAITING_INTERPRETATION_CONFIRM


def test_t05_ok_false_path_also_remints_when_awaiting_interpret() -> None:
    """All build_turn exits hit ensure — ok=False path covered (AC-71-01 / t04)."""
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="u71f", chat_id="c71f")
    g.offer_interpretation_confirm(sess.session_id)
    out = build_turn_from_engine(
        g,
        sess,
        {
            "ok": False,
            "message": "Turn rejected quietly.",
            "function_calls": [],
        },
    )
    assert out["actions"]
    kinds = {g.tokens.lookup(a["token"]).action for a in out["actions"]}
    assert TokenActionKind.CONFIRM_INTERPRETATION in kinds
    assert TokenActionKind.CONFIRM_SEND not in kinds
    assert transport.calls == []
