# Task: test — E2E function_call + interpretation confirm (AC #3–#4)

**Status:** Done  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md`  
**Parent story:** [`STORY-AIBRIDGE-13-wave1-asgi-e2e.md`](../STORY-AIBRIDGE-13-wave1-asgi-e2e.md)  
**P1 scaffold:** 2026-09-13T16:34:47Z  
**Maps:** REQ-03 §4 AC #3–#4

## Purpose

ASGI E2E: allowlisted `function_call` passes three gates, persists `call_id`, no gateway before Send; interpretation confirm mutates state, no gateway HTTP, returns next bounded response.

## Code Facts (verified exists — P1)

1. Coordinator + tool loop unit coverage — `tests/test_story_11_coordinator.py`.
2. Flat tools / adapter — story 10 product path.
3. Wave-1 ASGI E2E for AC #3–#4 not yet a dedicated suite.

## AC/DoD

- [x] E2E proves FC allowlist + three validation gates + `call_id` persistence; gateway fake records **zero** HTTPS before Send.
- [x] E2E interpretation confirm changes state without gateway HTTP; response bounded.
- [x] Depends on t01 harness.
- [x] `Skill declared: test-master` present.

## Where to change

`tests/` E2E module(s).

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "story_13 and (function_call or interpretation or confirm)" --maxfail=5
```
