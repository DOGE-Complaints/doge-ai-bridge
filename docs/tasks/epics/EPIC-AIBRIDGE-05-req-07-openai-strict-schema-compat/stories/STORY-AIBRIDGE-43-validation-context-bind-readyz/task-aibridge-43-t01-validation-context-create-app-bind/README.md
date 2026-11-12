# Task: implement — ValidationContext create_app bind

**Status:** Done · P3 2026-09-24T11:33:03Z  

**Skill declared:** python-pro  
**Composition:** fastapi-expert  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-43-validation-context-bind-readyz.md`  
**Parent story:** [`STORY-AIBRIDGE-43-validation-context-bind-readyz.md`](../STORY-AIBRIDGE-43-validation-context-bind-readyz.md)  
**P1 scaffold:** 2026-09-24T11:30:36Z  
**P3 closed:** 2026-09-24T11:33:03Z  
**Maps:** TECH-ARCH §2.3–2.4 · AIB-COMPAT-05 · REQ-07 §5

## Purpose

In `create_app` / `_apply_deployment_to_engine` composition: bind `ConfirmationGuard.validation_context` with dual schemas when content/schema tooling is configured:

- `tool_parameters` ← projected `strict_tool["parameters"]` (Gate 1)
- `pack_schema` ← canonical pack JSON (Gate 2)
- `wire_schema` ← Story Intake request body schema (Gate 3)
- `constants` ← `ServerConstants` / env stamps

Prefer existing `coordinator.ValidationContext` field shape — **no** invent alternate dataclass / new public HTTP APIs.

**Out of this task:** readyz fail-closed (t02); tests (t03); story gate (t04); REQ-04 full hardening; live TG.

## AC/DoD

- [x] `ConfirmationGuard.validation_context` set when content configured.
- [x] Dual schemas + `ServerConstants` populated per Gate 1/2/3 contract.
- [x] Existing `ValidationContext` dataclass reused.
- [x] `Skill declared: python-pro` present (+ Composition `fastapi-expert`).

## Where changed

- `src/aibridge/app.py` — `_bind_validation_context` after `_apply_deployment_to_engine`
- `src/aibridge/coordinator.py` — `build_validation_context`, `validation_context_is_bound`
- `src/aibridge/tool_gen.py` — `load_wire_request_schema`
