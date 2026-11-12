# Task: test — implement n8n mapping + ack_order suite

**Status:** Done  
**P3 closed:** 2026-09-17T17:44:23Z  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md`  
**Parent story:** [`STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md`](../STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md)  
**P1 scaffold:** 2026-09-17T17:39:14Z  
**Maps:** N8N-001…018 · layer `tests/n8n/`

## Purpose

Fixture-driven tests under `tests/n8n/` covering update→`/turns` mapping, Unicode, principal/session, callback ack before `/actions`, actions/keyboard/outcome (`claim_published_forbidden`). No live Telegram.

## AC/DoD

- [x] Suite under `tests/n8n/` asserts mapping + `ack_order` for matrix must-rows.
- [x] No live Telegram / network Telegram API in default CI path.
- [x] Characterization rows capture-first (N8N-009 · N8N-011).
- [x] `Skill declared: python-pro` present.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/n8n/ -q --noconftest → 19 passed
```

## Where to change

- `doge-ai-bridge/tests/n8n/test_n8n_telegram_mapping.py` — **Done**
