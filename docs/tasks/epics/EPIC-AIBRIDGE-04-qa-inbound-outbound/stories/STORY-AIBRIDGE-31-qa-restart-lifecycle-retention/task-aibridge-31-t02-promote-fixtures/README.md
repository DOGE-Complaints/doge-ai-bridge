# Task: fixtures — promote LIFE matrix copies

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md`  
**Parent story:** [`STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md`](../STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md)  
**P1 scaffold:** 2026-09-17T20:05:23Z  
**Maps:** LIFE-001…012 · TECH ADR-Q1 promote=copy

## Purpose

Copy package `fixtures/` LIFE-* envelopes → `tests/fixtures/{settings,channel,spies}/` as required. Keep originals in package `fixtures/` (do **not** move/delete). Verify hash_eq after promote.

**Out of this task:** generate envelopes (t01); pytest (t03); Railway invent; live Telegram.

## AC/DoD

- [x] Matching **copies** under `tests/fixtures/{settings,channel,spies}/` as required.
- [x] Package originals still present and hash_eq vs copies.
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/tests/fixtures/{settings,channel,spies}/` — **P3**
