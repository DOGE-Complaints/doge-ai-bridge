# Task: test — negative uniqueItems completeness prove (G-02)

**Status:** Done · P6 2026-09-24T11:25:01Z  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_42_audit_20260924`  
**Gap:** G-02 (Low) — P4 audit 2026-09-24 → **CLOSED**  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-42-canonical-uniqueitems-validation-20260924.md`  
**Parent story:** [`STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md`](../STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md)  
**P5 scaffold:** 2026-09-24T11:22:57Z  
**P6 closed:** 2026-09-24T11:25:01Z  
**Maps:** G-02 · `schema_validation_complete` · readiness fail-closed

## Purpose

Add negative prove: when uniqueItems enforcement is broken (monkeypatch / stub), `schema_validation_complete()` returns `False` and readiness surfaces `schema_validation_incomplete*` (or equivalent reason). Suite currently only asserts `schema_validation_complete() is True`.

**Out of this task:** AC-04 docs soften (t05); invent VC bind (STORY-43); live TG; pack JSON rewrite.

## AC/DoD

- [x] Negative test: broken uniqueItems → `schema_validation_complete() is False`.
- [x] Doc note: readiness maps False → `schema_validation_incomplete` (`readiness.py`).
- [x] Existing T-UNIQUE / request_assembly suite still green under filter (**17 passed**).
- [x] No invent live TG / Railway / VC bind.
- [x] `Skill declared: python-pro` present.

## Where changed

- `tests/test_uniqueitems_gate2.py` — `test_schema_validation_complete_false_when_uniqueitems_broken`
