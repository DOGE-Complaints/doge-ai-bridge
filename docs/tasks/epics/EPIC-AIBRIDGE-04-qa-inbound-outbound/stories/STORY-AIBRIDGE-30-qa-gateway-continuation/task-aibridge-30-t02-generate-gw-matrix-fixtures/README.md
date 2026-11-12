# Task: fixtures — generate GW-001…020 matrix envelopes

**Status:** Done  
**P3 closed:** 2026-09-17T19:51:28Z  

**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-30-qa-gateway-continuation.md`  
**Parent story:** [`STORY-AIBRIDGE-30-qa-gateway-continuation.md`](../STORY-AIBRIDGE-30-qa-gateway-continuation.md)  
**P1 scaffold:** 2026-09-17T19:45:47Z  
**Maps:** GW-001…020 · TECH ADR-Q1/Q2 envelope `schema_version=1.0`

## Purpose

Generate GW-001…020 envelopes into package `fixtures/` first (`schema_version=1.0`), then promote **copies** → `tests/fixtures/gateway/` (+ `spies` / `channel` as needed). Do **not** delete/move package originals (including seed `stashed-201`).

**Out of this task:** seed-only promote (t01); pytest (t03); Railway invent; live Telegram; product invent.

## AC/DoD

- [x] Package `fixtures/` holds envelopes covering GW-001…020 (gateway/spies/settings as needed).
- [x] Matching **copies** under `tests/fixtures/{gateway,spies,settings}/` as required; originals hash_eq.
- [x] Envelope fields per TECH §6.2 (`schema_version=1.0`).
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/` — **P3**
- `doge-ai-bridge/tests/fixtures/{gateway,spies,channel}/` — **P3**
