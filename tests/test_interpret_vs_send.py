"""t02 — interpretation ≠ Send; tool intent ≠ permission."""

from __future__ import annotations

from aibridge.confirm import ConfirmationGuard
from aibridge.confirm_fsm import SessionState


def test_interpretation_confirm_no_gateway() -> None:
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="1", chat_id="2")
    actions = g.offer_interpretation_confirm(sess.session_id)
    interpret = next(a for a in actions if a["style"] == "success")
    result = g.consume_action_token(
        interpret["token"], user_id="1", chat_id="2"
    )
    assert result["ok"] is True
    assert result["gateway_authorized"] is False
    assert result["gateway_invocations"] == 0
    assert g.get_session(sess.session_id).gateway_invocations == 0
    assert result["state"] == SessionState.INTERPRETATION_CONFIRMED.value


def test_tool_intent_alone_never_send() -> None:
    g = ConfirmationGuard()
    assert g.authorize_from_tool_intent_alone({"name": "postStoryDraftStash"}) is False
    sess = g.get_or_create_session(user_id="1", chat_id="2")
    g.offer_interpretation_confirm(sess.session_id)
    # Even with frozen intent, without Send token gateway stays unauthorized.
    g.set_frozen_tool_intent(sess.session_id, {"name": "postStoryDraftStash"})
    assert sess.gateway_authorized is False
    try:
        g.call_gateway(sess)
        raise AssertionError("expected RuntimeError")
    except RuntimeError as exc:
        assert "not authorized" in str(exc)


def test_send_token_authorizes_gateway_call_site() -> None:
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="1", chat_id="2")
    interpret_actions = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in interpret_actions if a["style"] == "success"),
        user_id="1",
        chat_id="2",
    )
    g.set_frozen_tool_intent(sess.session_id, {"name": "postStoryDraftStash"})
    send_actions = g.offer_send_confirm(sess.session_id)
    send_tok = next(a["token"] for a in send_actions if a["style"] == "primary")
    result = g.consume_action_token(send_tok, user_id="1", chat_id="2")
    assert result["ok"] is True
    assert result["gateway_authorized"] is True
    assert result["gateway_invocations"] == 1
    assert result["state"] == SessionState.EXECUTING.value


def test_send_tokens_bind_session_draft_hash() -> None:
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="1", chat_id="2")
    interpret_actions = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in interpret_actions if a["style"] == "success"),
        user_id="1",
        chat_id="2",
    )
    dh = "deadbeef" * 8
    g.set_frozen_tool_intent(
        sess.session_id,
        {"name": "postStoryDraftStash"},
        draft_hash=dh,
    )
    send_actions = g.offer_send_confirm(sess.session_id)
    send_tok = next(a["token"] for a in send_actions if a["style"] == "primary")
    snap = g.tokens.bind_snapshot(send_tok)
    assert snap["draft_hash"] == dh
    assert snap["nonce"]
    assert snap["raw_stored"] is False
