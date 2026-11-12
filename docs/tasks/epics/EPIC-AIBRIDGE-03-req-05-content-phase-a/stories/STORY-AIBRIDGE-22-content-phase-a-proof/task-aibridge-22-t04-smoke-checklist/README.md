# Task: docs — ops smoke checklist `req-05-phase-a-smoke.md`

**Status:** Done  
**P3 closed:** 2026-09-16T13:41:13Z  

**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-22-content-phase-a-proof.md`  
**Parent story:** [`STORY-AIBRIDGE-22-content-phase-a-proof.md`](../STORY-AIBRIDGE-22-content-phase-a-proof.md)  
**P1 scaffold:** 2026-09-16T13:36:35Z  
**Maps:** Scope #3 · TECH ADR-4 ops smoke · REQ-05 §4.5

## Purpose

Create `docs/ops/req-05-phase-a-smoke.md`: `/healthz` 200; full Phase A env → `/readyz` not `content_bundle_not_ready` due to OAS/manifest/wiring. Checklist only — **no** invent Railway SUCCESS.

**Out of this task:** live deploy invent; n8n/Telegram; pytest (t01–t03).

## Code Facts (verified exists — P1)

1. Named path **missing** until P3: `docs/ops/req-05-phase-a-smoke.md`.
2. Endpoints: `/healthz`, `/readyz` in `app.py`.
3. Phase A pins documented in `.env.example` / web runbook (STORY-21).

## AC/DoD

- [x] File exists at `docs/ops/req-05-phase-a-smoke.md`.
- [x] Checks include healthz 200 and readyz not failing for OAS/manifest/wiring when env complete.
- [x] No Railway SUCCESS claim invented.
- [x] `Skill declared: test-master` present.

## Where to change

- `docs/ops/req-05-phase-a-smoke.md` — **P3**

## Verification commands

```bash
test -f doge-ai-bridge/docs/ops/req-05-phase-a-smoke.md && rg -n 'healthz|readyz|content_bundle_not_ready' doge-ai-bridge/docs/ops/req-05-phase-a-smoke.md
```
