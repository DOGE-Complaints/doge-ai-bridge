# Task: fixtures — promote ACT-* copies

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-29-qa-action-token-fsm.md`  
**Parent story:** [`STORY-AIBRIDGE-29-qa-action-token-fsm.md`](../STORY-AIBRIDGE-29-qa-action-token-fsm.md)  
**P1 scaffold:** 2026-09-17T19:21:48Z  
**Maps:** ACT-001…018 · TECH ADR-Q1 promote=copy

## Purpose

Copy package ACT-* envelopes → `tests/fixtures/channel/`, `tests/fixtures/spies/`, and `tests/fixtures/openai/` as needed. Keep originals in package `fixtures/` (do **not** move/delete). Verify hash_eq after promote.

**Out of this task:** generate envelopes (t01); pytest (t03); Railway invent; live Telegram.

## AC/DoD

- [x] Matching **copies** exist under `tests/fixtures/{channel,spies,openai}/` as required.
- [x] Package originals still present and unchanged paths (hash_eq).
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/tests/fixtures/{channel,spies,openai}/` — **P3**
