"""t01 — dual-confirm FSM states and transitions."""

from __future__ import annotations

import pytest

from aibridge.confirm_fsm import (
    ConfirmAction,
    IllegalTransitionError,
    SessionState,
    can_transition,
    next_state,
)


def test_happy_path_transitions() -> None:
    s = SessionState.INTERVIEWING
    s = next_state(s, ConfirmAction.OFFER_INTERPRETATION)
    assert s is SessionState.AWAITING_INTERPRETATION_CONFIRM
    s = next_state(s, ConfirmAction.CONFIRM_INTERPRETATION)
    assert s is SessionState.INTERPRETATION_CONFIRMED
    s = next_state(s, ConfirmAction.OFFER_SEND)
    assert s is SessionState.AWAITING_SEND_CONFIRM
    s = next_state(s, ConfirmAction.CONFIRM_SEND)
    assert s is SessionState.EXECUTING
    s = next_state(s, ConfirmAction.MARK_STASHED)
    assert s is SessionState.STASHED


def test_illegal_transition_fail_closed() -> None:
    with pytest.raises(IllegalTransitionError):
        next_state(SessionState.INTERVIEWING, ConfirmAction.CONFIRM_SEND)
    assert not can_transition(SessionState.STASHED, ConfirmAction.CONFIRM_SEND)
    assert not can_transition(
        SessionState.UNKNOWN_OUTCOME, ConfirmAction.CONFIRM_SEND
    )


def test_edit_and_cancel_from_awaiting() -> None:
    assert (
        next_state(SessionState.AWAITING_SEND_CONFIRM, ConfirmAction.EDIT)
        is SessionState.INTERVIEWING
    )
    assert (
        next_state(SessionState.AWAITING_INTERPRETATION_CONFIRM, ConfirmAction.CANCEL)
        is SessionState.CANCELLED
    )
