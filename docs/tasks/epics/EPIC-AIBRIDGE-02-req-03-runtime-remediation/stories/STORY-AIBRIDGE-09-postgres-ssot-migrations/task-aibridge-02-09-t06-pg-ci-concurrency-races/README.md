# Task: implement — disposable Postgres CI + race tests

**Status:** Done  
**Skill declared:** postgres-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md`  
**Parent story:** [`STORY-AIBRIDGE-09-postgres-ssot-migrations.md`](../STORY-AIBRIDGE-09-postgres-ssot-migrations.md)  
**P3 Done:** 2026-09-13T15:25:46Z
**P1 scaffold:** 2026-09-13T15:16:41Z  
**Maps:** Scope #6; AC #4

## Purpose

Postgres row factory; disposable Postgres CI; transactional concurrency race tests (two messages/callbacks same session).

## Code Facts (verified exists — P1)

1. pytest suite exists; disposable PG CI for aibridge Unknown/partial (P1).
2. Multi-replica load out of scope (18).

## AC/DoD

- [x] Disposable PG harness works.
- [x] Race tests pass; constraints win.
- [x] Skill declared: postgres-pro present.

## Where to change

- test harness + CI under doge-ai-bridge/

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q  # after P3
```
