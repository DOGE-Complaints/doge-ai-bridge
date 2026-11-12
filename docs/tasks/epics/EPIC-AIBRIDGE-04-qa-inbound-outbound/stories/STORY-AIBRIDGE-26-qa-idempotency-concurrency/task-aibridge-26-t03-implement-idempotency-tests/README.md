# Task: test — implement idempotency / concurrency integration suite

**Status:** Done  
**P3 closed:** 2026-09-17T18:21:34Z  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-26-qa-idempotency-concurrency.md`  
**Parent story:** [`STORY-AIBRIDGE-26-qa-idempotency-concurrency.md`](../STORY-AIBRIDGE-26-qa-idempotency-concurrency.md)  
**P1 scaffold:** 2026-09-17T18:12:10Z  
**Maps:** IDEM-001…010 · layer `tests/integration/`

## Purpose

Integration tests under `tests/integration/` covering IDEM-001…010: side-effect counts (OpenAI/gateway calls), EventDedupeStore claim/abort/replay, session lock serialization, concurrent barriers/`threading.Barrier` (**not** `sleep`), RecordingResponsesClient. No live Telegram.

## AC/DoD

- [x] Suite under `tests/integration/` asserts side-effect counts + barriers for matrix must-rows.
- [x] No live Telegram / network Telegram API in default CI path.
- [x] Characterization rows capture-first (IDEM-003 log-if-implemented; IDEM-004 waiter-branch).
- [x] Spy bag §14: no Bearer / full narrative / raw token in log asserts.
- [x] `Skill declared: python-pro` present.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/integration/test_idempotency_concurrency.py -q
→ 13 passed
```

## Where to change

- `doge-ai-bridge/tests/integration/test_idempotency_concurrency.py` — **Done**
