"""STORY-68/70 — seam policy + control-surface gate.

Arch: docs/architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md
      docs/architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md

Free-text «дальше» / «отправляй» is never the sole advance path when a seam is non-seamless.
CONTINUE ≠ interpretation confirm ≠ Send (REQ-11 Keep stash only via CONFIRM_SEND).
Send-claim prose without actions/URL → remint CTAs (no invent stash · no NL rewrite v1).
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

# STORY-70 — phrases that assert an in-chat Send/submit control is available.
# Literal lock: do NOT treat bare «отправ» / «отправка» as a claim (false-positive fence).
# Matching runs on markdown-stripped casefold text (see _normalize_claim_text).
SEND_CLAIM_MARKERS: tuple[str, ...] = (
    "действие send",
    "действию send",
    "действием send",
    "действия send",
    "action send",
    "send button",
    "send-кнопк",  # send-кнопка / send-кнопку (prefix)
    "кнопку send",
    "кнопка send",
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


def _normalize_claim_text(reply_text: str) -> str:
    """Casefold + strip markdown emphasis so «**Send**» matches marker «send»."""
    raw = (reply_text or "").casefold().replace("*", "").replace("_", " ")
    return " ".join(raw.split())


def reply_claims_vague_interface(reply_text: str) -> bool:
    """True when assistant copy points at vague UI without a concrete control."""
    low = _normalize_claim_text(reply_text)
    return any(marker in low for marker in VAGUE_INTERFACE_MARKERS)


def reply_claims_send_control(reply_text: str) -> bool:
    """STORY-70 — True when copy asserts an in-chat Send/submit control is available."""
    low = _normalize_claim_text(reply_text)
    return any(marker in low for marker in SEND_CLAIM_MARKERS)


def needs_control_surface(
    *,
    reply_text: str,
    actions: list[dict[str, str]] | None,
    continuation_url: str | None,
) -> bool:
    """AC-68-03 / AC-70-01: vague or Send-claim requires actions or post-stash URL."""
    claimed = reply_claims_vague_interface(reply_text) or reply_claims_send_control(
        reply_text
    )
    if not claimed:
        return False
    if actions:
        return False
    if continuation_url:
        return False
    return True
