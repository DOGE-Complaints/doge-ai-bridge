# Acceptance verification — task-aibridge-30-t06-audit-g02-gw011-spy-resend

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T19:59:20Z |
| **Story** | STORY-AIBRIDGE-30-qa-gateway-continuation |
| **Gap** | G-02 |
| **Wave** | `run_mode=aibridge_30_audit_20260917` |

## AC check

- [x] Spy `http_posted` / `send_blocked_same_revision` asserted in `test_gw_011`.
- [x] Second `offer_send_confirm` blocked (`IllegalTransitionError`); transport call count unchanged.
- [x] Optional disconnect: `ConnectionError` → `unknown_outcome` + `http_posted`.
- [x] No live Telegram / Railway SUCCESS invent; active pkg unchanged.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/integration/test_gateway_continuation.py -q
→ 23 passed
```
