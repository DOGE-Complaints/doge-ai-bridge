# STORY-AIBRIDGE-43 — Minimal ValidationContext bind + readiness

## Meta
- **Key:** `STORY-AIBRIDGE-43-validation-context-bind-readyz`
- **Status:** P6 Done · G-01/G-02/G-03 CLOSED · next P7 · pkg-000042 · 2026-09-24T11:43:20Z
- **Parent REQ:** [`REQ-07`](../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §5 ValidationContext · AIB-COMPAT-05/07/08
- **Tech-arch:** [`TECH-ARCH-REQ-07`](../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §2.3–2.4 · operator two-stage DoD
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [41](STORY-AIBRIDGE-41-openai-schema-projection.md) · [42](STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md) · [44](STORY-AIBRIDGE-44-compat-merge-gate-proof.md) · [45](STORY-AIBRIDGE-45-compat-live-telegram-verify.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)  
  Composition: `fastapi-expert` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/fastapi-expert/SKILL.md)
- **Emitted:** 2026-09-24T10:28:49Z

## Scope
- In `create_app` composition: bind `ConfirmationGuard.validation_context` with dual schemas when content/schema tooling is configured:
  - `tool_parameters` ← projected `strict_tool["parameters"]` (Gate 1)
  - `pack_schema` ← canonical pack JSON (Gate 2)
  - `wire_schema` ← Story Intake request body schema (Gate 3)
  - `constants` ← `ServerConstants` / env stamps
- Prefer existing `coordinator.ValidationContext` field shape.
- `/readyz` not_ready if ValidationContext missing or invalid when gates are required.
- **Target readiness reason (materialize default):** `validation_context_not_bound` (stable, non-secret; adjust only if existing convention conflicts — document in gate notes).

## Out of scope
- Full REQ-04 confirm/FSM/token hardening beyond this bind; new public HTTP APIs; inventing alternate dataclass unless forced by tests.

## Verified current state
- `ValidationContext` defined (`src/aibridge/coordinator.py`); `validate_function_calls` requires it or raises `schemas not configured`.
- P3+ bind: `create_app` → `_bind_validation_context` sets `ConfirmationGuard.validation_context` when content configured + ready deployment with `strict_tool` (dual schemas + `ServerConstants`).
- `/readyz` fail-closed with reason `validation_context_not_bound` when VC missing/invalid and content configured.
- `ConfirmationGuard.validation_context` field exists (`confirm.py`).
- Envelope stamp: `constants.schema_version` = `m2.story_intake_envelope.v2`; pack version in `schema_version_pack` only (P6 G-01).

## Target / AC
- [x] Dual Gate contract wired in production composition (TECH-ARCH §2.3–2.4).
- [x] Missing/invalid VC → `/readyz` not_ready with stable reason (default `validation_context_not_bound`).
- [x] AC-06 partial: no silent accept of consequential FC without schemas when content configured.

## Code points
- `src/aibridge/app.py` (`create_app`, `_apply_deployment_to_engine`)
- `src/aibridge/confirm.py`, `coordinator.py`, `readiness.py`

## Dependencies
- Requires **41** and **42** (projected tool + canonical uniqueness available)
