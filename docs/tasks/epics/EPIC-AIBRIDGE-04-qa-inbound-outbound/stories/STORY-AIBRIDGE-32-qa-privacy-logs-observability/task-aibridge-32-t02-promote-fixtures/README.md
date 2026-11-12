# Task: fixtures — promote SEC matrix copies

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-32-qa-privacy-logs-observability.md`  
**Parent story:** [`STORY-AIBRIDGE-32-qa-privacy-logs-observability.md`](../STORY-AIBRIDGE-32-qa-privacy-logs-observability.md)  
**P1 scaffold:** 2026-09-17T20:27:34Z  
**P3 closed:** 2026-09-17T20:33:31Z  
**Maps:** SEC-001…010 · TECH ADR-Q1 promote=copy

## Purpose

Copy package `fixtures/` SEC-* envelopes → `tests/fixtures/{spies,channel,openai,gateway}/` as required. Keep originals in package `fixtures/` (do **not** move/delete). Verify hash_eq after promote.

**Out of this task:** generate envelopes (t01); pytest (t03); Railway invent; live Telegram.

## AC/DoD

- [x] Matching **copies** under `tests/fixtures/{spies,channel,openai,gateway}/` as required.
- [x] Package originals still present and hash_eq vs copies.
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/tests/fixtures/{spies,channel,openai,gateway}/` — **P3**
