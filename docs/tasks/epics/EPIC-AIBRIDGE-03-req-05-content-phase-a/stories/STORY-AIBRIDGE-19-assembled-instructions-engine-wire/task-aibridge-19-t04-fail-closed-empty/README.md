# Task: implement — fail-closed empty assembled / not-ready deploy

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`  
**Parent story:** [`STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`](../STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md)  
**P1 scaffold:** 2026-09-16T12:04:31Z  
**Maps:** Scope #4 · Target #3 · ADR-1 fail-closed

## Purpose

When `content_configured()` and deploy is not ready or `assembled_instructions` is empty, do **not** silently serve an empty stable prefix — fail-closed via existing readiness / deployment error path (`deployment.error` / content reasons). HTTP may still bind for `/healthz`; `/readyz` 503.

## Code Facts (verified exists — post P3 / P6 G-02)

1. `content_configured()`: `src/aibridge/config.py`.
2. `/readyz` → `evaluate_readiness(cfg, dep)`: `src/aibridge/app.py` (readyz handler).
3. Helper fail-closed: empty/whitespace assembled → `DeploymentBundleState(error="assembled_instructions_empty")` `app.py:196–230`; engine instructions not overwritten to empty.
4. Engine type default `instructions=""` remains for non-content boots: `interview.py:44`.

## AC/DoD

- [x] content_configured + empty/not-ready does not leave a ready interview path with silent empty instructions.
- [x] Uses existing readiness/deployment error surfaces (no invent channel OAS errors).
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/app.py` helper/wire; possibly readiness evaluation already owning content reasons — extend only if needed.

## Verification commands

```bash
rg -n "content_configured|evaluate_readiness|deployment.error" doge-ai-bridge/src/aibridge --glob '*.py' | head -40
```
