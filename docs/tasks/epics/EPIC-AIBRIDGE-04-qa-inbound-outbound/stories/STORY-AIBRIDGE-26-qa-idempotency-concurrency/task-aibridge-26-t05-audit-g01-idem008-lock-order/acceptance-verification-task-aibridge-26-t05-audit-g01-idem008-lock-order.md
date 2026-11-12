# Acceptance verification — task-aibridge-26-t05-audit-g01-idem008-lock-order

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T18:30:28Z |
| **Story** | STORY-AIBRIDGE-26-qa-idempotency-concurrency |
| **Gap** | G-01 |
| **Wave** | P6 · `run_mode=aibridge_26_audit_20260917` |

## AC check

- [x] Tautology `is_active(...) is False or True` removed.
- [x] `max_concurrent == 1` and phases `enter/exit/enter/exit` under barrier.
- [x] Same session_id; lock idle after both; both message texts in OpenAI call history.
- [x] Suite green; no live Telegram / Railway invent.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/integration/test_idempotency_concurrency.py -q
→ 13 passed
```
