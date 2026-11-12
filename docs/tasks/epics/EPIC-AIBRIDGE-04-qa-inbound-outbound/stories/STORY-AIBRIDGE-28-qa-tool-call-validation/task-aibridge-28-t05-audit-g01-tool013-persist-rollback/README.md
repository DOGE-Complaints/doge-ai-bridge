# Task: test — TOOL-013 persist fail-closed / no freeze leak (G-01)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_28_audit_20260917`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-28-qa-tool-call-validation-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-28-qa-tool-call-validation.md`](../STORY-AIBRIDGE-28-qa-tool-call-validation.md)  
**P5 scaffold:** 2026-09-17T19:13:12Z  
**P6 closed:** 2026-09-17T19:15:26Z  
**Gate:** [acceptance-verification-task-aibridge-28-t05-audit-g01-tool013-persist-rollback.md](./acceptance-verification-task-aibridge-28-t05-audit-g01-tool013-persist-rollback.md) PASS  

## Purpose

Strengthen TOOL-013 fail-closed on persist failure: after `_persist_session` boom in `persist_pending_tool` / `build_turn_from_engine`, assert **no Send** and **no durable pending freeze leak** (`frozen_tool_intent` and `pending_call_id` cleared/`None`). Preference B applied: product clear in `persist_pending_tool` before re-raise. Keep gw=[]. **No** live Telegram / Railway invent.

## AC/DoD

- [x] After persist boom: no Send actions / state ≠ successful `AWAITING_SEND_CONFIRM` offer path; gw=[].
- [x] Assert `frozen_tool_intent is None` and `pending_call_id is None` — no in-memory freeze leak.
- [x] Suite still green; no live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/unit/test_tool_call_validation.py` — **P6 Done**
- `src/aibridge/coordinator.py` (`persist_pending_tool`) — **P6 Done** (Preference B)
