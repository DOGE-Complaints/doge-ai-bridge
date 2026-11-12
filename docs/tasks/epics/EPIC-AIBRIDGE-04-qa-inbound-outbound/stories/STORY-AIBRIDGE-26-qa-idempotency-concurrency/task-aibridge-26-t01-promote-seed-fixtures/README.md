# Task: fixtures — promote spies (+ channel/openai) seed copies

**Status:** Done  
**P3 closed:** 2026-09-17T18:21:34Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-26-qa-idempotency-concurrency.md`  
**Parent story:** [`STORY-AIBRIDGE-26-qa-idempotency-concurrency.md`](../STORY-AIBRIDGE-26-qa-idempotency-concurrency.md)  
**P1 scaffold:** 2026-09-17T18:12:10Z  
**Maps:** IDEM-001 seed · TECH ADR-Q1 promote=copy

## Purpose

Copy package seed `fixtures/idem-same-event-once-openai.json` → `tests/fixtures/spies/idem-same-event-once-openai.json`. Promote needed channel/openai seeds as **copies** (reuse existing channel copies under `tests/fixtures/channel/` where already present). Keep originals in package `fixtures/` (do **not** move/delete). Verify hash_eq after promote.

**Out of this task:** generate IDEM-002…010 (t02); integration pytest (t03); Railway invent; live Telegram.

## AC/DoD

- [x] Target copy exists under `tests/fixtures/spies/idem-same-event-once-openai.json` (hash_eq vs package original).
- [x] Needed channel/openai seed copies present under `tests/fixtures/{channel,openai}/` when required by matrix (hash_eq; reuse if already promoted).
- [x] Package originals still present and unchanged paths.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/fixtures/spies/` · `tests/fixtures/openai/text-only-ru-clarify.json` — **Done**
