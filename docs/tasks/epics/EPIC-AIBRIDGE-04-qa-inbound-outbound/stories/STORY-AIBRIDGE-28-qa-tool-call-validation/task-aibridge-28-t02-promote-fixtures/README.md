# Task: fixtures — promote TOOL-* copies

**Status:** Done  
**P3 closed:** 2026-09-17T19:07:11Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-28-qa-tool-call-validation.md`  
**Parent story:** [`STORY-AIBRIDGE-28-qa-tool-call-validation.md`](../STORY-AIBRIDGE-28-qa-tool-call-validation.md)  
**P1 scaffold:** 2026-09-17T19:00:38Z  
**Maps:** TOOL-001…014 · TECH ADR-Q1 promote=copy

## Purpose

Copy package TOOL-* envelopes → `tests/fixtures/openai/` and `tests/fixtures/gateway/`. Keep originals in package `fixtures/` (do **not** move/delete). Verify hash_eq after promote.

## AC/DoD

- [x] Matching **copies** exist under `tests/fixtures/openai/` and `tests/fixtures/gateway/`.
- [x] Package originals still present and unchanged paths (hash_eq).
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/tests/fixtures/openai/tool-*.json` · `doge-ai-bridge/tests/fixtures/gateway/tool-*.json` — **Done**
