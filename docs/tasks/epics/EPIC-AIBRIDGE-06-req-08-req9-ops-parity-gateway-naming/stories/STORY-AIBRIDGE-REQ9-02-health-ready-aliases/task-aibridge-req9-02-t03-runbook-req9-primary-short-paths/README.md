# Task: docs — runbooks REQ9-primary /health /ready

**Status:** Done · P3 2026-09-26T12:27:23Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md`  
**Parent story:** [`STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md`](../STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md)  
**P1 scaffold:** 2026-09-26T12:24:30Z  
**P3 closed:** 2026-09-26T12:27:23Z  
**Maps:** REQ-08 G2 docs · story Scope runbooks

## Purpose

Update docs/runbooks that cite only `z` paths so short paths `/health` `/ready` are listed as **REQ9-primary** (z OK as alias). At minimum: `docs/runbooks/aibridge-web-service-local-railway.md`; align pilot runbook probe citations where they are operator-facing for aibridge probes.

## AC/DoD

- [x] Web-service runbook lists `/health` `/ready` as REQ9-primary (z as alias OK).
- [x] Operator-facing probe curl/checklists updated where they cited z-only for aibridge.
- [x] No readiness-logic or Makefile/env invent.
- [x] `Skill declared: python-pro` present.

## Where changed

- `docs/runbooks/aibridge-web-service-local-railway.md`
- `docs/runbooks/AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md`

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-req9-02-t03-runbook-req9-primary-short-paths.md`](./acceptance-verification-task-aibridge-req9-02-t03-runbook-req9-primary-short-paths.md)
