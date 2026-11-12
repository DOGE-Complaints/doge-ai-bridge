# Task: implement — DB one-active-turn lock

**Status:** Done  
**Skill declared:** postgres-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md`  
**Parent story:** [`STORY-AIBRIDGE-09-postgres-ssot-migrations.md`](../STORY-AIBRIDGE-09-postgres-ssot-migrations.md)  
**P3 Done:** 2026-09-13T15:25:46Z
**P1 scaffold:** 2026-09-13T15:16:41Z  
**Maps:** Scope #3; AC #2/#4

## Purpose

Database-backed one active turn per session (replace in-process exclusivity for production).

## Code Facts (verified exists — P1)

1. turn_lock / session path in-process today.
2. confirm._sessions in-process.

## AC/DoD

- [x] Two concurrent same-session attempts → one wins via DB constraints/txn.
- [x] Skill declared: postgres-pro present.

## Where to change

- session/turn lock persistence

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q  # after P3
```
