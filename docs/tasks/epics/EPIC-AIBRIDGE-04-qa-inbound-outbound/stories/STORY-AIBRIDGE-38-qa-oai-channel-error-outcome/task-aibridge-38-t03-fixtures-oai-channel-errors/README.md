# Task: fixtures — OAI channel error expect envelopes

**Status:** Done · 2026-09-18T13:43:00Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md`  
**Parent story:** [`STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md`](../STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md)  
**P1 scaffold:** 2026-09-18T13:40:25Z  
**P3 closed:** 2026-09-18T13:43:00Z  
**Maps:** OAI-008 · OAI-009 · CHAR-006 · gaps §38 T03

## Purpose

Expect envelopes for channel error shape; promote=copy to `tests/fixtures/openai/`.

## AC/DoD

- [x] Expect envelopes match Option A (429/503).
- [x] Promote = copy; hash_eq.
- [x] No secrets in envelopes.
- [x] `Skill declared: test-master` present.

## Where to change

- package `fixtures/openai/char-006-channel-*-expect.json` — **P3 Done**
- `tests/fixtures/openai/` copies — **P3 Done**
