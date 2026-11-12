# Task: docs — Phase A pins in `.env.example`

**Status:** Done  
**Skill declared:** devops-engineer  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-21-oas-image-env-docs.md`  
**Parent story:** [`STORY-AIBRIDGE-21-oas-image-env-docs.md`](../STORY-AIBRIDGE-21-oas-image-env-docs.md)  
**P1 scaffold:** 2026-09-16T12:52:52Z
**P3 Done:** 2026-09-16T12:55:52Z  
**Maps:** Scope #4 · REQ-05 §4.3 · TECH §9

## Purpose

Document Phase A env pins in `.env.example`: local relative paths vs image `/app/...` notes; `DOGESTONIA_OPENAPI_PATH` = Story Intake wire; SCHEMA_ID/VERSION `uus_veerenni_civic` / `v3`. No new aliases.

**Out of this task:** inventing secrets; Dockerfile COPY (t01); runbook body (t03); product runtime code.

## Code Facts (verified exists — P1)

1. `.env.example` exists at repo root.
2. TECH §9 env map lists INSTRUCTIONS_DIR/MANIFEST, OPENAPI_PATH (story-intake), PAYLOAD_SCHEMA_PATH, SCHEMA_ID/VERSION, CONTENT_SOURCE_COMMIT, TOOL_SCHEMA_PATH.
3. Soft consistency with STORY-20 MANIFEST path examples.

## AC/DoD

- [x] Phase A pin block present in `.env.example` (local + `/app` note).
- [x] OPENAPI_PATH documents story-intake wire only; SCHEMA_ID/VERSION uus_veerenni_civic/v3.
- [x] No new env aliases invented.
- [x] `Skill declared: devops-engineer` present.

## Where to change

- `.env.example` (P3)

## Verification commands

```bash
rg -n 'DOGESTONIA_OPENAPI_PATH|DOGESTONIA_SCHEMA_ID|DOGESTONIA_SCHEMA_VERSION|Phase A|/app/docs/openapi' doge-ai-bridge/.env.example
```
