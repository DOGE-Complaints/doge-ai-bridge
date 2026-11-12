# Task: implement — LLM budgets / rate / timeout without gateway side effect

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-03-responses-tool-budgets.md`  
**Parent story:** [`STORY-AIBRIDGE-03-responses-tool-budgets.md`](../STORY-AIBRIDGE-03-responses-tool-budgets.md)

## Purpose

Enforce budget / rate / timeout env knobs (placeholders OK — numeric defaults **Unknown**); bounded resident-safe error; **no gateway side effect**; keep last confirmed state; redacted metric reason hook (full `/metrics` in 06).

**Out of this task:** inventing measured numeric defaults; dual-confirm Send (04/05); full metrics series (06).

## Code Facts (verified exists)

1. Budget env names — REQ-01 §17; `04-ops-security.md` §2.
2. Pre-send safe failure note — `03-confirm-gateway.md` §4.
3. No budget guard in `src/` yet; no gateway HTTP client yet (story 05).

## AC/DoD

- [ ] Budget breach → resident-safe error, no gateway call, redacted metric reason (AC #3).
- [ ] Env knobs present as placeholders (no invented measured defaults).
- [ ] Last confirmed state retained on fail.
- [ ] `Skill declared: python-pro` present.

## Where to change

- Budget guard module + `config.py` aliases.
- Ensure Responses/turn path consults guard before any future gateway call.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# mock gateway must not be invoked on budget breach
```
