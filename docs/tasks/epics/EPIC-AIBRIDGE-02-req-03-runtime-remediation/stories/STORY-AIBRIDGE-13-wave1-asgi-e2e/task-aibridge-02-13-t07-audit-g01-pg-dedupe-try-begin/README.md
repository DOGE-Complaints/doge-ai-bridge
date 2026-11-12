# Task: implement — PostgresEventDedupeStore try_begin/complete (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_13_audit_20260913`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-13-wave1-asgi-e2e-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-13-wave1-asgi-e2e.md`](../STORY-AIBRIDGE-13-wave1-asgi-e2e.md)  
**P5 scaffold:** 2026-09-13T16:54:19Z
**P6 Done:** 2026-09-13T16:58:55Z  
**Maps:** REQ-03 §4 #2 · R3-P0-12 ASGI+Postgres claim-before-engine

## Purpose

Parity with in-memory `EventDedupeStore.try_begin`/`complete`/`abort` on `PostgresEventDedupeStore` so ASGI `process_turn_async` claims before Responses (no peek-then-engine race). Optional: apply stored `http_status` on replay; concurrent same `event_id` E2E.

## AC/DoD

- [x] `PostgresEventDedupeStore` implements `try_begin` / `complete` / `abort` (+ `wait_for_result` if needed).
- [x] ASGI path uses claim-before-engine on PG (no Legacy peek branch for PG store).
- [x] Concurrent duplicate `(channel, event_id)` does not double-call Responses (test).
- [x] Serial replay/restart E2E still green.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/pg_runtime.py`, optionally `channel.py` / `app.py` (stored status on replay), `tests/test_story_13_*.py` / helpers

## Verification commands

```bash
cd doge-ai-bridge && ./scripts/start-disposable-pg.sh
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "story_13 or dedupe or pg_runtime" --maxfail=10
```
