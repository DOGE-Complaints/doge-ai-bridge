# Task: fixtures — generate OAI-002…016 matrix envelopes

**Status:** Done  
**P3 closed:** 2026-09-17T18:46:05Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md`  
**Parent story:** [`STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md`](../STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md)  
**P1 scaffold:** 2026-09-17T18:39:38Z  
**Maps:** OAI-002…016 · TECH ADR-Q1/Q2 envelope `schema_version=1.0`

## Purpose

Generate remaining OAI-002…016 envelopes into package `fixtures/` first, then **copy** to `tests/fixtures/openai/` (and `channel` envelopes if needed for turn harness). Characterization: OAI-008/009/016 hedges — capture-first, no silent product invent.

## AC/DoD

- [x] Package `fixtures/` holds envelopes covering OAI-002…016 (plus seed for 001).
- [x] Matching **copies** exist under `tests/fixtures/openai/` (and channel if required).
- [x] Characterization IDs marked — capture-first (OAI-008/009/016).
- [x] `Skill declared: test-master` present.

## Where to change

- package `fixtures/` + `tests/fixtures/{openai,channel}/` — **Done**
