# Task: implement — uniqueness + gateway-attempt constraints

**Status:** Done  
**Skill declared:** postgres-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md`  
**Parent story:** [`STORY-AIBRIDGE-09-postgres-ssot-migrations.md`](../STORY-AIBRIDGE-09-postgres-ssot-migrations.md)  
**P3 Done:** 2026-09-13T15:25:46Z
**P1 scaffold:** 2026-09-13T15:16:41Z  
**Maps:** Scope #2; AC #2

## Purpose

Unique (channel, event_id), action token hash, (session_id, call_id); ≤1 gateway attempt per authorized revision; failed txn does not advance history/FSM.

## Code Facts (verified exists — P1)

1. dedupe.py EventDedupeStore in-process.
2. action_tokens.py on disk.
3. confirm/history modules present.

## AC/DoD

- [x] DB constraints enforced fail-closed.
- [x] Failed txn does not advance history/FSM.
- [x] Skill declared: postgres-pro present.

## Where to change

- schema + dedupe.py, action_tokens.py, gateway attempt store

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q  # after P3
```
