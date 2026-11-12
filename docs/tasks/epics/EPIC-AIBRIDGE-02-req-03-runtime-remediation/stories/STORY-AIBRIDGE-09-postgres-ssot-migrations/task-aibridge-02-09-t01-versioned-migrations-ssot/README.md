# Task: implement — versioned migrations SSOT

**Status:** Done  
**Skill declared:** postgres-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md`  
**Parent story:** [`STORY-AIBRIDGE-09-postgres-ssot-migrations.md`](../STORY-AIBRIDGE-09-postgres-ssot-migrations.md)  
**P3 Done:** 2026-09-13T15:25:46Z
**P1 scaffold:** 2026-09-13T15:16:41Z  
**Maps:** Scope #1; AC #1

## Purpose

Versioned migrations sole production schema; forbid boot-only CREATE TABLE IF NOT EXISTS as production path.

## Code Facts (verified exists — P1)

1. Arch/REQ-03 §5.3 schema SSOT — REQ-03.
2. Boot CREATE TABLE IF NOT EXISTS — sessions.py, registry.py.
3. No versioned migrations tree under doge-ai-bridge yet (P1).

## AC/DoD

- [x] Versioned migrations applied on production path.
- [x] Boot schema-only CREATE TABLE IF NOT EXISTS not production-acceptable.
- [x] Skill declared: postgres-pro present.

## Where to change

- migrations tree + sessions.py / registry.py boot path

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q  # after P3
```
