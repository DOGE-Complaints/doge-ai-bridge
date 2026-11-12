# Task: test — LIFE-002 spy + history (G-02)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_31_audit_20260917`  
**Gap:** G-02 (Low) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-31-qa-restart-lifecycle-retention-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md`](../STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md)  
**P5 scaffold:** 2026-09-17T20:17:44Z  
**P6 closed:** 2026-09-17T20:19:43Z  
**Gate:** [acceptance-verification-task-aibridge-31-t06-audit-g02-life002-spy-history.md](./acceptance-verification-task-aibridge-31-t06-audit-g02-life002-spy-history.md) PASS  
**Maps:** LIFE-002 · spy `life-restart-interview`

## Purpose

Assert spy `openai_call_count_after_restart_replay` via recording client across rebuild; persist+list history across restart (`HistoryStore` + `PostgresHistoryStore` fake seam). **No** live Telegram / Railway invent.

## AC/DoD

- [x] `test_life_002` reads spy `openai_call_count_after_restart_replay`.
- [x] History persist/restore across restart asserted.
- [x] No live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/integration/test_lifecycle_retention.py` — **P6 Done**
- `tests/fixtures/spies/life-restart-interview.json` (notes if matrix-only)
