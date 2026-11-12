# Task: fixtures — generate ACT-* channel/spies envelopes

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-29-qa-action-token-fsm.md`  
**Parent story:** [`STORY-AIBRIDGE-29-qa-action-token-fsm.md`](../STORY-AIBRIDGE-29-qa-action-token-fsm.md)  
**P1 scaffold:** 2026-09-17T19:21:48Z  
**Maps:** ACT-001…018 · TECH ADR-Q1/Q2 envelope `schema_version=1.0`

## Purpose

Generate ACT-* channel actions + spies envelopes into package `fixtures/` first (`schema_version=1.0`). May reuse openai seed where needed. Do **not** delete/move existing package originals. Promote copies = **t02**.

**Out of this task:** copy to `tests/fixtures/` (t02); pytest (t03); Railway invent; live Telegram; product invent.

## AC/DoD

- [x] Package `fixtures/` holds envelopes covering ACT-001…018 (channel/spies/openai as needed).
- [x] Envelope fields per TECH §6.2 (`schema_version=1.0`).
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/` — **P3**
