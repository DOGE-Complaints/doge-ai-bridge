"""Dual-confirm FSM — AIB-CONF-01A canonical states and transitions."""

from __future__ import annotations

from enum import StrEnum


class SessionState(StrEnum):
    INTERVIEWING = "interviewing"
    AWAITING_INTERPRETATION_CONFIRM = "awaiting_interpretation_confirm"
    INTERPRETATION_CONFIRMED = "interpretation_confirmed"
    AWAITING_SEND_CONFIRM = "awaiting_send_confirm"
    EXECUTING = "executing"
    STASHED = "stashed"
    CANCELLED = "cancelled"
    UNKNOWN_OUTCOME = "unknown_outcome"
    FAILED = "failed"


class ConfirmAction(StrEnum):
    OFFER_INTERPRETATION = "offer_interpretation"
    CONFIRM_INTERPRETATION = "confirm_interpretation"
    OFFER_SEND = "offer_send"
    CONFIRM_SEND = "confirm_send"
    MARK_STASHED = "mark_stashed"
    EDIT = "edit"
    CANCEL = "cancel"
    MARK_FAILED = "mark_failed"
    MARK_UNKNOWN_OUTCOME = "mark_unknown_outcome"


# (from_state, action) -> to_state
_TRANSITIONS: dict[tuple[SessionState, ConfirmAction], SessionState] = {
    (SessionState.INTERVIEWING, ConfirmAction.OFFER_INTERPRETATION): (
        SessionState.AWAITING_INTERPRETATION_CONFIRM
    ),
    (SessionState.AWAITING_INTERPRETATION_CONFIRM, ConfirmAction.CONFIRM_INTERPRETATION): (
        SessionState.INTERPRETATION_CONFIRMED
    ),
    (SessionState.INTERPRETATION_CONFIRMED, ConfirmAction.OFFER_SEND): (
        SessionState.AWAITING_SEND_CONFIRM
    ),
    (SessionState.AWAITING_SEND_CONFIRM, ConfirmAction.CONFIRM_SEND): (
        SessionState.EXECUTING
    ),
    (SessionState.EXECUTING, ConfirmAction.MARK_STASHED): SessionState.STASHED,
    (SessionState.EXECUTING, ConfirmAction.MARK_UNKNOWN_OUTCOME): (
        SessionState.UNKNOWN_OUTCOME
    ),
    (SessionState.EXECUTING, ConfirmAction.MARK_FAILED): SessionState.FAILED,
    # Edit from any non-terminal mid-flow → interviewing
    (SessionState.AWAITING_INTERPRETATION_CONFIRM, ConfirmAction.EDIT): (
        SessionState.INTERVIEWING
    ),
    (SessionState.INTERPRETATION_CONFIRMED, ConfirmAction.EDIT): SessionState.INTERVIEWING,
    (SessionState.AWAITING_SEND_CONFIRM, ConfirmAction.EDIT): SessionState.INTERVIEWING,
    (SessionState.INTERVIEWING, ConfirmAction.EDIT): SessionState.INTERVIEWING,
    # Cancel
    (SessionState.AWAITING_INTERPRETATION_CONFIRM, ConfirmAction.CANCEL): (
        SessionState.CANCELLED
    ),
    (SessionState.INTERPRETATION_CONFIRMED, ConfirmAction.CANCEL): SessionState.CANCELLED,
    (SessionState.AWAITING_SEND_CONFIRM, ConfirmAction.CANCEL): SessionState.CANCELLED,
    (SessionState.INTERVIEWING, ConfirmAction.CANCEL): SessionState.CANCELLED,
    (SessionState.UNKNOWN_OUTCOME, ConfirmAction.EDIT): SessionState.INTERVIEWING,
    (SessionState.FAILED, ConfirmAction.EDIT): SessionState.INTERVIEWING,
}


class IllegalTransitionError(ValueError):
    """FSM reject — fail closed."""

    def __init__(self, state: SessionState, action: ConfirmAction) -> None:
        super().__init__(f"illegal transition: {state.value} + {action.value}")
        self.state = state
        self.action = action


def next_state(state: SessionState, action: ConfirmAction) -> SessionState:
    key = (state, action)
    if key not in _TRANSITIONS:
        raise IllegalTransitionError(state, action)
    return _TRANSITIONS[key]


def can_transition(state: SessionState, action: ConfirmAction) -> bool:
    return (state, action) in _TRANSITIONS


# Actions that must never authorize gateway HTTP (AIB-CONF-01).
GATEWAY_FORBIDDEN_ACTIONS = frozenset(
    {
        ConfirmAction.OFFER_INTERPRETATION,
        ConfirmAction.CONFIRM_INTERPRETATION,
        ConfirmAction.OFFER_SEND,
        ConfirmAction.EDIT,
        ConfirmAction.CANCEL,
        ConfirmAction.MARK_FAILED,
    }
)
