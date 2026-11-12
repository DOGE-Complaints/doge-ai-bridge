# Task: implement — channel 429 + finite budget defaults on /turns

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md`  
**Parent story:** [`STORY-AIBRIDGE-14-p1-ops-schema-restart.md`](../STORY-AIBRIDGE-14-p1-ops-schema-restart.md)  
**P1 scaffold:** 2026-09-13T17:03:24Z  
**Maps:** Scope #2 · R3-P1-02

## Purpose

Close R3-P1-02: channel **429** / rate limits plus **finite budget defaults** enforced on `/turns` (OpenAI spend guard). Story 12 only wired knobs «when set».

## Code Facts (verified exists — P1)

1. `RateLimiter` + middleware → HTTP 429 in `src/aibridge/app.py` / `rate_limit.py`.
2. Settings defaults for principal/global rate limits and LLM budgets are `None` (`config.py` L59–66, L120–144); comment: «do not invent».
3. `BudgetGuard` attaches only when any limit set (`app.py` + `budgets.py`).

## AC/DoD

- [x] Finite documented defaults for rate limits and LLM budgets (or explicit product-chosen values with evidence in README/tests).
- [x] Budgets enforced on `/channel/.../turns` path (fail-closed, no gateway side effects).
- [x] Over-limit requests return channel **429** with OpenAPI-conformant error body.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/config.py`, `budgets.py`, `rate_limit.py`, `app.py`, `.env.example`, `tests/`.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "rate_limit or budget or 429 or story_14" --maxfail=10
```
