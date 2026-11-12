# Task: implement — `_apply_deployment_to_engine` helper (ADR-1)

**Status:** Done  
**Skill declared:** python-pro  
**Composition note:** fastapi-expert (create_app composition slice)  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`  
**Parent story:** [`STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`](../STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md)  
**P1 scaffold:** 2026-09-16T12:04:31Z  
**Maps:** Scope #1 · TECH ADR-1

## Purpose

Add `_apply_deployment_to_engine(engine, deployment, settings)` (or equivalent next to `create_app`) that mutates the existing `InterviewEngine` from a ready `DeploymentBundleState` — **no** new service layer, **no** full `create_app` reorder.

## Code Facts (verified exists — post P3 / P6 G-02)

1. Helper: `_apply_deployment_to_engine` `src/aibridge/app.py:196–230` (sets prefix + assembled instructions).
2. Defaults still on engine type: `instructions=""`, `tools=[]`, `prompt_channel="prefix"`: `src/aibridge/interview.py:42–50` (overwritten by helper when deploy ready).
3. Deploy state + optional `strict_tool`: `src/aibridge/deployment.py`.
4. Assembled text on loaded bundle: `src/aibridge/content.py`.
5. ADR-1: engine ctor before `_init_stores` (~327 vs ~420); **no** full create_app reorder.

## AC/DoD

- [x] Helper exists and sets `prompt_channel="prefix"`, `instructions` from `deployment.loaded.assembled_instructions` when ready/loaded.
- [x] Does not invent a second prompt channel or reorder stores-before-engine.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/app.py` (helper beside `create_app`); read-only consume `deployment.py` / `interview.py` types.

## Verification commands

```bash
rg -n "_apply_deployment_to_engine|assembled_instructions" doge-ai-bridge/src/aibridge/app.py
rg -n "prompt_channel|instructions" doge-ai-bridge/src/aibridge/interview.py | head -20
```
