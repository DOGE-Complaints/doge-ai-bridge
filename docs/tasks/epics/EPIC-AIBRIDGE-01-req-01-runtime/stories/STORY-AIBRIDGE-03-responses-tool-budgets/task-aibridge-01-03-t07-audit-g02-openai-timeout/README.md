# Task: implement — enforce OpenAI timeout budget (G-02)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_03_audit_20260912`  
**Gap:** G-02 (Info) — P4 audit 2026-09-12  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-03-responses-tool-budgets-20260912.md`  
**Parent story:** [`STORY-AIBRIDGE-03-responses-tool-budgets.md`](../STORY-AIBRIDGE-03-responses-tool-budgets.md)  
**P5 scaffold:** 2026-09-12T21:27:29Z  
**P6 Done:** 2026-09-12T21:30:01Z

## Purpose

Enforce `AIBRIDGE_OPENAI_TIMEOUT_MS` / `BudgetLimits.openai_timeout_ms` on the Responses call path: elapsed wall time → resident-safe `budget_breach`, redacted metric, **no gateway**.

**Out of this task:** Live OpenAI HTTP client; inventing numeric default timeout; Postgres history (G-01 → STORY-AIBRIDGE-07).

## Code Facts (verified exists — post P6)

1. `BudgetGuard.check_elapsed` — `src/aibridge/budgets.py`.
2. `InterviewEngine.run_turn` measures wall time around `client.create` and calls `check_elapsed`.
3. Tests — `tests/test_budgets.py` (`test_openai_timeout_breach`, `test_interview_timeout_no_gateway`).

## AC/DoD

- [x] When `openai_timeout_ms` is set and Responses call elapsed exceeds it → `BudgetBreachError` / interview `budget_breach` with `metric_reason=budget_openai_timeout`.
- [x] No gateway invocation on timeout breach.
- [x] Unset (`None`) timeout remains no-op (do not invent default).
- [x] Tests cover breach + unset allow.
- [x] `Skill declared: python-pro` present.

## Where to change

- `src/aibridge/budgets.py`, `interview.py`
- `tests/test_budgets.py`

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_budgets.py
```
