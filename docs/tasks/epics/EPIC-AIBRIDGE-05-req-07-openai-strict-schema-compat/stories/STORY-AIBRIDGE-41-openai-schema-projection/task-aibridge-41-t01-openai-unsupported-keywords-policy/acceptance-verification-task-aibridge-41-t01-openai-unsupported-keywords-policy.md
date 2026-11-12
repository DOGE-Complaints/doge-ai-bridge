# Acceptance verification — task-aibridge-41-t01-openai-unsupported-keywords-policy

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-24T11:00:27Z |
| **Story** | STORY-AIBRIDGE-41-openai-schema-projection |
| **Pkg** | pkg-000040 |
| **Wave** | P3 Execute |

## AC check

- [x] `OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS = frozenset({"uniqueItems"})` sole strip allow-list — `src/aibridge/tool_gen.py`
- [x] Recursive `project_schema_for_openai` covers nested schema shapes; property names not stripped
- [x] `Skill declared: python-pro` present

## Evidence

```text
src/aibridge/tool_gen.py — OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS, project_schema_for_openai
pytest tests/test_openai_schema_projection.py::test_policy_constant_sole_strip_allowlist PASSED
pytest …::test_project_strips_unique_items_preserves_input PASSED
pytest …::test_project_preserves_property_named_unique_items PASSED
```
