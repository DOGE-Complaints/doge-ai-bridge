# Task: fixtures — promote openai seed copy

**Status:** Done  
**P3 closed:** 2026-09-17T18:46:05Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md`  
**Parent story:** [`STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md`](../STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md)  
**P1 scaffold:** 2026-09-17T18:39:38Z  
**Maps:** OAI-001 seed · TECH ADR-Q1 promote=copy

## Purpose

Copy package seed `fixtures/text-only-ru-clarify.json` → `tests/fixtures/openai/text-only-ru-clarify.json` (idempotent if already present). Keep original in package `fixtures/` (do **not** move/delete). Verify hash_eq after promote.

**Out of this task:** generate OAI-002…016 (t02); integration pytest (t03); Railway invent; live Telegram.

## AC/DoD

- [x] Target copy exists under `tests/fixtures/openai/text-only-ru-clarify.json` (hash_eq vs package original).
- [x] Package original still present and unchanged path.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/fixtures/openai/text-only-ru-clarify.json` — **Done** (hash_eq)
