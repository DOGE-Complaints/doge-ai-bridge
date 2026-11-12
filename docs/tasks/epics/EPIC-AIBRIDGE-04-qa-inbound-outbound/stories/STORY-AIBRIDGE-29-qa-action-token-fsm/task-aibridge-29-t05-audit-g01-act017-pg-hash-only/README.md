# Task: test — ACT-017 PG/logs hash-only (G-01)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_29_audit_20260917`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-29-qa-action-token-fsm-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-29-qa-action-token-fsm.md`](../STORY-AIBRIDGE-29-qa-action-token-fsm.md)  
**P5 scaffold:** 2026-09-17T19:35:13Z  
**P6 closed:** 2026-09-17T19:38:16Z  
**Gate:** [acceptance-verification-task-aibridge-29-t05-audit-g01-act017-pg-hash-only.md](./acceptance-verification-task-aibridge-29-t05-audit-g01-act017-pg-hash-only.md) PASS  

## Purpose

Strengthen ACT-017 **must**: raw token must not persist in PostgreSQL/logs — only hash. Exercise `PostgresActionTokenStore` (fake conn seam) hash-only insert+lookup; assert spy `act-hash-only-persist` fields (`forbid_substrings_in_store_keys`, `raw_stored=false`); optional log/forbid bag that raw is absent. Preference A applied: **test-first** against existing PG store seam. **No** live Telegram / Railway invent.

## AC/DoD

- [x] PG store path (fake conn): issue+lookup stores hash only; raw not in INSERT params / row blob.
- [x] Spy `act-hash-only-persist` fields asserted (`forbid_substrings_in_store_keys` / mint ≤64).
- [x] Optional: log/forbid bag assert raw token absent.
- [x] No live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/unit/test_action_token_fsm.py` — **P6 Done**
