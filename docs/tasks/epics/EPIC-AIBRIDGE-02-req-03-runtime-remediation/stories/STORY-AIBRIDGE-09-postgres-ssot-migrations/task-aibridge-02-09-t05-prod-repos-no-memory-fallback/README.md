# Task: implement — production repos no memory fallback

**Status:** Done  
**Skill declared:** postgres-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md`  
**Parent story:** [`STORY-AIBRIDGE-09-postgres-ssot-migrations.md`](../STORY-AIBRIDGE-09-postgres-ssot-migrations.md)  
**P3 Done:** 2026-09-13T15:25:46Z
**P1 scaffold:** 2026-09-13T15:16:41Z  
**Maps:** Scope #5; AC #5

## Purpose

SessionStore / confirm / token / history on runtime path with no silent memory fallback in production.

## Code Facts (verified exists — P1)

1. Memory/in-process stores used today for dedupe/confirm.
2. sessions.py / registry.py have PG pieces but boot CREATE TABLE.

## AC/DoD

- [x] Production config refuses silent memory-only path.
- [x] Tests assert fail-closed.
- [x] Skill declared: postgres-pro present.

## Where to change

- sessions.py, confirm.py, action_tokens.py, history.py, app factory

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q  # after P3
```
