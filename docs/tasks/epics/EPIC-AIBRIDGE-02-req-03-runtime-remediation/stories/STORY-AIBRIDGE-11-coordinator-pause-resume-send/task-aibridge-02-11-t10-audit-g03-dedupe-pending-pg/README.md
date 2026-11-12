# Task: implement — claim-or-insert turn dedupe + PG pending restart (G-03)

**Status:** Done  
**Skill declared:** fastapi-expert  
**Wave:** `run_mode=aibridge_11_audit_20260913`  
**Gap:** G-03 (Info) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-11-coordinator-pause-resume-send-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`](../STORY-AIBRIDGE-11-coordinator-pause-resume-send.md)  
**P5 scaffold:** 2026-09-13T16:07:28Z
**P6 Done:** 2026-09-13T16:12:58Z

## Purpose

(a) `process_turn_async`: claim/insert dedupe **before** Responses engine so concurrent same `event_id` does not double-call.  
(b) Disposable-PG (or skipif) test: pending confirm fields survive ConfirmSessionStore round-trip / restart hydrate.

## AC/DoD

- [x] Async turn path claims event before `arun_turn`; loser does not call engine.
- [x] PG (or skipif) pending `call_id`/frozen/replay round-trip via `PostgresConfirmSessionStore`.
- [x] `Skill declared: fastapi-expert` present.

## Where to change

`src/aibridge/dedupe.py`, `channel.py`, `pg_runtime.py` (if needed), tests

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k 'dedupe or pending or claim or g03'
```
