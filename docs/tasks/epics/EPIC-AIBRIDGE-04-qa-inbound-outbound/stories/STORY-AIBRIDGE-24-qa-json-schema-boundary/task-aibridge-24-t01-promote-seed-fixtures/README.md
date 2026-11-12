# Task: fixtures — promote seed turns-valid-private (copy)

**Status:** Done  
**P3 closed:** 2026-09-17T14:32:38Z  

**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-24-qa-json-schema-boundary.md`  
**Parent story:** [`STORY-AIBRIDGE-24-qa-json-schema-boundary.md`](../STORY-AIBRIDGE-24-qa-json-schema-boundary.md)  
**P1 scaffold:** 2026-09-17T14:26:09Z  
**Maps:** VAL-001 seed · TECH ADR-Q1 promote=copy

## Purpose

Ensure package seed `fixtures/turns-valid-private.json` is present as a **copy** at `tests/fixtures/channel/turns-valid-private.json`. Keep original in package `fixtures/` (do **not** move/delete). If already promoted by STORY-23, verify hash_eq and leave both paths intact.

**Out of this task:** generate VAL-002…018 (t02); schema pytest (t03); Railway invent.

## Code Facts (verified exists — post P3)

1. Seed original + copy **hash_eq** (sha256).
2. Package original path unchanged.
3. INDEX promote map: seed → `tests/fixtures/channel/turns-valid-private.json`.

## AC/DoD

- [x] `tests/fixtures/channel/turns-valid-private.json` exists as a **copy** (hash_eq vs package original).
- [x] Package original still present and unchanged path.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/fixtures/channel/` — **Done** (verified copy from STORY-23)

## Verification commands

```bash
test -f doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/turns-valid-private.json
test -f doge-ai-bridge/tests/fixtures/channel/turns-valid-private.json
```
