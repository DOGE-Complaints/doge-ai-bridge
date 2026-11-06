"""STORY-68 — seam policy invariants (non-seamless stages → actions).

Arch: docs/architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md §2–§4.
Free-text «дальше» / «отправляй» is never the sole advance path when a seam is non-seamless.
CONTINUE ≠ interpretation confirm ≠ Send (REQ-11 Keep stash only via CONFIRM_SEND).
"""

from __future__ import annotations

from enum import StrEnum

from aibridge.confirm_fsm import SessionState


class SeamKind(StrEnum):
    """Product-thin stage→action class for channel turns."""

    INTERPRETATION = "interpretation"  # INTERVIEWING FC-less → Looks right / Edit / Cancel
    CONTINUE_EDIT = "continue_edit"  # INTERPRETATION_CONFIRMED FC-less → CONTINUE / Edit
    SEND_CONFIRM = "send_confirm"  # frozen+validated FC → Send / Edit / Cancel
    AWAITING_ACTION = "awaiting_action"  # already awaiting confirm — wait /actions
    TERMINAL = "terminal"  # stashed / cancelled / failed — no new seam CTAs
    ERROR_RECOVER = "error_recover"  # validation / engine reject mid-flow


# States where an ordinary (FC-less) reply MUST expose ≥1 Telegram-renderable action.
NON_SEAMLESS_FCLESS_STATES: frozenset[SessionState] = frozenset(
    {
        SessionState.INTERVIEWING,
        SessionState.INTERPRETATION_CONFIRMED,
    }
)

# Markers that claim submission lives «в интерфейсе» without naming a control.
# Enforcement = ensure actions or post-stash URL — not ML rewrite invent (OOS).
VAGUE_INTERFACE_MARKERS: tuple[str, ...] = (
    "интерфейс",  # covers «в интерфейсе» / «интерфейсе DOGEstonia»
    "in the interface",
    "in the ui",
)


def classify_fcless_seam(state: SessionState) -> SeamKind:
    """Map confirm FSM state → seam class for FC-less engine replies."""
    if state is SessionState.INTERVIEWING:
        return SeamKind.INTERPRETATION
    if state is SessionState.INTERPRETATION_CONFIRMED:
        return SeamKind.CONTINUE_EDIT
    if state in {
        SessionState.AWAITING_INTERPRETATION_CONFIRM,
        SessionState.AWAITING_SEND_CONFIRM,
    }:
        return SeamKind.AWAITING_ACTION
    if state in {
        SessionState.STASHED,
        SessionState.CANCELLED,
        SessionState.FAILED,
        SessionState.UNKNOWN_OUTCOME,
        SessionState.EXECUTING,
    }:
        return SeamKind.TERMINAL
    return SeamKind.TERMINAL


def requires_fcless_actions(state: SessionState) -> bool:
    """True when free-text alone must not be the sole advance path."""
    return state in NON_SEAMLESS_FCLESS_STATES


def reply_claims_vague_interface(reply_text: str) -> bool:
    """True when assistant copy points at vague UI without a concrete control."""
    low = (reply_text or "").casefold()
    return any(marker in low for marker in VAGUE_INTERFACE_MARKERS)


def needs_control_surface(
    *,
    reply_text: str,
    actions: list[dict[str, str]] | None,
    continuation_url: str | None,
) -> bool:
    """AC-68-03: vague «интерфейс» claim requires actions or post-stash URL."""
    if not reply_claims_vague_interface(reply_text):
        return False
    if actions:
        return False
    if continuation_url:
        return False
    return True
