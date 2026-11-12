# Task: fixtures — promote meta fixture-index

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-35-qa-gates-layers-dod.md`  
**Parent story:** [`STORY-AIBRIDGE-35-qa-gates-layers-dod.md`](../STORY-AIBRIDGE-35-qa-gates-layers-dod.md)  
**P1 scaffold:** 2026-09-17T21:40:06Z  
**P3 close:** 2026-09-17T21:45:30Z  
**Maps:** Gate-5 registry · TECH ADR-Q1 promote=copy

## Purpose

Copy package `fixtures/fixture-index.json` → `tests/fixtures/meta/fixture-index.json`. Keep original in package `fixtures/` (do **not** move/delete). Verify hash_eq after promote.

**Out of this task:** index sync alone (t02); gates checklist (t03); pytest product invent; Railway invent; live Telegram.

## AC/DoD

- [x] Matching **copy** under `tests/fixtures/meta/fixture-index.json`.
- [x] Package original still present and hash_eq vs copy.
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/tests/fixtures/meta/` — **P3**
