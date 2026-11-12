# Task: implement — schema_validation_complete uniqueItems prove

**Status:** Done · P3 2026-09-24T11:17:36Z  

**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md`  
**Parent story:** [`STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md`](../STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md)  
**P1 scaffold:** 2026-09-24T11:13:54Z  
**Maps:** AIB-COMPAT-07 · readiness · `schema_validation_incomplete*`

## Purpose

Extend `schema_validation_complete()` so readiness **proves** uniqueness enforcement via behavioral probe (not frozenset membership alone). Incomplete uniqueness capability → fail-closed readiness (`schema_validation_incomplete*` family / existing conventions). Wire through `readiness.py` as already consuming this probe.

**Out of this task:** Gate 2 enforce logic alone (t01); T-UNIQUE suite (t03); VC bind (STORY-43).

## AC/DoD

- [x] Behavioral prove that `uniqueItems: true` rejects duplicates in the completeness probe.
- [x] Incomplete capability → readiness not ready (fail-closed).
- [x] Does not rely solely on frozenset membership.
- [x] `Skill declared: python-pro` present.

## Where to change (execute — not P1)

- `src/aibridge/request_assembly.py` · `readiness.py` as needed — **P3**
