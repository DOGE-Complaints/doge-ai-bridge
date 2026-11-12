# Task: Dockerfile — COPY docs/openapi into image

**Status:** Done  
**Skill declared:** devops-engineer  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-21-oas-image-env-docs.md`  
**Parent story:** [`STORY-AIBRIDGE-21-oas-image-env-docs.md`](../STORY-AIBRIDGE-21-oas-image-env-docs.md)  
**P1 scaffold:** 2026-09-16T12:52:52Z
**P3 Done:** 2026-09-16T12:55:52Z  
**Maps:** Scope #1 · TECH ADR-3 · REQ-05 §4.4

## Purpose

Add `COPY docs/openapi ./docs/openapi` (or equivalent) to root `Dockerfile` so both YAML contracts land under `/app/docs/openapi/` without manual mount.

**Out of this task:** inventing OAS content; putting OAS under `src/instructions/`; Railpack redesign; env/runbook docs (t02/t03).

## Code Facts (verified exists — P1)

1. Dockerfile currently `COPY src` + `COPY migrations` only: `Dockerfile:10–12`.
2. WORKDIR `/app` (`Dockerfile:4`).
3. Both OAS files exist: `docs/openapi/story-intake-actions.openapi.yaml`, `docs/openapi/aibridge-channel-v1.openapi.yaml`.

## AC/DoD

- [x] Dockerfile copies `docs/openapi/` (both YAMLs) into the image tree.
- [x] No OAS under `src/instructions/`.
- [x] `Skill declared: devops-engineer` present.

## Where to change

- `Dockerfile` (P3)

## Verification commands

```bash
rg -n 'COPY docs/openapi|COPY src|COPY migrations' doge-ai-bridge/Dockerfile
ls -1 doge-ai-bridge/docs/openapi/
```
