# Task: fixtures — generate LIFE-001…012 matrix envelopes

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md`  
**Parent story:** [`STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md`](../STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md)  
**P1 scaffold:** 2026-09-17T20:05:23Z  
**Maps:** LIFE-001…012 · TECH ADR-Q1/Q2 envelope `schema_version=1.0`

## Purpose

Generate LIFE-001…012 envelopes into package `fixtures/` first (`schema_version=1.0`; settings/channel/spies as needed). Mark LIFE-009/010 notes as characterization. Do **not** delete/move package originals.

**Out of this task:** promote copies (t02); pytest (t03); Railway invent; live Telegram; product invent.

## AC/DoD

- [x] Package `fixtures/` holds envelopes covering LIFE-001…012 (settings/channel/spies as needed).
- [x] Envelope fields per TECH §6.2 (`schema_version=1.0`).
- [x] LIFE-009/010 notes include characterization.
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/` — **P3**
