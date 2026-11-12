# Task: implement — /readyz ValidationContext fail-closed

**Status:** Done · P3 2026-09-24T11:33:03Z  

**Skill declared:** python-pro  
**Composition:** fastapi-expert  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-43-validation-context-bind-readyz.md`  
**Parent story:** [`STORY-AIBRIDGE-43-validation-context-bind-readyz.md`](../STORY-AIBRIDGE-43-validation-context-bind-readyz.md)  
**P1 scaffold:** 2026-09-24T11:30:36Z  
**P3 closed:** 2026-09-24T11:33:03Z  
**Maps:** AIB-COMPAT-07/08 · TECH-ARCH §2.4 · readiness

## Purpose

When gates are required (content/schema tooling configured): `/readyz` returns not_ready if `ValidationContext` is missing or invalid. **Default reason token:** `validation_context_not_bound` (stable, non-secret). Adjust only if existing convention conflicts — document in gate notes. Must not call OpenAI or write gateway (AIB-COMPAT-08).

**Out of this task:** create_app bind (t01); tests (t03); story gate (t04); invent live TG.

## AC/DoD

- [x] Missing/invalid VC → `/readyz` not_ready when gates required.
- [x] Stable reason `validation_context_not_bound` (no rename needed).
- [x] No OpenAI call / gateway write from readiness path.
- [x] `Skill declared: python-pro` present (+ Composition `fastapi-expert`).

## Where changed

- `src/aibridge/readiness.py` — `evaluate_readiness(..., validation_context=)`
- `src/aibridge/app.py` — `/readyz` passes `guard.validation_context`
