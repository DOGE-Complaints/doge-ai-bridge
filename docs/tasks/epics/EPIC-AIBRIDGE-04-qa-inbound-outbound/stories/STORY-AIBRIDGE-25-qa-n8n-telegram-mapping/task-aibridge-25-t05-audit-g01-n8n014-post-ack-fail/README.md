# Task: test — N8N-014 post-ack aibridge fail timeline (G-01)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_25_audit_20260917`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-25-qa-n8n-telegram-mapping-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md`](../STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md)  
**P5 scaffold:** 2026-09-17T17:50:16Z  
**P6 closed:** 2026-09-17T17:52:37Z  
**Gate:** [acceptance-verification-task-aibridge-25-t05-audit-g01-n8n014-post-ack-fail.md](./acceptance-verification-task-aibridge-25-t05-audit-g01-n8n014-post-ack-fail.md) PASS  

## Purpose

Deepen N8N-014 beyond documentary fixture flags: fixture-driven **ordered timeline** where `answerCallbackQuery` completes **before** a simulated aibridge slow/unavailable failure; assert prompt ack + later resident-safe error path. **No** live Telegram / Railway invent.

## AC/DoD

- [x] Fixture encodes failure_timeline: ack → aibridge_unavailable → resident-safe error.
- [x] Test asserts `answerCallbackQuery` before aibridge failure; prompt-ack retained.
- [x] No live Telegram / network Bot API.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/n8n/test_n8n_telegram_mapping.py` — **P6 Done**
- `tests/fixtures/n8n/callback-ack-before-actions.json` (+ package copy) — **P6 Done**
