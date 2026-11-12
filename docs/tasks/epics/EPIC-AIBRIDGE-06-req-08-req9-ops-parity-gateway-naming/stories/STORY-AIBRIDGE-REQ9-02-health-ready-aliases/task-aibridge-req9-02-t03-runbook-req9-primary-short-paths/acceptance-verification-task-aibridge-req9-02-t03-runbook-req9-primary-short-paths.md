# Acceptance — task-aibridge-req9-02-t03-runbook-req9-primary-short-paths

| Field | Value |
|-------|-------|
| **Date** | 2026-09-26T12:26:24Z |
| **Result** | **Done** |

## Disk facts

| Claim | Evidence |
|-------|----------|
| Web runbook REQ9-primary | `docs/runbooks/aibridge-web-service-local-railway.md` — `/health` `/ready` primary; z as alias |
| Smoke curls | §1.4 uses `/health` `/ready` |
| Checklist | §4 `GET /health` / optional `GET /ready` |
| Pilot probes | `AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md` Health/Readiness + checklists updated |
