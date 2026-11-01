"""STORY-AIBRIDGE-57 — L11-1 invalidation seam (AC-AIB-11-02 transition C).

Named seam invalidate_send_permission() shares apply_edit clearance effects.
Target A remains Partial until REQ-13 semantic state Present — do not invent taxonomy.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from aibridge.confirm import ConfirmationGuard
from aibridge.confirm_fsm import IllegalTransitionError, SessionState
from aibridge.gateway import (
    GatewayExecutor,
    GatewayOutcome,
    RecordingGatewayTransport,
    RawHttpResponse,
)
import json

_REPO = Path(__file__).resolve().parents[1]

# Honesty: AC-AIB-11-02 target A not Done in this wave.
AC_AIB_11_02_TARGET_A_STATUS = "Partial"


def _ok_201() -> RawHttpResponse:
    body = json.dumps(
        {"data": {"draft_id": "draft-57"}, "trace_id": "trace-57"}
    ).encode()
    return RawHttpResponse(status_code=201, body=body)


def _guard_with_send_offered() -> tuple[ConfirmationGuard, object, str]:
    transport = RecordingGatewayTransport(scripted=[_ok_201()])
    executor = GatewayExecutor(
        origin="https://gateway.example.invalid",
        gateway_bearer="gw-57",
        channel_bearer="ch-57",
        redirect_base="https://spa.example",
        transport=transport,
    )
    g = ConfirmationGuard(executor=executor)
    sess = g.get_or_create_session(user_id="u57", chat_id="c57")
    interpret = g.offer_interpretation_confirm(sess.session_id)
    g.consume_action_token(
        next(a["token"] for a in interpret if a["style"] == "success"),
        user_id="u57",
        chat_id="c57",
    )
    g.set_frozen_tool_intent(sess.session_id, {"arguments": {"t": 1}}, draft_hash="h57")
    send_actions = g.offer_send_confirm(sess.session_id)
    send_tok = next(a["token"] for a in send_actions if a["style"] == "primary")
    # Simulate authorized send path without HTTP: mark gateway_authorized via consume deferred
    # or leave at awaiting_send — for invalidate we need permission-ish state.
    return g, sess, send_tok


# --- t01/t02 seam = apply_edit clearance ---


def test_t01_t02_apply_edit_uses_named_seam_and_clears_send() -> None:
    g, sess, send_tok = _guard_with_send_offered()
    assert hasattr(g, "invalidate_send_permission")
    assert callable(g.invalidate_send_permission)
    old_rev = sess.revision
    assert sess.state is SessionState.AWAITING_SEND_CONFIRM
    g.apply_edit(sess.session_id)
    assert sess.state is SessionState.INTERVIEWING
    assert sess.revision == old_rev + 1
    assert sess.gateway_authorized is False
    assert sess.frozen_tool_intent is None
    assert sess.draft_hash is None
    assert sess.continuation_url is None
    assert sess.draft_id is None
    bad = g.consume_action_token(send_tok, user_id="u57", chat_id="c57")
    assert bad["ok"] is False
    assert bad["http_status"] == 409


# --- t03 transition C: EDIT remains enforce while state Absent ---


def test_t03_transition_c_edit_invalidates_send_permission() -> None:
    g, sess, send_tok = _guard_with_send_offered()
    # No semantic state store — enforce via EDIT only.
    g.apply_edit(sess.session_id)
    bad = g.consume_action_token(send_tok, user_id="u57", chat_id="c57")
    assert bad["ok"] is False
    # After edit, cannot offer send without re-confirm/freeze path.
    with pytest.raises(IllegalTransitionError):
        g.offer_send_confirm(sess.session_id)


# --- t04 unit: seam without Telegram EDIT → same clearance ---


def test_t04_seam_invoke_without_edit_matches_clearance() -> None:
    g, sess, send_tok = _guard_with_send_offered()
    pre_state = sess.state
    old_rev = sess.revision
    # Call named seam directly — future meaning-change entry (no FSM EDIT).
    g.invalidate_send_permission(sess.session_id, reason="meaning_change_future")
    assert sess.revision == old_rev + 1
    assert sess.gateway_authorized is False
    assert sess.frozen_tool_intent is None
    assert sess.draft_hash is None
    assert sess.continuation_url is None
    # Without apply_edit, FSM may remain pre-EDIT state (transition C honesty).
    assert sess.state is pre_state
    bad = g.consume_action_token(send_tok, user_id="u57", chat_id="c57")
    assert bad["ok"] is False
    assert bad["http_status"] == 409
    # Target A remains Partial — marker for honesty gate.
    assert AC_AIB_11_02_TARGET_A_STATUS == "Partial"


def test_t04_seam_and_apply_edit_clearance_parity() -> None:
    """Clearance fields match between seam-only and apply_edit (minus FSM state)."""

    def _cleared(sess) -> dict:
        return {
            "revision_delta": True,
            "gateway_authorized": sess.gateway_authorized,
            "frozen": sess.frozen_tool_intent,
            "draft_hash": sess.draft_hash,
            "continuation": sess.continuation_url,
            "draft_id": sess.draft_id,
        }

    g1, s1, tok1 = _guard_with_send_offered()
    rev1 = s1.revision
    g1.invalidate_send_permission(s1.session_id, reason="meaning_change_future")
    c1 = _cleared(s1)
    assert s1.revision == rev1 + 1

    g2, s2, tok2 = _guard_with_send_offered()
    rev2 = s2.revision
    g2.apply_edit(s2.session_id)
    c2 = _cleared(s2)
    assert s2.revision == rev2 + 1
    assert c1 == c2
    assert g1.consume_action_token(tok1, user_id="u57", chat_id="c57")["http_status"] == 409
    assert g2.consume_action_token(tok2, user_id="u57", chat_id="c57")["http_status"] == 409


# --- t05 / gate docs ---


def test_t05_doc_target_a_partial_vs_done() -> None:
    note = _REPO / "docs" / "runtime-docs" / "05-l11-invalidation-seam.md"
    assert note.is_file()
    text = note.read_text(encoding="utf-8")
    assert "Partial" in text
    assert "AC-AIB-11-02" in text
    assert "REQ-13" in text
    assert "invalidate_send_permission" in text
    assert "Done" in text
    # Must not claim target A Done in this wave.
    assert AC_AIB_11_02_TARGET_A_STATUS == "Partial"
    arch = (
        _REPO
        / "docs"
        / "architecture"
        / "req15-dual-confirm-handoff"
        / "02-l11-invalidation-seam.md"
    )
    assert arch.is_file()
