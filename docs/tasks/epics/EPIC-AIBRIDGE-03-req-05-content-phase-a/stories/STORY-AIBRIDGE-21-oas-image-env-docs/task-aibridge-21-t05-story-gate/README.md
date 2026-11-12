# Task: story gate — REQ-05 §4.3–4.4 AC

**Status:** Done  
**Skill declared:** devops-engineer  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-21-oas-image-env-docs.md`  
**Parent story:** [`STORY-AIBRIDGE-21-oas-image-env-docs.md`](../STORY-AIBRIDGE-21-oas-image-env-docs.md)  
**P1 scaffold:** 2026-09-16T12:52:52Z
**P3 Done:** 2026-09-16T12:55:52Z  
**Maps:** Target / AC §4.3–4.4

## Purpose

Story acceptance gate: confirm openapi dir in image (Dockerfile COPY), OPENAPI_PATH = Story Intake, Phase A pins documented in `.env.example` + web runbook (SCHEMA_ID/VERSION uus_veerenni_civic/v3). Write `acceptance-verification-task-aibridge-21-t05-story-gate.md` after live verify in P3 (not in P1).

**Out of this task:** product invent; REQ-06; story 22 proof.

## Code Facts (verified exists — P1)

1. AC from `$storyFile` Target (two checkboxes).
2. Upstream t01–t04 deliver Dockerfile, env, runbook, path contract.
3. Gate Date: only after live verify in P3 session.

## AC/DoD

- [x] REQ-05 §4.4: openapi dir in image; OPENAPI_PATH = Story Intake — evidenced.
- [x] REQ-05 §4.3: documented pins incl. SCHEMA_ID/VERSION — evidenced.
- [x] Acceptance verification artifact PASS with live Date.
- [x] `Skill declared: devops-engineer` present.

## Where to change

- This folder: `acceptance-verification-task-aibridge-21-t05-story-gate.md` (P3)
- Pipeline / backlog AC checkboxes (P3)

## Verification commands

```bash
rg -n 'COPY docs/openapi' doge-ai-bridge/Dockerfile
rg -n 'DOGESTONIA_OPENAPI_PATH|uus_veerenni_civic' doge-ai-bridge/.env.example doge-ai-bridge/docs/runbooks/aibridge-web-service-local-railway.md
```
