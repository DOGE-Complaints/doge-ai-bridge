# Task: fixtures — promote seed ready-missing-channel-bearer

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-33-qa-readiness-configuration.md`  
**Parent story:** [`STORY-AIBRIDGE-33-qa-readiness-configuration.md`](../STORY-AIBRIDGE-33-qa-readiness-configuration.md)  
**P1 scaffold:** 2026-09-17T20:50:14Z
**P3 closed:** 2026-09-17T20:57:41Z  
**Maps:** READY-002 · TECH ADR-Q1 promote=copy

## Purpose

Copy package `fixtures/ready-missing-channel-bearer.json` → `tests/fixtures/settings/`. Keep original in package `fixtures/` (do **not** move/delete). Verify hash_eq after promote.

**Out of this task:** generate READY matrix (t02); pytest (t03); Railway invent; live Telegram.

## AC/DoD

- [x] Matching **copy** under `tests/fixtures/settings/ready-missing-channel-bearer.json`.
- [x] Package original still present and hash_eq vs copy.
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/tests/fixtures/settings/` — **P3**
