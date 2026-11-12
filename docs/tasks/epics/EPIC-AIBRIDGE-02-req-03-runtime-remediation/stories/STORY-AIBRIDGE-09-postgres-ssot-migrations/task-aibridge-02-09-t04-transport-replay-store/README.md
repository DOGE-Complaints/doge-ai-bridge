# Task: implement — transport replay store (HTTP status + body)

**Status:** Done  
**Skill declared:** postgres-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md`  
**Parent story:** [`STORY-AIBRIDGE-09-postgres-ssot-migrations.md`](../STORY-AIBRIDGE-09-postgres-ssot-migrations.md)  
**P3 Done:** 2026-09-13T15:25:46Z
**P1 scaffold:** 2026-09-13T15:16:41Z  
**Maps:** Scope #4; AC #3

## Purpose

Persist event dedupe with stored HTTP status + response body for restart/instance replay (REQ-03 AC #2).

## Code Facts (verified exists — P1)

1. In-process EventDedupeStore — no HTTP status/body persistence.
2. REQ-03 §3 transport replay terms.

## AC/DoD

- [x] After restart, replay returns previously stored status + body.
- [x] No live OpenAI in this task.
- [x] Skill declared: postgres-pro present.

## Where to change

- Postgres-backed dedupe/replay; channel/gateway wiring as needed

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q  # after P3
```
