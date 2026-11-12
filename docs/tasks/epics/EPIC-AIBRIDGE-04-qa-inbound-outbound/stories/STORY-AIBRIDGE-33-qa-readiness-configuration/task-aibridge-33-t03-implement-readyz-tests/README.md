# Task: test — implement /readyz readiness suite

**Status:** Done  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-33-qa-readiness-configuration.md`  
**Parent story:** [`STORY-AIBRIDGE-33-qa-readiness-configuration.md`](../STORY-AIBRIDGE-33-qa-readiness-configuration.md)  
**P1 scaffold:** 2026-09-17T20:50:14Z
**P3 closed:** 2026-09-17T20:57:41Z  
**Maps:** READY-001…015 · layer `tests/contract/` / readiness unit

## Purpose

Readiness/configuration tests via Settings overrides + `/readyz`: bounded 503 reasons for READY-002…014; READY-001 → 200 `ready`; READY-015 no OpenAI generation and no gateway write. No live Telegram. Guide must-rows → automated asserts; no silent product invent.

## AC/DoD

- [x] Suite under `tests/contract/` (and/or readiness unit) asserts READY-001…015 must-rows.
- [x] No live Telegram / Railway invent.
- [x] No silent product invent for READY-*.
- [x] `Skill declared: python-pro` present.

## Verification commands (P3)

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/contract/ -q -k 'ready or readyz or readiness'
```

## Where to change

- `doge-ai-bridge/tests/contract/` — **P3**
- Surfaces: Settings · `readiness.py` · `/readyz` (assert only; no product invent in P1)
