# Acceptance verification — task-aibridge-29-t05-audit-g01-act017-pg-hash-only

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T19:38:16Z |
| **Story** | STORY-AIBRIDGE-29-qa-action-token-fsm |
| **Gap** | G-01 |
| **Wave** | `run_mode=aibridge_29_audit_20260917` |

## AC check

- [x] PostgresActionTokenStore issue path (fake conn seam): INSERT params hash-only; raw absent from params/row blob; peek by hash.
- [x] Spy `act-hash-only-persist` fields asserted (`forbid_substrings_in_store_keys`, `raw_stored=false`, mint ≤64).
- [x] Optional log bag: bind_snapshot JSON never contains raw.
- [x] No live Telegram / Railway SUCCESS invent; active pkg unchanged.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/unit/test_action_token_fsm.py \
  tests/integration/test_action_token_fsm_http.py -q
→ 29 passed
```
