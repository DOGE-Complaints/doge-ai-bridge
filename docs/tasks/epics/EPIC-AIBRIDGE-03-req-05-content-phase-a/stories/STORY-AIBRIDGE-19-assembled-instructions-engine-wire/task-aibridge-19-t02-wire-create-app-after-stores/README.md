# Task: implement — wire helper after `deployment_bundle` in `create_app`

**Status:** Done  
**Skill declared:** python-pro  
**Composition note:** fastapi-expert  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`  
**Parent story:** [`STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`](../STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md)  
**P1 scaffold:** 2026-09-16T12:04:31Z  
**Maps:** Scope #1 · ADR-1 wire point

## Purpose

Call `_apply_deployment_to_engine(...)` immediately after `app.state.deployment_bundle = deployment` so the same engine instance used for turns receives assembled instructions without reordering store init before engine construction.

## Code Facts (verified exists — post P3 / P6 G-02)

1. `_init_stores` + assign `deployment_bundle`: `src/aibridge/app.py:420–429`.
2. Helper invoke immediately after: `app.py:429–433`.
3. Engine construction precedes stores: `app.py:~327` (ADR-1 — no full reorder).
4. TECH ADR-1 rejects full reorder of `create_app` for Phase A.

## AC/DoD

- [x] Helper invoked once after `deployment_bundle` assignment on the live `engine` reference used by the app.
- [x] No silent skip when content is configured and deploy is ready (pair with t04).
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/app.py` (`create_app` after stores init).

## Verification commands

```bash
rg -n "deployment_bundle|_apply_deployment_to_engine|_init_stores" doge-ai-bridge/src/aibridge/app.py
```
