# Task: test — implement UC-01…10 journey E2E

**Status:** Done  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-34-qa-product-journey-scenarios.md`  
**Parent story:** [`STORY-AIBRIDGE-34-qa-product-journey-scenarios.md`](../STORY-AIBRIDGE-34-qa-product-journey-scenarios.md)  
**P1 scaffold:** 2026-09-17T21:14:24Z  
**Maps:** UC-01…10 · layer `tests/integration/` · E2EHarness

## Purpose

Parameterized E2E per UC using `E2EHarness` (disposable PG + Recording OpenAI + Recording Gateway). Barriers not sleep. Guide must-rows → automated asserts; characterization capture-first for UC-06/09 adapter seams. No live Telegram / Railway invent. No silent product invent.

## AC/DoD

- [x] Suite under `tests/integration/` asserts UC-01…10 must-rows (or marked characterization).
- [x] Uses E2EHarness; no live Telegram / Railway SUCCESS invent.
- [x] No silent product invent for UC-*.
- [x] `Skill declared: python-pro` present.

## Verification commands (P3)

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/integration/ -q -k 'uc or journey or product_journey'
```

## Where to change

- `doge-ai-bridge/tests/integration/` — **P3**
- Surfaces: channel turns/actions · confirm FSM · gateway outcomes (assert only; no product invent in P1)
