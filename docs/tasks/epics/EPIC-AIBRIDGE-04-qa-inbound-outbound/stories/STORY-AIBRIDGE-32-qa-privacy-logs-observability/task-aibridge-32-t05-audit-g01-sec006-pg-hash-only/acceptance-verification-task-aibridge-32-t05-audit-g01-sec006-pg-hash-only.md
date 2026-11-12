# Acceptance verification — task-aibridge-32-t05-audit-g01-sec006-pg-hash-only

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T20:42:29Z |
| **Story** | STORY-AIBRIDGE-32-qa-privacy-logs-observability |
| **Gap** | G-01 |
| **Wave** | `run_mode=aibridge_32_audit_20260917` |
| **Pkg** | pkg-000029 (immutable) |

## AC check

- [x] SEC-006 via `PostgresActionTokenStore` fake-conn Preference A.
- [x] Raw absent from INSERT params/keys; hash-only persist + peek.
- [x] No live Telegram / Railway invent.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/integration/test_privacy_observability.py -q
→ 12 passed
```
