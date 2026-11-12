# Task: test — spy bag forbid live logs (G-03)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_26_audit_20260917`  
**Gap:** G-03 (Low) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-26-qa-idempotency-concurrency-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-26-qa-idempotency-concurrency.md`](../STORY-AIBRIDGE-26-qa-idempotency-concurrency.md)  
**P5 scaffold:** 2026-09-17T18:28:05Z  
**P6 closed:** 2026-09-17T18:30:28Z  
**Gate:** [acceptance-verification-task-aibridge-26-t06-audit-g03-spy-forbid-logs.md](./acceptance-verification-task-aibridge-26-t06-audit-g03-spy-forbid-logs.md) PASS  

## Purpose

Spy bag §14 hygiene: either **capture logs** on key IDEM-001 / IDEM-006 paths and assert `forbid_substrings_in_logs` patterns against the bag, **or** drop the unused `_assert_forbid` helper (prefer live assert on 001/006). Patterns only — never embed secret values. **No** live Telegram / Railway invent.

## AC/DoD

- [x] `_assert_forbid` applied to captured logs on IDEM-001 and/or IDEM-006 **or** dead helper removed.
- [x] Forbid patterns remain patterns-only (no Channel/Gateway Bearer values).
- [x] Suite still green; no live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/integration/test_idempotency_concurrency.py` — **P6 Done**
