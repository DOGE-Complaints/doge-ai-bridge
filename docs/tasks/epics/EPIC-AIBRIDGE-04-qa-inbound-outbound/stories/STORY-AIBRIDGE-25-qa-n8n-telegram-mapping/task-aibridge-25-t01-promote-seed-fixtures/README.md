# Task: fixtures — promote telegram + n8n seed copies

**Status:** Done  
**P3 closed:** 2026-09-17T17:44:23Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md`  
**Parent story:** [`STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md`](../STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md)  
**P1 scaffold:** 2026-09-17T17:39:14Z  
**Maps:** N8N-001 seed · N8N-013 seed · TECH ADR-Q1 promote=copy

## Purpose

Copy package seeds `fixtures/message-private-ru-pothole.json` → `tests/fixtures/telegram/message-private-ru-pothole.json` and `fixtures/callback-ack-before-actions.json` → `tests/fixtures/n8n/callback-ack-before-actions.json`. Keep originals in package `fixtures/` (do **not** move/delete). Verify hash_eq after promote.

**Out of this task:** generate N8N-002…018 (t02); mapping pytest (t03); Railway invent; live Telegram.

## AC/DoD

- [x] Both target copies exist under `tests/fixtures/telegram/` and `tests/fixtures/n8n/` (hash_eq vs package originals).
- [x] Package originals still present and unchanged paths.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/fixtures/telegram/` — **Done**
- `tests/fixtures/n8n/` — **Done**
