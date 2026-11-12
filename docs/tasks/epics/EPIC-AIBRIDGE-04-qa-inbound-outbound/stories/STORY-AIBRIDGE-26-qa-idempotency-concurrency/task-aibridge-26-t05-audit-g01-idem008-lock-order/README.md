# Task: test — IDEM-008 lock exclusivity / history order (G-01)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_26_audit_20260917`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-26-qa-idempotency-concurrency-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-26-qa-idempotency-concurrency.md`](../STORY-AIBRIDGE-26-qa-idempotency-concurrency.md)  
**P5 scaffold:** 2026-09-17T18:28:05Z  
**P6 closed:** 2026-09-17T18:30:28Z  
**Gate:** [acceptance-verification-task-aibridge-26-t05-audit-g01-idem008-lock-order.md](./acceptance-verification-task-aibridge-26-t05-audit-g01-idem008-lock-order.md) PASS  

## Purpose

Strengthen IDEM-008 beyond two completions + 2 OpenAI calls: prove **non-overlapping** `SessionTurnLock` hold (max concurrent `_active` ≤ 1 / exclusive serialization) and **deterministic history/completion order** under `threading.Barrier`. **Remove** tautology `assert lock.is_active(...) is False or True`. **No** live Telegram / Railway invent; **no** disposable-PG invent (G-04 WAIVED).

## AC/DoD

- [x] Tautology assert removed from `test_idem_008_same_session_serialized_by_turn_lock`.
- [x] Assert proves non-overlapping lock hold and ordered completion/history under barrier.
- [x] Suite still green; no live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/integration/test_idempotency_concurrency.py` — **P6 Done**
