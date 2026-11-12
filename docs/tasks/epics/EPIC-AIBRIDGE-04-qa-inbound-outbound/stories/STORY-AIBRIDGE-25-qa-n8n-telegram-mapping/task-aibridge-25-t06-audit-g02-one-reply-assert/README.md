# Task: test — N8N-001 assert one_reply outbound (G-02)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_25_audit_20260917`  
**Gap:** G-02 (Low) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-25-qa-n8n-telegram-mapping-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md`](../STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md)  
**P5 scaffold:** 2026-09-17T17:50:16Z  
**P6 closed:** 2026-09-17T17:52:37Z  
**Gate:** [acceptance-verification-task-aibridge-25-t06-audit-g02-one-reply-assert.md](./acceptance-verification-task-aibridge-25-t06-audit-g02-one-reply-assert.md) PASS  

## Purpose

On N8N-001 `map-private-text`, assert `outbound_telegram.one_reply` / single `SendOrEditMessage` in the outbound contract.

## AC/DoD

- [x] N8N-001 private-text path asserts `one_reply` and single `SendOrEditMessage` in `ack_order`.
- [x] Existing mapping equality asserts remain.
- [x] Suite still passes (`DATABASE_URL=memory` + `--noconftest`).
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/tests/n8n/test_n8n_telegram_mapping.py` — **P6 Done**
