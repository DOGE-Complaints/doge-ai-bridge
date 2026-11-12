# Task: docs — audit G-02 runbook make + railpack 8080

**Status:** Done · P6 2026-09-26T12:20:13Z · G-02 **CLOSED**  
**Skill declared:** python-pro · soft devops-engineer  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack-20260926.md` · G-02  
**Parent story:** [`STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md`](../STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md)  
**P5 scaffold:** 2026-09-26T12:18:29Z  
**P6 closed:** 2026-09-26T12:20:13Z  
**Maps:** runbook G1/G3 align

## Purpose

Align `docs/runbooks/aibridge-web-service-local-railway.md` to post-P3: primary `make serve`/`dev`; Railpack `${PORT:-8080}`.

## AC/DoD

- [x] Runbook documents `make serve` / `make dev` as primary local start.
- [x] Railpack fallback documented as `${PORT:-8080}` (not 8000).
- [x] No invent Railway live SUCCESS; no probe/env hard-cut scope creep.
- [x] `Skill declared: python-pro` present.

## Where changed

- `docs/runbooks/aibridge-web-service-local-railway.md`

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-req9-01-t06-audit-g02-runbook-make-railpack-8080.md`](./acceptance-verification-task-aibridge-req9-01-t06-audit-g02-runbook-make-railpack-8080.md)
