"""STORY-AIBRIDGE-56 — Keep pipe: dual-confirm + stash + SPA verify harness.

Re-verifies Present pipe (AC-AIB-11-01/03/04/05/06). Does not rewrite FSM/gateway API.
OOS: L11-1 seam (57), stub/live evidence gates (58).
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from aibridge.action_tokens import TokenActionKind
from aibridge.confirm import ConfirmationGuard
from aibridge.confirm_fsm import IllegalTransitionError, SessionState
from aibridge.gateway import (
    STASH_PATH,
    STASH_REPLY,
    GatewayExecutor,
    GatewayOutcome,
    RecordingGatewayTransport,
    RawHttpResponse,
    build_continuation_url,
)

_REPO = Path(__file__).resolve().parents[1]
_SRC = _REPO / "src" / "aibridge"


def _ok_201(draft_id: str = "draft-56", trace_id: str = "trace-56") -> RawHttpResponse:
    body = json.dumps({"data": {"draft_id": draft_id}, "trace_id": trace_id}).encode()
    return RawHttpResponse(status_code=201, body=body)


def _guard(
    *,
    scripted: list[RawHttpResponse] | None = None,
    raise_on_call: Exception | None = None,
    gateway_bearer: str = "gw-secret-56",
    channel_bearer: str = "ch-secret-56",
    redirect_base: str = "https://spa.example",
    origin: str = "https://gateway.example.invalid",
) -> tuple[ConfirmationGuard, RecordingGatewayTransport]:
    transport = RecordingGatewayTransport(scripted=list(scripted or [_ok_201()]))
    if raise_on_call is not None:
        transport.raise_on_call = raise_on_call
    executor = GatewayExecutor(
        origin=origin,
        gateway_bearer=gateway_bearer,
        channel_bearer=channel_bearer,
        redirect_base=redirect_base,
        transport=transport,
    )
    return ConfirmationGuard(executor=executor), transport


def _full_send(g: ConfirmationGuard) -> dict:
    sess = g.get_or_create_session(user_id="u56", chat_id="c56")
    interpret = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id="u56",
        chat_id="c56",
    )
    g.set_frozen_tool_intent(
        sess.session_id,
        {"arguments": {"title": "keep-pipe"}},
        draft_hash="hash-56",
    )
    send_actions = g.offer_send_confirm(sess.session_id)
    send_tok = next(a["token"] for a in send_actions if a["style"] == "primary")
    return g.consume_action_token(send_tok, user_id="u56", chat_id="c56")


# --- t01 AC-AIB-11-01 dual-confirm stages ---


def test_t01_interpretation_confirm_never_authorizes_gateway() -> None:
    g, transport = _guard()
    sess = g.get_or_create_session(user_id="u56", chat_id="c56")
    interpret = g.offer_interpretation_confirm(sess.session_id)
    assert sess.state is SessionState.AWAITING_INTERPRETATION_CONFIRM
    kinds = {TokenActionKind.CONFIRM_INTERPRETATION, TokenActionKind.EDIT, TokenActionKind.CANCEL}
    # Bundle is interpretation-stage — no CONFIRM_SEND in offer.
    result = g.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id="u56",
        chat_id="c56",
    )
    assert result["ok"] is True
    assert sess.state is SessionState.INTERPRETATION_CONFIRMED
    assert sess.gateway_authorized is False
    assert transport.calls == []
    assert result.get("outcome") in (None, "")
    assert result.get("continuation_url") in (None, "")
    # Send offer still requires frozen intent after interpretation.
    with pytest.raises(IllegalTransitionError):
        g.offer_send_confirm(sess.session_id)
    _ = kinds  # kinds documented for harness readers


def test_t01_send_offer_distinct_from_interpretation() -> None:
    g, _t = _guard()
    sess = g.get_or_create_session(user_id="u56", chat_id="c56")
    interpret = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id="u56",
        chat_id="c56",
    )
    g.set_frozen_tool_intent(sess.session_id, {"a": 1}, draft_hash="h1")
    send_actions = g.offer_send_confirm(sess.session_id)
    assert sess.state is SessionState.AWAITING_SEND_CONFIRM
    labels = {a["label"] for a in send_actions}
    assert "Send to DOGEstonia" in labels
    assert "Looks right" not in labels


# --- t02 ActionToken + revision/draft_hash reuse ---


def test_t02_send_token_binds_revision_and_draft_hash() -> None:
    g, _t = _guard()
    sess = g.get_or_create_session(user_id="u56", chat_id="c56")
    interpret = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id="u56",
        chat_id="c56",
    )
    g.set_frozen_tool_intent(sess.session_id, {"a": 1}, draft_hash="hash-bind")
    rev = sess.revision
    send_actions = g.offer_send_confirm(sess.session_id)
    send_tok = next(a["token"] for a in send_actions if a["style"] == "primary")
    rec = g.tokens.verify_for_consume(send_tok, user_id="u56", chat_id="c56")
    assert rec.action is TokenActionKind.CONFIRM_SEND
    assert rec.revision == rev
    assert rec.draft_hash == "hash-bind"
    # Edit bumps revision and invalidates prior tokens (reuse store — no parallel schema).
    g.apply_edit(sess.session_id)
    assert sess.revision == rev + 1
    with pytest.raises(Exception):
        g.tokens.verify_for_consume(send_tok, user_id="u56", chat_id="c56")


# --- t03 tool-intent freeze ≠ gateway permission ---


def test_t03_frozen_intent_alone_does_not_stash() -> None:
    g, transport = _guard()
    sess = g.get_or_create_session(user_id="u56", chat_id="c56")
    interpret = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id="u56",
        chat_id="c56",
    )
    g.set_frozen_tool_intent(sess.session_id, {"arguments": {"x": 1}})
    assert g.authorize_from_tool_intent_alone(sess.frozen_tool_intent or {}) is False
    assert sess.gateway_authorized is False
    with pytest.raises(RuntimeError, match="gateway not authorized"):
        g.call_gateway(sess, body={"x": 1})
    assert transport.calls == []
    # Direct executor also blocked without Send authorization.
    assert (
        g.executor.execute_stash({"x": 1}, gateway_authorized=False).outcome
        is GatewayOutcome.BLOCKED_BY_CONFIRMATION
    )


# --- t04 AC-AIB-11-03 config URL + Bearer ---


def test_t04_submit_url_and_bearer_from_config_only() -> None:
    g, transport = _guard(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw-only-56",
        channel_bearer="ch-only-56",
    )
    result = _full_send(g)
    assert result["ok"] is True
    assert result["outcome"] == GatewayOutcome.STASHED.value
    assert len(transport.calls) == 1
    call = transport.calls[0]
    assert call["url"] == f"https://gateway.example.invalid{STASH_PATH}"
    assert call["headers"]["Authorization"] == "Bearer gw-only-56"
    assert "ch-only-56" not in call["headers"]["Authorization"]


def test_t04_fail_closed_without_gateway_token() -> None:
    """Present Keep: empty bearer raises before HTTP (fail-closed; no rewrite)."""
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    ex = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="",
        channel_bearer="ch",
        transport=transport,
        redirect_base="https://spa.example",
    )
    with pytest.raises(ValueError, match="GATEWAY_SERVICE_API_TOKEN"):
        ex.authorization_header()
    with pytest.raises(ValueError, match="GATEWAY_SERVICE_API_TOKEN"):
        ex.execute_stash({"a": 1}, gateway_authorized=True)
    assert transport.calls == []


# --- t05 AC-AIB-11-04 factual stash success ---


def test_t05_user_visible_success_only_after_factual_stash() -> None:
    g, _t = _guard()
    result = _full_send(g)
    assert result["outcome"] == GatewayOutcome.STASHED.value
    assert result["reply_text"] == STASH_REPLY
    assert "not a published Story" in result["reply_text"]
    assert result["draft_id"] == "draft-56"


def test_t05_clear_failure_no_continuation() -> None:
    bad = RawHttpResponse(status_code=400, body=b'{"error":"bad"}')
    g, transport = _guard(scripted=[bad])
    result = _full_send(g)
    assert result["outcome"] == GatewayOutcome.VALIDATION_ERROR.value
    assert result["continuation_url"] is None
    assert result["draft_id"] is None
    assert len(transport.calls) == 1


def test_t05_unknown_outcome_blocks_blind_resend() -> None:
    g, transport = _guard(raise_on_call=TimeoutError("timeout"))
    result = _full_send(g)
    assert result["outcome"] == GatewayOutcome.UNKNOWN_OUTCOME.value
    assert len(transport.calls) == 1
    sess = g.get_session(result["session_id"])
    assert sess is not None
    assert g.send_blocked_for_revision(sess) is True
    with pytest.raises(IllegalTransitionError):
        sess.state = SessionState.INTERPRETATION_CONFIRMED
        g.set_frozen_tool_intent(sess.session_id, {"a": 1})
        g.offer_send_confirm(sess.session_id)


# --- t06 AC-AIB-11-05 continuation SPA hash ---


def test_t06_continuation_present_shape_only_when_stashed() -> None:
    expected = build_continuation_url(
        redirect_base="https://spa.example", draft_id="draft-56"
    )
    assert expected == "https://spa.example/#/story/submit?draft_id=draft-56"
    g, _t = _guard(redirect_base="https://spa.example")
    result = _full_send(g)
    assert result["continuation_url"] == expected
    assert "Story published" not in result["reply_text"]


def test_t06_no_continuation_without_stash() -> None:
    g, _t = _guard(
        scripted=[RawHttpResponse(status_code=500, body=b"err")],
        redirect_base="https://spa.example",
    )
    result = _full_send(g)
    assert result["outcome"] == GatewayOutcome.TRANSIENT_FAILURE.value
    assert result["continuation_url"] is None


# --- t07 AC-AIB-11-06 bridge owns stash / channel boundary ---


def test_t07_channel_module_has_no_gateway_stash_client() -> None:
    """channel.py / app channel routes must not own gateway Bearer or stash client."""
    forbidden = {
        "GATEWAY_SERVICE_API_TOKEN",
        "gateway_service_api_token",
        "execute_stash",
        "GatewayExecutor",
        "STASH_PATH",
    }
    channel_src = (_SRC / "channel.py").read_text(encoding="utf-8")
    tree = ast.parse(channel_src)
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            names.add(node.value)
    assert not (forbidden & names), f"channel leaked {forbidden & names}"
    assert "GATEWAY_SERVICE_API_TOKEN" not in channel_src
    assert "execute_stash" not in channel_src


def test_t07_runtime_note_present() -> None:
    note = _REPO / "docs" / "runtime-docs" / "04-confirm-gateway-keep-pipe.md"
    assert note.is_file()
    text = note.read_text(encoding="utf-8")
    assert "AC-AIB-11-01" in text
    assert "Keep" in text
    assert "GatewayExecutor" in text


# --- gate surface ---


def test_story_56_keep_pipe_gate_docs_linked() -> None:
    arch = _REPO / "docs" / "architecture" / "req15-dual-confirm-handoff" / "01-keep-pipe-boundaries.md"
    assert arch.is_file()
    runtime_keep = _REPO / "docs" / "architecture" / "runtime" / "03-confirm-gateway.md"
    assert runtime_keep.is_file()
