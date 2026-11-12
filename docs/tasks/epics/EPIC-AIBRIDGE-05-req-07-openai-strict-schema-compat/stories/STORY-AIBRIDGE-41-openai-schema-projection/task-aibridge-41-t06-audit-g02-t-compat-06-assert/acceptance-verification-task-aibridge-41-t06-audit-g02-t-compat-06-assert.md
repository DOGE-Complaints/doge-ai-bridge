# Acceptance verification — task-aibridge-41-t06-audit-g02-t-compat-06-assert

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-24T11:08:43Z |
| **Story** | STORY-AIBRIDGE-41-openai-schema-projection |
| **Pkg** | pkg-000040 (immutable) |
| **Wave** | P6 · `run_mode=aibridge_41_audit_20260924` |
| **Gap** | G-02 → **CLOSED** |

## AC check

- [x] T-COMPAT-06: projected houses keep `minItems: 1`; no `uniqueItems`
- [x] Named in this AV + test docstring
- [x] Suite green; no invent live TG / OpenAI
- [x] `Skill declared: python-pro` present

## Evidence

```text
tests/test_openai_schema_projection.py::test_t_compat_06_supported_constraints_survive PASSED
pytest … → 14 passed
```
