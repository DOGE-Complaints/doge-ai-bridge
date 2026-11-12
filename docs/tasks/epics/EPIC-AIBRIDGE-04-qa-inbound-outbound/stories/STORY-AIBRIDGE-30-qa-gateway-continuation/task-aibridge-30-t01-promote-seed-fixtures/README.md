# Task: fixtures — promote gateway seed stashed-201

**Status:** Done  
**P3 closed:** 2026-09-17T19:51:28Z  

**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-30-qa-gateway-continuation.md`  
**Parent story:** [`STORY-AIBRIDGE-30-qa-gateway-continuation.md`](../STORY-AIBRIDGE-30-qa-gateway-continuation.md)  
**P1 scaffold:** 2026-09-17T19:45:47Z  
**Maps:** GW-002 · TECH ADR-Q1 promote=copy · seed `gateway.stashed-201`

## Purpose

Copy package `fixtures/stashed-201.json` → `tests/fixtures/gateway/stashed-201.json`. Keep original in package `fixtures/` (do **not** move/delete). Verify hash_eq after promote.

**Out of this task:** generate GW-001…020 envelopes (t02); pytest (t03); Railway invent; live Telegram.

## AC/DoD

- [x] Matching **copy** exists under `tests/fixtures/gateway/stashed-201.json`.
- [x] Package original still present and unchanged path (hash_eq).
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/tests/fixtures/gateway/stashed-201.json` — **P3**
