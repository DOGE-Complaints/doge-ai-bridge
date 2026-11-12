# Task: implement — Gate 2 uniqueItems enforcement

**Status:** Done · P3 2026-09-24T11:17:36Z  

**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md`  
**Parent story:** [`STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md`](../STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md)  
**P1 scaffold:** 2026-09-24T11:13:54Z  
**Maps:** AIB-COMPAT-04/05 · §9.1 · TECH-ARCH §2.3

## Purpose

Add `uniqueItems` to the canonical validator keyword set (`FULL_SCHEMA_KEYWORDS` or equivalent). Enforce JSON Schema `uniqueItems: true` on Gate 2 path (`validate_gate2_pack_payload` / `_validate_type`): structural equality; object key order independent. `uniqueItems: false` / absent → no uniqueness restriction. Always validate against untouched canonical pack schema (not OpenAI projection).

**Out of this task:** `schema_validation_complete` prove (t02); T-UNIQUE tests (t03); story gate (t04); STORY-41/43/45 invent.

## AC/DoD

- [x] `uniqueItems` in supported validation keywords.
- [x] Gate 2 rejects structurally duplicate array items when `uniqueItems: true`.
- [x] Key-order-independent object equality; false/absent keyword does not reject duplicates.
- [x] `Skill declared: python-pro` present.

## Where to change (execute — not P1)

- `src/aibridge/request_assembly.py` — **P3**
