# Acceptance verification — task-aibridge-31-t06-audit-g02-life002-spy-history

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T20:19:43Z |
| **Story** | STORY-AIBRIDGE-31-qa-restart-lifecycle-retention |
| **Gap** | G-02 |
| **Wave** | `run_mode=aibridge_31_audit_20260917` |

## AC check

- [x] `test_life_002` asserts spy `openai_call_count_after_restart_replay`.
- [x] History persist/restore across rebuild (`HistoryStore` + `PostgresHistoryStore` fake seam).
- [x] No live Telegram / Railway SUCCESS invent; active pkg unchanged.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/integration/test_lifecycle_retention.py -q -k 'life_002 or g02'
→ passed (spy + history)
```
