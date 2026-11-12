# Task: test — T-COMPAT-06 supported-constraints assert (G-02)

**Status:** Done · 2026-09-24T11:08:43Z  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_41_audit_20260924`  
**Gap:** G-02 (Low) — P4 audit 2026-09-24 → **CLOSED**  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-41-openai-schema-projection-20260924.md`  
**Parent story:** [`STORY-AIBRIDGE-41-openai-schema-projection.md`](../STORY-AIBRIDGE-41-openai-schema-projection.md)  
**P5 scaffold:** 2026-09-24T11:06:43Z  
**P6 closed:** 2026-09-24T11:08:43Z  
**Maps:** G-02 · T-COMPAT-06 · REQ-07 §11.1

## Purpose

Add explicit T-COMPAT-06 coverage: after projection, supported constraints on canonical houses (e.g. `minItems`) remain; `uniqueItems` absent.

**Out of this task:** keyword-helper align (t05); Gate 2 uniqueItems enforcement; live TG invent.

## AC/DoD

- [x] Explicit assert: projected houses keep supported constraint(s) (e.g. `minItems`); no `uniqueItems` keyword.
- [x] t03 acceptance (or this task AV) names T-COMPAT-06.
- [x] Suite green under filter; no invent live TG / OpenAI network SUCCESS.
- [x] `Skill declared: python-pro` present.

## Where changed

- `tests/test_openai_schema_projection.py` — `test_t_compat_06_supported_constraints_survive`
- this AV names T-COMPAT-06
