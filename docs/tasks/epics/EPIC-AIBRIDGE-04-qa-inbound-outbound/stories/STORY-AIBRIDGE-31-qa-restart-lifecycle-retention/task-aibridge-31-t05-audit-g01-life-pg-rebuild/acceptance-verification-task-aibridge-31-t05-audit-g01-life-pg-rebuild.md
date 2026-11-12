# Acceptance verification — task-aibridge-31-t05-audit-g01-life-pg-rebuild

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T20:19:43Z |
| **Story** | STORY-AIBRIDGE-31-qa-restart-lifecycle-retention |
| **Gap** | G-01 |
| **Wave** | `run_mode=aibridge_31_audit_20260917` |

## AC check

- [x] LIFE-002/003/004 via `PostgresConfirmSessionStore` / `PostgresActionTokenStore` (fake conn Preference A) + rebuild guard.
- [x] Live `rebuild_app_same_pg` path present (`skipif` when disposable PG absent).
- [x] Restore / pending usable / consumed stays consumed; no duplicate gateway.
- [x] No live Telegram / Railway SUCCESS invent; active pkg unchanged.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/integration/test_lifecycle_retention.py -q
→ 17 passed, 1 skipped (live disposable PG)
```
