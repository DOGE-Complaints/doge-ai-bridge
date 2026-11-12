# Acceptance verification — task-aibridge-28-t06-audit-g02-tool007-scalar-args

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T19:15:26Z |
| **Story** | STORY-AIBRIDGE-28-qa-tool-call-validation |
| **Gap** | G-02 |
| **Wave** | `run_mode=aibridge_28_audit_20260917` |

## AC check

- [x] `tool-fc-args-scalar.json` package + copy hash_eq.
- [x] Parametrize rejects scalar + array (`JSON object`).
- [x] Suite green; no live Telegram / Railway invent.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/unit/test_tool_call_validation.py -q
→ 18 passed
```
