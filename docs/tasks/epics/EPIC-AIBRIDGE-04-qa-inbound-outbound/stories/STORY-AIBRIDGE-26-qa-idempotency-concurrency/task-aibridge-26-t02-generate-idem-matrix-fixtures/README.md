# Task: fixtures — generate IDEM-002…010 matrix envelopes

**Status:** Done  
**P3 closed:** 2026-09-17T18:21:34Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-26-qa-idempotency-concurrency.md`  
**Parent story:** [`STORY-AIBRIDGE-26-qa-idempotency-concurrency.md`](../STORY-AIBRIDGE-26-qa-idempotency-concurrency.md)  
**P1 scaffold:** 2026-09-17T18:12:10Z  
**Maps:** IDEM-002…010 · TECH ADR-Q1/Q2 envelope `schema_version=1.0`

## Purpose

Generate remaining IDEM-002…010 envelopes (+ linked channel/openai/spies refs) into package `fixtures/` first, then **copy** to `tests/fixtures/{spies,channel,openai}/`. Characterization: IDEM-003 collision-log if implemented; IDEM-004 waiter-branch — capture-first, no silent product invent.

## AC/DoD

- [x] Package `fixtures/` holds envelopes covering IDEM-002…010 (plus seed for 001).
- [x] Matching **copies** exist under `tests/fixtures/{cluster}/`.
- [x] Characterization IDs marked — capture-first (IDEM-003 log-if-implemented; IDEM-004 waiter branch).
- [x] `Skill declared: test-master` present.

## Where to change

- package `fixtures/` + `tests/fixtures/{spies,channel}/` — **Done**
