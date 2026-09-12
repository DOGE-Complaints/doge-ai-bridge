"""t04 — Edit/Cancel invalidate + ownership."""

from __future__ import annotations

from aibridge.confirm import ConfirmationGuard


def test_edit_increments_revision_and_invalidates_send() -> None:
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="10", chat_id="20")
    a1 = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(x["token"] for x in a1 if x["style"] == "success"),
        user_id="10",
        chat_id="20",
    )
    g.set_frozen_tool_intent(sess.session_id, {"x": 1})
    a2 = g.offer_send_confirm(sess.session_id)
    send_tok = next(x["token"] for x in a2 if x["style"] == "primary")
    old_rev = sess.revision
    g.apply_edit(sess.session_id)
    assert sess.revision == old_rev + 1
    assert sess.state.value == "interviewing"
    bad = g.consume_action_token(send_tok, user_id="10", chat_id="20")
    assert bad["ok"] is False
    assert bad["http_status"] == 409


def test_cancel_invalidates_tokens() -> None:
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="3", chat_id="4")
    acts = g.offer_interpretation_confirm(sess.session_id)
    cancel_tok = next(x["token"] for x in acts if x["style"] == "danger")
    other = next(x["token"] for x in acts if x["style"] == "success")
    ok = g.consume_action_token(cancel_tok, user_id="3", chat_id="4")
    assert ok["ok"] is True
    assert ok["state"] == "cancelled"
    bad = g.consume_action_token(other, user_id="3", chat_id="4")
    assert bad["ok"] is False
    assert bad["http_status"] == 409


def test_foreign_principal_forbidden() -> None:
    g = ConfirmationGuard()
    sess = g.get_or_create_session(user_id="1", chat_id="2")
    acts = g.offer_interpretation_confirm(sess.session_id)
    tok = acts[0]["token"]
    bad = g.consume_action_token(tok, user_id="999", chat_id="2")
    assert bad["ok"] is False
    assert bad["http_status"] == 403
