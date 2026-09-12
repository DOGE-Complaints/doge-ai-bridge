"""t04 — LLM budgets; breach → no gateway side effect."""

from __future__ import annotations

import time

import pytest

from aibridge.budgets import BudgetBreachError, BudgetGuard, BudgetLimits
from aibridge.interview import InterviewEngine
from aibridge.responses_client import RecordingResponsesClient


def test_budget_session_turns_breach_no_gateway() -> None:
    client = RecordingResponsesClient()
    guard = BudgetGuard(BudgetLimits(max_session_turns=1))
    engine = InterviewEngine(client=client, budgets=guard)
    ok = engine.run_turn(session_id="s", user_text="first")
    assert ok["ok"] is True
    engine.last_confirmed_state["s"] = "interviewing"
    bad = engine.run_turn(session_id="s", user_text="second")
    assert bad["ok"] is False
    assert bad["error"] == "budget_breach"
    assert bad["gateway_called"] is False
    assert engine.gateway_invocations == 0
    assert client.gateway_calls == 0
    assert bad["metric_reason"] == "budget_session_turns"
    assert any(e["reason"] == "budget_session_turns" for e in guard.metric_events)


def test_budget_input_tokens_breach() -> None:
    guard = BudgetGuard(BudgetLimits(max_input_tokens=5))
    with pytest.raises(BudgetBreachError) as ei:
        guard.check_usage(input_tokens=10)
    assert ei.value.metric_reason == "budget_input_tokens"


def test_budget_unset_limits_allow() -> None:
    """None limits = unset placeholders — do not invent numeric defaults."""
    guard = BudgetGuard(BudgetLimits())
    guard.check_usage(input_tokens=10_000, output_tokens=10_000, responses_calls=99)
    guard.check_elapsed(60_000)


def test_openai_timeout_breach() -> None:
    guard = BudgetGuard(BudgetLimits(openai_timeout_ms=50))
    with pytest.raises(BudgetBreachError) as ei:
        guard.check_elapsed(51)
    assert ei.value.metric_reason == "budget_openai_timeout"
    assert any(e["reason"] == "budget_openai_timeout" for e in guard.metric_events)


def test_interview_timeout_no_gateway() -> None:
    class SlowClient(RecordingResponsesClient):
        def create(self, request):  # type: ignore[no-untyped-def]
            time.sleep(0.05)
            return super().create(request)

    client = SlowClient()
    guard = BudgetGuard(BudgetLimits(openai_timeout_ms=10))
    engine = InterviewEngine(client=client, budgets=guard)
    bad = engine.run_turn(session_id="s", user_text="hi")
    assert bad["ok"] is False
    assert bad["metric_reason"] == "budget_openai_timeout"
    assert bad["gateway_called"] is False
    assert engine.gateway_invocations == 0
