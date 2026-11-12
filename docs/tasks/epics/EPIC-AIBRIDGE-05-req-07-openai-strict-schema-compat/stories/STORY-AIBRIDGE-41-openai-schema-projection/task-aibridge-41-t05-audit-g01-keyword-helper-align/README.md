# Task: test — align keyword helper with production map keys (G-01)

**Status:** Done · 2026-09-24T11:08:43Z  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_41_audit_20260924`  
**Gap:** G-01 (Low) — P4 audit 2026-09-24 → **CLOSED**  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-41-openai-schema-projection-20260924.md`  
**Parent story:** [`STORY-AIBRIDGE-41-openai-schema-projection.md`](../STORY-AIBRIDGE-41-openai-schema-projection.md)  
**P5 scaffold:** 2026-09-24T11:06:43Z  
**P6 closed:** 2026-09-24T11:08:43Z  
**Maps:** G-01 · AC-03 oracle hygiene · AIB-COMPAT-02

## Purpose

Align `tests/test_openai_schema_projection.py` helper `_keyword_in_schema_tree` with production `_PROPERTY_MAP_KEYS` (`properties` / `patternProperties` / `$defs` / `definitions`) so a `$defs` entry *named* `uniqueItems` is not false-positive as a schema keyword.

**Out of this task:** T-COMPAT-06 assert (t06); Gate 2 / live TG invent; product `tool_gen.py` policy change.

## AC/DoD

- [x] Helper walk matches production property-map keys (or AC-03 oracle documented without `$defs` false positive).
- [x] Existing projection suite still green under filter.
- [x] No invent live TG / Railway / Gate2.
- [x] `Skill declared: python-pro` present.

## Where changed

- `tests/test_openai_schema_projection.py` — `_keyword_in_schema_tree` + `test_helper_ignores_defs_entry_named_unique_items`
