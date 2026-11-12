# Task: fix — envelope schema_version stamp + assert (G-01 / G-03)

**Status:** Done · P6 2026-09-24T11:43:20Z  
**Skill declared:** python-pro  
**Composition:** fastapi-expert  
**Wave:** `run_mode=aibridge_43_audit_20260924`  
**Gap:** G-01 (Medium) · G-03 (Low) — P4 audit 2026-09-24 → **CLOSED**  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-43-validation-context-bind-readyz-20260924.md`  
**Parent story:** [`STORY-AIBRIDGE-43-validation-context-bind-readyz.md`](../STORY-AIBRIDGE-43-validation-context-bind-readyz.md)  
**P5 scaffold:** 2026-09-24T11:41:37Z  
**P6 closed:** 2026-09-24T11:43:20Z  
**Maps:** G-01 · G-03 · Gate 3 envelope · `ServerConstants`

## Purpose

Fix `_bind_validation_context` so `constants.schema_version` is the Story Intake envelope default `m2.story_intake_envelope.v2` (not pack `DOGESTONIA_SCHEMA_VERSION`). Keep pack version only in `schema_version_pack`. Add bind-test assert `vc.constants.schema_version == "m2.story_intake_envelope.v2"` (G-03).

**Out of this task:** backlog Verified sync (t06); invent live TG / REQ-04; alternate ValidationContext dataclass.

## AC/DoD

- [x] `constants.schema_version` = `m2.story_intake_envelope.v2` (envelope), not pack `v1`.
- [x] `schema_version_pack` still carries pack version from env.
- [x] Test asserts envelope constant on bound VC.
- [x] Existing VC bind / readyz suite still green under filter.
- [x] `Skill declared: python-pro` present (+ Composition `fastapi-expert`).

## Where changed (P6)

- `src/aibridge/app.py` — `_bind_validation_context` ServerConstants stamp
- `tests/test_validation_context_bind.py` — envelope assert
