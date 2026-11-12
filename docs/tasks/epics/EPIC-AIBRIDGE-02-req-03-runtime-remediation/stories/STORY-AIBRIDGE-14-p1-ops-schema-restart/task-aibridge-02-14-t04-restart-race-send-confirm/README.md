# Task: tests — restart recovery + DB race (Send / pending-confirm / unknown_outcome)

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md`  
**Parent story:** [`STORY-AIBRIDGE-14-p1-ops-schema-restart.md`](../STORY-AIBRIDGE-14-p1-ops-schema-restart.md)  
**P1 scaffold:** 2026-09-13T17:03:24Z  
**Maps:** Scope #4 · R3-P1-04 · Target #3

## Purpose

Prove restart recovery and DB race/restart behavior for Send, pending-confirm, and `unknown_outcome` (REQ-03 §4 AC #7–#8 / R3-P1-04).

## Code Facts (verified exists — P1)

1. Wave-1 E2E restart/OpenAPI coverage — `tests/test_story_13_wave1_asgi_e2e.py` (+ harness); does **not** fully own P1-04 Send/pending-confirm/`unknown_outcome` race matrix.
2. Attempt store / confirm paths — `pg_runtime.py`, `confirm.py`, `gateway.py` (`GatewayOutcome.UNKNOWN_OUTCOME`).
3. Disposable PG — `scripts/start-disposable-pg.sh`.

## AC/DoD

- [x] Tests cover restart/race for Send, pending-confirm, and `unknown_outcome` (AC #7–#8 evidence).
- [x] No invented live n8n/OpenAI; use disposable PG + fakes where needed.
- [x] `Skill declared: python-pro` present.

## Where to change

`tests/` (new or extend story-14 suite); product fixes only if races expose bugs.

## Verification commands

```bash
cd doge-ai-bridge && ./scripts/start-disposable-pg.sh
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "restart or race or unknown_outcome or story_14" --maxfail=10
```
