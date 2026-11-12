# Task: fixtures — promote seed turns-valid-private (copy)

**Status:** Done  
**P3 closed:** 2026-09-17T14:02:23Z  

**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md`  
**Parent story:** [`STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md`](../STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md)  
**P1 scaffold:** 2026-09-17T13:59:06Z  
**Maps:** AUTH-001 seed · TECH ADR-Q1 promote=copy

## Purpose

Copy package seed `fixtures/turns-valid-private.json` → `tests/fixtures/channel/turns-valid-private.json`. Keep original in package `fixtures/` (do **not** move/delete).

**Out of this task:** generate AUTH-002…012 (t02); contract pytest (t03); Railway invent.

## Code Facts (verified exists — P1)

1. Seed original: `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/turns-valid-private.json`
2. Target tree `tests/fixtures/channel/` — **absent** until this task (P3).
3. INDEX promote map: seed → `tests/fixtures/channel/turns-valid-private.json`

## AC/DoD

- [x] `tests/fixtures/channel/turns-valid-private.json` exists as a **copy**.
- [x] Package original still present and unchanged path.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/fixtures/channel/` — **P3** (copy only)

## Verification commands

```bash
test -f doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/turns-valid-private.json
test -f doge-ai-bridge/tests/fixtures/channel/turns-valid-private.json
```
