# Task: docs — Phase A pins in web-service runbook

**Status:** Done  
**Skill declared:** devops-engineer  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-21-oas-image-env-docs.md`  
**Parent story:** [`STORY-AIBRIDGE-21-oas-image-env-docs.md`](../STORY-AIBRIDGE-21-oas-image-env-docs.md)  
**P1 scaffold:** 2026-09-16T12:52:52Z
**P3 Done:** 2026-09-16T12:55:52Z  
**Maps:** Scope #4 · REQ-05 §4.3 · TECH §9

## Purpose

Document the same Phase A pins in `docs/runbooks/aibridge-web-service-local-railway.md` (local + Railway/image `/app` paths). Align with `.env.example` (t02); no new aliases.

**Out of this task:** inventing secrets; Dockerfile (t01); rewriting channel OAS; REQ-06 CI.

## Code Facts (verified exists — P1)

1. Runbook exists: `docs/runbooks/aibridge-web-service-local-railway.md`.
2. Pins SSOT: TECH §9 + REQ-05 §4.3.
3. OPENAPI_PATH must remain Story Intake wire, not channel façade.

## AC/DoD

- [x] Runbook documents Phase A pins incl. OPENAPI_PATH = story-intake and SCHEMA_ID/VERSION uus_veerenni_civic/v3.
- [x] Local vs `/app` path notes present; no new aliases.
- [x] `Skill declared: devops-engineer` present.

## Where to change

- `docs/runbooks/aibridge-web-service-local-railway.md` (P3)

## Verification commands

```bash
rg -n 'DOGESTONIA_OPENAPI_PATH|story-intake-actions|SCHEMA_ID|uus_veerenni_civic|/app/docs/openapi' doge-ai-bridge/docs/runbooks/aibridge-web-service-local-railway.md
```
