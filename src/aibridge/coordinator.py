"""Turn coordinator — Responses → validate/freeze → confirm actions (story 11)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from aibridge.confirm import ConfirmationGuard, ConfirmSession
from aibridge.confirm_fsm import SessionState
from aibridge.request_assembly import (
    ServerConstants,
    ValidationGateError,
    run_three_gates,
)
from aibridge.tool_gen import CANONICAL_OPERATION_ID

ALLOWLISTED_TOOL_NAMES = frozenset({CANONICAL_OPERATION_ID})


@dataclass
class ValidationContext:
    """Schemas for AIB-REQ-02 three gates (injectable; required to freeze FC)."""

    tool_parameters: dict[str, Any]
    pack_schema: dict[str, Any]
    wire_schema: dict[str, Any]
    constants: ServerConstants


class ToolValidationError(ValueError):
    """Fail-closed tool gates (REQ-03 §4 #3 / AIB-RSP-04)."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def validate_function_calls(
    function_calls: list[dict[str, Any]],
    *,
    session_state: SessionState,
    validation: ValidationContext | None = None,
) -> dict[str, Any]:
    """Allowlist + parse + FSM + run_three_gates when validation context present.

    Returns frozen intent dict including call_id + assembled arguments body.
    """
    if len(function_calls) != 1:
        raise ToolValidationError(
            "conflict",
            "Exactly one consequential function_call per turn is required",
        )
    fc = function_calls[0]
    name = str(fc.get("name") or "")
    if name not in ALLOWLISTED_TOOL_NAMES:
        raise ToolValidationError("conflict", f"Tool name not allowlisted: {name}")
    call_id = str(fc.get("call_id") or "").strip()
    if not call_id:
        raise ToolValidationError("conflict", "function_call missing call_id")
    raw_args = fc.get("arguments")
    if isinstance(raw_args, dict):
        model_args = dict(raw_args)
    else:
        try:
            parsed = json.loads(str(raw_args or "{}"))
        except json.JSONDecodeError as exc:
            raise ToolValidationError(
                "conflict", "Malformed function_call arguments"
            ) from exc
        if not isinstance(parsed, dict):
            raise ToolValidationError(
                "conflict", "function_call arguments must be a JSON object"
            )
        model_args = parsed
    # Consequential FC only after interpretation confirmation (AIB-RSP-03).
    if session_state not in {
        SessionState.INTERPRETATION_CONFIRMED,
        SessionState.AWAITING_SEND_CONFIRM,
    }:
        raise ToolValidationError(
            "conflict",
            "function_call blocked until interpretation is confirmed",
        )
    if validation is None:
        raise ToolValidationError(
            "conflict",
            "Three validation gates require ValidationContext (schemas not configured)",
        )
    try:
        assembled, d_hash = run_three_gates(
            model_args,
            tool_parameters=validation.tool_parameters,
            pack_schema=validation.pack_schema,
            wire_schema=validation.wire_schema,
            constants=validation.constants,
        )
    except ValidationGateError as exc:
        raise ToolValidationError("conflict", str(exc)) from exc
    return {
        "name": name,
        "call_id": call_id,
        "arguments": assembled,
        "draft_hash": d_hash,
    }


def persist_pending_tool(
    guard: ConfirmationGuard,
    sess: ConfirmSession,
    *,
    frozen: dict[str, Any],
    replay_items: list[dict[str, Any]],
) -> None:
    """Persist call_id, frozen body, replay items before /turns returns actions."""
    guard.set_frozen_tool_intent(
        sess.session_id,
        {
            "name": frozen["name"],
            "call_id": frozen["call_id"],
            "arguments": frozen["arguments"],
        },
        draft_hash=str(frozen["draft_hash"]),
    )
    sess.pending_call_id = str(frozen["call_id"])
    sess.pending_replay_items = list(replay_items)
    guard._persist_session(sess)  # noqa: SLF001 — intentional before actions return


def build_turn_from_engine(
    guard: ConfirmationGuard,
    sess: ConfirmSession,
    engine_result: dict[str, Any],
) -> dict[str, Any]:
    """Map InterviewEngine result → channel success fields (no Received stub)."""
    if not engine_result.get("ok", True):
        return {
            "session_id": sess.session_id,
            "state": sess.state.value,
            "reply_text": str(
                engine_result.get("message")
                or engine_result.get("reply_text")
                or "Turn rejected."
            ),
            "actions": [],
            "outcome": None,
            "draft_id": None,
            "continuation_url": None,
        }

    reply = str(engine_result.get("reply_text") or "Acknowledged.")
    # Never echo stub Received: — strip if a bad client leaked it.
    if reply.startswith("Received:"):
        reply = "Acknowledged."

    fcs = list(engine_result.get("function_calls") or [])
    replay = list(engine_result.get("replay_items") or [])

    # Ordinary interview — offer interpretation once while interviewing (AIB-RSP-03).
    if not fcs:
        actions: list[dict[str, str]] = []
        if sess.state is SessionState.INTERVIEWING:
            actions = guard.offer_interpretation_confirm(sess.session_id)
            guard._persist_session(sess)  # noqa: SLF001
        # If already awaiting/confirmed, do not re-mint; wait for /actions or FC.
        return {
            "session_id": sess.session_id,
            "state": sess.state.value,
            "reply_text": reply,
            "actions": actions,
            "outcome": None,
            "draft_id": None,
            "continuation_url": None,
        }

    try:
        frozen = validate_function_calls(
            fcs,
            session_state=sess.state,
            validation=getattr(guard, "validation_context", None),
        )
    except ToolValidationError as exc:
        return {
            "session_id": sess.session_id,
            "state": sess.state.value,
            "reply_text": exc.message,
            "actions": [],
            "outcome": None,
            "draft_id": None,
            "continuation_url": None,
        }

    # Persist BEFORE minting actions (REQ-03 §5.2).
    persist_pending_tool(guard, sess, frozen=frozen, replay_items=replay)
    actions = guard.offer_send_confirm(sess.session_id)
    guard._persist_session(sess)  # noqa: SLF001
    return {
        "session_id": sess.session_id,
        "state": sess.state.value,
        "reply_text": reply or "Ready to send — confirm below.",
        "actions": actions,
        "outcome": None,
        "draft_id": None,
        "continuation_url": None,
    }
