# Task: test — split transport vs channel asserts (OAI-008/009)

**Status:** Done · 2026-09-18T13:43:00Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md`  
**Parent story:** [`STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md`](../STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md)  
**P1 scaffold:** 2026-09-18T13:40:25Z  
**P3 closed:** 2026-09-18T13:43:00Z  
**Maps:** OAI-008 · OAI-009 · CHAR-006 · gaps §38 T02

## Purpose

Keep transport asserts; rewrite channel asserts to Option A. Product map: `ResponsesTransportError` handler in `app.py` (RATE_LIMITED→429, TRANSIENT_FAILURE→503).

## AC/DoD

- [x] Transport asserts remain green.
- [x] Channel asserts match Option A expects (no forever-500 lock).
- [x] Secrets absent from error bodies.
- [x] `Skill declared: test-master` present.

## Where to change

- `src/aibridge/app.py` — **P3 Done**
- `tests/integration/test_openai_prompt_behavior.py` — **P3 Done**
