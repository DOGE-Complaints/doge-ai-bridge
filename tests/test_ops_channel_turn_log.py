"""Ops channel turn log — diagnosis fields without full reply bodies."""

from __future__ import annotations

import logging

from aibridge.channel import _ops_reply_prefix, log_ops_channel_turn


def test_ops_reply_prefix_truncates() -> None:
    long = ("word " * 40) + "TAIL_MARKER_XYZ"
    out = _ops_reply_prefix(long)
    assert len(out) == 80
    assert "TAIL_MARKER_XYZ" not in out


def test_log_ops_channel_turn_includes_counts(
    caplog: logging.LogCaptureFixture,
) -> None:
    reply = (
        "Если формулировка верна, можно переходить к отправке через "
        "доступное в чате действие **Send**."
    )
    with caplog.at_level(logging.INFO, logger="aibridge.channel"):
        log_ops_channel_turn(
            session_id="sess_test70",
            state="interviewing",
            reply_text=reply,
            actions=[],
            fc_count=0,
            continuation_url=None,
            event_id="evt_join_tg",
        )
    joined = " ".join(r.getMessage() for r in caplog.records)
    assert "ops_channel_turn" in joined
    assert "event_id=evt_join_tg" in joined
    assert "session_id=sess_test70" in joined
    assert "state=interviewing" in joined
    assert "fc_count=0" in joined
    assert "actions_count=0" in joined
    assert "send_claim=True" in joined
    assert "needs_control=True" in joined
    assert "reply_prefix=" in joined
    assert "TAIL_MARKER" not in joined
