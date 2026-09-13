"""LLM budget / rate / timeout guards — fail closed without gateway side effects."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


class BudgetBreachError(Exception):
    """Resident-safe budget/rate/timeout failure (no gateway call)."""

    def __init__(self, reason: str, *, metric_reason: str) -> None:
        super().__init__(reason)
        self.reason = reason
        self.metric_reason = metric_reason  # redacted / coarse


@dataclass
class BudgetLimits:
    """Env placeholders — numeric defaults Unknown until measured (REQ-01 §17)."""

    max_input_tokens: int | None = None
    max_output_tokens: int | None = None
    max_responses_calls_per_turn: int | None = None
    max_tool_calls_per_turn: int | None = None
    openai_timeout_ms: int | None = None
    max_session_turns: int | None = None


class SettingsLike(Protocol):
    aibridge_max_input_tokens: int | None
    aibridge_max_output_tokens: int | None
    aibridge_max_responses_calls_per_turn: int | None
    aibridge_max_tool_calls_per_turn: int | None
    aibridge_openai_timeout_ms: int | None
    aibridge_max_session_turns: int | None


def budget_limits_from_settings(settings: SettingsLike) -> BudgetLimits:
    """Map Settings budget knobs → BudgetLimits (None = unset / no enforce)."""
    return BudgetLimits(
        max_input_tokens=settings.aibridge_max_input_tokens,
        max_output_tokens=settings.aibridge_max_output_tokens,
        max_responses_calls_per_turn=settings.aibridge_max_responses_calls_per_turn,
        max_tool_calls_per_turn=settings.aibridge_max_tool_calls_per_turn,
        openai_timeout_ms=settings.aibridge_openai_timeout_ms,
        max_session_turns=settings.aibridge_max_session_turns,
    )


def any_budget_limit_set(limits: BudgetLimits) -> bool:
    return any(
        v is not None
        for v in (
            limits.max_input_tokens,
            limits.max_output_tokens,
            limits.max_responses_calls_per_turn,
            limits.max_tool_calls_per_turn,
            limits.openai_timeout_ms,
            limits.max_session_turns,
        )
    )


@dataclass
class BudgetGuard:
    limits: BudgetLimits
    _session_turns: dict[str, int] = field(default_factory=dict)
    metric_events: list[dict[str, Any]] = field(default_factory=list)

    def check_turn_start(self, session_id: str) -> None:
        lim = self.limits.max_session_turns
        if lim is None:
            return
        used = self._session_turns.get(session_id, 0)
        if used >= lim:
            self._emit("budget_session_turns")
            raise BudgetBreachError(
                "Session turn budget exceeded",
                metric_reason="budget_session_turns",
            )

    def record_turn(self, session_id: str) -> None:
        self._session_turns[session_id] = self._session_turns.get(session_id, 0) + 1

    def check_elapsed(self, elapsed_ms: int) -> None:
        """Enforce openai_timeout_ms wall-clock budget (unset = no-op)."""
        lim = self.limits.openai_timeout_ms
        if lim is None:
            return
        if elapsed_ms > lim:
            self._emit("budget_openai_timeout")
            raise BudgetBreachError(
                "OpenAI Responses timeout exceeded",
                metric_reason="budget_openai_timeout",
            )

    def check_usage(
        self,
        *,
        input_tokens: int = 0,
        output_tokens: int = 0,
        responses_calls: int = 1,
        tool_calls: int = 0,
    ) -> None:
        lim = self.limits
        if lim.max_responses_calls_per_turn is not None and responses_calls > lim.max_responses_calls_per_turn:
            self._emit("budget_responses_calls")
            raise BudgetBreachError(
                "Responses calls per turn exceeded",
                metric_reason="budget_responses_calls",
            )
        if lim.max_tool_calls_per_turn is not None and tool_calls > lim.max_tool_calls_per_turn:
            self._emit("budget_tool_calls")
            raise BudgetBreachError(
                "Tool calls per turn exceeded",
                metric_reason="budget_tool_calls",
            )
        if lim.max_input_tokens is not None and input_tokens > lim.max_input_tokens:
            self._emit("budget_input_tokens")
            raise BudgetBreachError(
                "Input token budget exceeded",
                metric_reason="budget_input_tokens",
            )
        if lim.max_output_tokens is not None and output_tokens > lim.max_output_tokens:
            self._emit("budget_output_tokens")
            raise BudgetBreachError(
                "Output token budget exceeded",
                metric_reason="budget_output_tokens",
            )

    def _emit(self, metric_reason: str) -> None:
        # Redacted reason only — no prompt/PII.
        self.metric_events.append({"event": "budget_breach", "reason": metric_reason})
        try:
            from aibridge.metrics import get_metrics

            get_metrics().record_budget_stop(metric_reason)
        except Exception:  # noqa: BLE001 — metrics must not break fail-closed budget path
            pass
