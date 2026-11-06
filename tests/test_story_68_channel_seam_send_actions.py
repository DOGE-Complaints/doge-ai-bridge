"""STORY-AIBRIDGE-68 — channel seam CTAs + Send always + CONTINUE ≠ stash.

Harness (t07): seam actions Present; send-ready CTAs; stash Keep via CONFIRM_SEND only;
vague «интерфейс» without control is rejected/enforced; no live TG / Railway invent.
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
    SeamKind,
    classify_fcless_seam,
    needs_control_surface,
    reply_claims_vague_interface,
    requires_fcless_actions,
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


def _validation() -> ValidationContext:
    return ValidationContext(
        tool_parameters=TOOL_PARAMS,
        pack_schema=PACK_SCHEMA,
        wire_schema=WIRE_SCHEMA,
        constants=ServerConstants(schema_id="pack-68", schema_version_pack="v1"),
    )


def _good_args() -> dict:
    return {
        "narrative": {"note": "n68"},
        "schema_binding": {"structured_payload": {"title": "ok68"}},
    }


def _ok_201(draft_id: str = "draft-68") -> RawHttpResponse:
    body = json.dumps({"data": {"draft_id": draft_id}, "trace_id": "t68"}).encode()
    return RawHttpResponse(status_code=201, body=body)


def _guard_recording() -> tuple[ConfirmationGuard, RecordingGatewayTransport]:
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw-68",
        channel_bearer="ch-68",
        transport=transport,
        redirect_base="https://spa.example.invalid",
    )
    return (
        ConfirmationGuard(executor=executor, validation_context=_validation()),
        transport,
    )


# --- t01 seam policy ---


def test_t01_seam_policy_matrix() -> None:
    assert classify_fcless_seam(SessionState.INTERVIEWING) is SeamKind.INTERPRETATION
    assert (
        classify_fcless_seam(SessionState.INTERPRETATION_CONFIRMED)
        is SeamKind.CONTINUE_EDIT
    )
    assert requires_fcless_actions(SessionState.INTERPRETATION_CONFIRMED)
    assert not requires_fcless_actions(SessionState.AWAITING_SEND_CONFIRM)
    assert reply_claims_vague_interface("подайте в интерфейсе DOGEstonia")
    assert needs_control_surface(
        reply_text="используйте интерфейс",
        actions=[],
        continuation_url=None,
    )
    assert not needs_control_surface(
        reply_text="используйте интерфейс",
        actions=[{"label": "Continue", "token": "x", "style": "primary"}],
        continuation_url=None,
    )
    assert not needs_control_surface(
        reply_text="в интерфейсе",
        actions=[],
        continuation_url="https://spa.example/#/story/submit?draft_id=d",
    )


# --- t02 CONTINUE kind ---


def test_t02_continue_token_mint_and_store() -> None:
    g, _ = _guard_recording()
    sess = g.get_or_create_session(user_id="u68", chat_id="c68")
    # Reach interpretation_confirmed without CONTINUE overload.
    acts = g.offer_interpretation_confirm(sess.session_id)
    tok = next(a["token"] for a in acts if a["style"] == "success")
    g.consume_action_token(tok, user_id="u68", chat_id="c68")
    assert sess.state is SessionState.INTERPRETATION_CONFIRMED

    seam = g.offer_continue_seam(sess.session_id)
    assert len(seam) == 2
    kinds = {g.tokens.lookup(a["token"]).action for a in seam}
    assert TokenActionKind.CONTINUE in kinds
    assert TokenActionKind.EDIT in kinds
    assert TokenActionKind.CONFIRM_INTERPRETATION not in kinds
    cont = next(a for a in seam if g.tokens.lookup(a["token"]).action is TokenActionKind.CONTINUE)
    assert cont["label"] == "Continue"
    assert len(cont["token"].encode("utf-8")) <= 64


# --- t03 coordinator emit ---


def test_t03_coordinator_emits_continue_on_confirmed_fcless() -> None:
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="u68e", chat_id="c68e")
    acts = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in acts if a["style"] == "success"),
        user_id="u68e",
        chat_id="c68e",
    )
    out = build_turn_from_engine(
        g,
        sess,
        {"ok": True, "reply_text": "Draft normalized — next?", "function_calls": []},
    )
    assert out["actions"], "non-seamless seam must expose actions"
    kinds = {g.tokens.lookup(a["token"]).action for a in out["actions"]}
    assert TokenActionKind.CONTINUE in kinds
    assert transport.calls == []


# --- t04 CONTINUE consume resume ---


def test_t04_continue_consume_no_stash_no_gateway() -> None:
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="u68c", chat_id="c68c")
    acts = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in acts if a["style"] == "success"),
        user_id="u68c",
        chat_id="c68c",
    )
    seam = g.offer_continue_seam(sess.session_id)
    cont_tok = next(
        a["token"]
        for a in seam
        if g.tokens.lookup(a["token"]).action is TokenActionKind.CONTINUE
    )
    before_inv = sess.gateway_invocations
    result = g.consume_action_token(cont_tok, user_id="u68c", chat_id="c68c")
    assert result["ok"] is True
    assert result["gateway_authorized"] is False
    assert sess.gateway_authorized is False
    assert sess.gateway_invocations == before_inv
    assert sess.continuation_url is None
    assert transport.calls == []
    assert "Continuing" in result["reply_text"]


# --- t05 send-ready always ---


def test_t05_send_ready_always_offer_send_confirm() -> None:
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="u68s", chat_id="c68s")
    acts = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in acts if a["style"] == "success"),
        user_id="u68s",
        chat_id="c68s",
    )
    out = build_turn_from_engine(
        g,
        sess,
        {
            "ok": True,
            "reply_text": "Ready.",
            "function_calls": [
                {
                    "call_id": "call_68",
                    "name": "postStoryDraftStash",
                    "arguments": json.dumps(_good_args()),
                }
            ],
            "replay_items": [],
        },
    )
    assert out["state"] == SessionState.AWAITING_SEND_CONFIRM.value
    assert len(out["actions"]) == 3
    kinds = {g.tokens.lookup(a["token"]).action for a in out["actions"]}
    assert TokenActionKind.CONFIRM_SEND in kinds
    assert transport.calls == []  # stash only after Send consume


# --- t06 ban vague interface ---


def test_t06_vague_interface_without_control_gets_actions() -> None:
    g, _ = _guard_recording()
    sess = g.get_or_create_session(user_id="u68v", chat_id="c68v")
    acts = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in acts if a["style"] == "success"),
        user_id="u68v",
        chat_id="c68v",
    )
    # Force AWAITING path empty + vague claim via error-style ok=False mid INTERPRETATION_CONFIRMED
    # Ordinary path already mints; simulate reply that would have been empty under old code
    # by using engine reject then ensure control surface:
    out = build_turn_from_engine(
        g,
        sess,
        {
            "ok": False,
            "message": "я не могу отправить — используйте действие в интерфейсе DOGEstonia",
            "function_calls": [],
        },
    )
    assert out["actions"], "vague interface claim must not ship without CTAs"
    assert needs_control_surface(
        reply_text=out["reply_text"],
        actions=out["actions"],
        continuation_url=out.get("continuation_url"),
    ) is False


# --- AC-68-04 Keep stash only via Send ---


def test_t07_stash_only_via_send_consume() -> None:
    g, transport = _guard_recording()
    sess = g.get_or_create_session(user_id="u68k", chat_id="c68k")
    acts = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in acts if a["style"] == "success"),
        user_id="u68k",
        chat_id="c68k",
    )
    out = build_turn_from_engine(
        g,
        sess,
        {
            "ok": True,
            "reply_text": "Ready.",
            "function_calls": [
                {
                    "call_id": "call_68k",
                    "name": "postStoryDraftStash",
                    "arguments": json.dumps(_good_args()),
                }
            ],
            "replay_items": [],
        },
    )
    send_tok = next(
        a["token"]
        for a in out["actions"]
        if g.tokens.lookup(a["token"]).action is TokenActionKind.CONFIRM_SEND
    )
    result = g.consume_action_token(send_tok, user_id="u68k", chat_id="c68k")
    assert result["ok"] is True
    assert len(transport.calls) == 1
    assert result.get("continuation_url") or sess.continuation_url


def test_t07_interviewing_still_offers_interpretation_not_continue() -> None:
    g, _ = _guard_recording()
    sess = g.get_or_create_session(user_id="u68i", chat_id="c68i")
    out = build_turn_from_engine(
        g,
        sess,
        {"ok": True, "reply_text": "Tell me more.", "function_calls": []},
    )
    kinds = {g.tokens.lookup(a["token"]).action for a in out["actions"]}
    assert TokenActionKind.CONFIRM_INTERPRETATION in kinds
    assert TokenActionKind.CONTINUE not in kinds
