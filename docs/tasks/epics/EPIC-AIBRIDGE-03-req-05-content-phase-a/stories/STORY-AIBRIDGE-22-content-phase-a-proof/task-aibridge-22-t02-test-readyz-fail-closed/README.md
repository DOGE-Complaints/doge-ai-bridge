# Task: test — missing/broken content → `/readyz` 503

**Status:** Done  
**P3 closed:** 2026-09-16T13:41:13Z  

**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-22-content-phase-a-proof.md`  
**Parent story:** [`STORY-AIBRIDGE-22-content-phase-a-proof.md`](../STORY-AIBRIDGE-22-content-phase-a-proof.md)  
**P1 scaffold:** 2026-09-16T13:36:35Z  
**Maps:** Scope #2 · TECH ADR-4 fail-closed

## Purpose

Pytest: broken/missing instruction path or incomplete content config → `/readyz` 503 (or `deployment_bundle.ready` false); no silent empty prompt on content_configured production path.

**Out of this task:** inventing Railway SUCCESS; changing readiness schema beyond existing fail-closed.

## Code Facts (verified exists — P1)

1. Readiness: `src/aibridge/readiness.py`.
2. `/readyz` route in `src/aibridge/app.py`.
3. Prior patterns: story-19 fail-closed assembled path tests.

## AC/DoD

- [x] Test: broken/missing content → not_ready / 503 with content-related reason.
- [x] No silent empty prefix when content is configured but broken.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/` — **P3**

## Verification commands

```bash
rg -n 'readyz|content_bundle_not_ready|not_ready' doge-ai-bridge/src/aibridge/readiness.py doge-ai-bridge/tests/
```
