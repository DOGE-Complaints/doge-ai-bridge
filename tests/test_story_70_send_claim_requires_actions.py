"""STORY-AIBRIDGE-70 — Send-claim requires in-chat actions (remint CTAs).

Honesty: no invent stash · no NL rewrite · Keep REQ-11 · no invent live TG/Railway.
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
from aibridge.seam_policy import (
    SEND_CLAIM_MARKERS,
    needs_control_surface,
    reply_claims_send_control,
    reply_claims_vague_interface,
)

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

# Transcript-shaped claim (2026-11-09 Pille) — markdown emphasis around Send.
TRANSCRIPT_SEND_CLAIM = (
    "Если формулировка верна, можно переходить к отправке через "
    "доступное в чате действие **Send**."
)


def _validation() -> ValidationContext:
    return ValidationContext(
        tool_parameters=TOOL_PARAMS,
        pack_schema=PACK_SCHEMA,
        wire_schema=WIRE_SCHEMA,
        constants=ServerConstants(schema_id="pack-70", schema_version_pack="v1"),
    )


def _good_args() -> dict:
    return {
        "narrative": {"note": "n70"},
        "schema_binding": {"structured_payload": {"title": "ok70"}},
    }


def _ok_201(draft_id: str = "draft-70") -> RawHttpResponse:
    body = json.dumps({"data": {"draft_id": draft_id}, "trace_id": "t70"}).encode()
    return RawHttpResponse(status_code=201, body=body)


def _guard_recording() -> tuple[ConfirmationGuard, RecordingGatewayTransport]:
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw-70",
        channel_bearer="ch-70",
        transport=transport,
        redirect_base="https://spa.example.invalid",
    )
    return (
        ConfirmationGuard(executor=executor, validation_context=_validation()),
        transport,
    )


# --- t01 marker lock ---


def test_t01_send_claim_markers_lock_and_false_positive_fence() -> None:
    assert "действие send" in SEND_CLAIM_MARKERS
    assert reply_claims_send_control(TRANSCRIPT_SEND_CLAIM)
    assert reply_claims_send_control("Please use the action Send now.")
    assert reply_claims_send_control("Press the Send button when ready.")
    # False-positive fence: bare «отправка» / «отправ» without naming Send control
    assert not reply_claims_send_control("расскажите про отправку жалобы")
    assert not reply_claims_send_control("можно переходить к отправке черновика")
    assert not reply_claims_vague_interface(TRANSCRIPT_SEND_CLAIM)


# --- t02 gate ---


def test_t02_needs_control_surface_send_claim_and_url_exempt() -> None:
    assert needs_control_surface(
        reply_text=TRANSCRIPT_SEND_CLAIM,
        actions=[],
        continuation_url=None,
    )
    assert not needs_control_surface(
        reply_text=TRANSCRIPT_SEND_CLAIM,
        actions=[{"label": "Looks right", "token": "x", "style": "success"}],
        continuation_url=None,
    )
    assert not needs_control_surface(
        reply_text=TRANSCRIPT_SEND_CLAIM,
        actions=[],
        continuation_url="https://spa.example/#/story/submit?draft_id=d",
    )
    # vague Keep still
    assert needs_control_surface(
        reply_text="используйте интерфейс",
        actions=[],
        continuation_url=None,
    )


# --- t03 remint interpret ---


def test_t03_awaiting_interpret_send_claim_remints_interpretation() -> None:
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="u70i", chat_id="c70i")
    g.offer_interpretation_confirm(sess.session_id)
    assert sess.state is SessionState.AWAITING_INTERPRETATION_CONFIRM
    out = build_turn_from_engine(
        g,
        sess,
        {
            "ok": True,
            "reply_text": TRANSCRIPT_SEND_CLAIM,
            "function_calls": [],
        },
    )
    assert out["actions"], "Send-claim must remint CTAs"
    # reply_text unchanged — no NL rewrite
    assert out["reply_text"] == TRANSCRIPT_SEND_CLAIM
    kinds = {g.tokens.lookup(a["token"]).action for a in out["actions"]}
    assert TokenActionKind.CONFIRM_INTERPRETATION in kinds
    assert TokenActionKind.CONFIRM_SEND not in kinds  # no invent Send without freeze
    assert transport.calls == []
    assert sess.state is SessionState.AWAITING_INTERPRETATION_CONFIRM


# --- t03 remint send-ready ---


def test_t03_awaiting_send_claim_remints_send_confirm() -> None:
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="u70s", chat_id="c70s")
    acts = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in acts if a["style"] == "success"),
        user_id="u70s",
        chat_id="c70s",
    )
    out = build_turn_from_engine(
        g,
        sess,
        {
            "ok": True,
            "reply_text": "Ready.",
            "function_calls": [
                {
                    "call_id": "call_70",
                    "name": "postStoryDraftStash",
                    "arguments": json.dumps(_good_args()),
                }
            ],
            "replay_items": [],
        },
    )
    assert out["state"] == SessionState.AWAITING_SEND_CONFIRM.value
    # Second engine turn with Send-claim + empty would remint — simulate empty via ensure path:
    # already have actions from first turn; force ensure by rebuilding with claim after clearing
    # by calling build_turn again while awaiting (FC-less + claim).
    out2 = build_turn_from_engine(
        g,
        sess,
        {
            "ok": True,
            "reply_text": TRANSCRIPT_SEND_CLAIM,
            "function_calls": [],
        },
    )
    assert out2["actions"]
    kinds = {g.tokens.lookup(a["token"]).action for a in out2["actions"]}
    assert TokenActionKind.CONFIRM_SEND in kinds
    assert transport.calls == []  # remint ≠ stash


# --- t04 / t05 FC-less seam remint when claim + would-be empty ---


def test_t05_interpretation_confirmed_send_claim_gets_continue_seam() -> None:
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="u70c", chat_id="c70c")
    acts = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in acts if a["style"] == "success"),
        user_id="u70c",
        chat_id="c70c",
    )
    out = build_turn_from_engine(
        g,
        sess,
        {
            "ok": True,
            "reply_text": TRANSCRIPT_SEND_CLAIM,
            "function_calls": [],
        },
    )
    kinds = {g.tokens.lookup(a["token"]).action for a in out["actions"]}
    assert TokenActionKind.CONTINUE in kinds
    assert TokenActionKind.CONFIRM_SEND not in kinds
    assert transport.calls == []


# --- AC-70-04 Keep stash only via Send consume ---


def test_t05_no_stash_invent_on_send_claim_remint() -> None:
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="u70k", chat_id="c70k")
    g.offer_interpretation_confirm(sess.session_id)
    out = build_turn_from_engine(
        g,
        sess,
        {
            "ok": True,
            "reply_text": TRANSCRIPT_SEND_CLAIM,
            "function_calls": [],
        },
    )
    assert transport.calls == []
    assert sess.gateway_authorized is False
    assert sess.continuation_url is None
    assert all(
        g.tokens.lookup(a["token"]).action is not TokenActionKind.CONFIRM_SEND
        for a in out["actions"]
    )
