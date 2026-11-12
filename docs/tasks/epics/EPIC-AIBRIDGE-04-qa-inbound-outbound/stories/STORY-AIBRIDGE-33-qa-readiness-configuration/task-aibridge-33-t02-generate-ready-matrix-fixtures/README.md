# Task: fixtures — generate READY-001…015 settings envelopes

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-33-qa-readiness-configuration.md`  
**Parent story:** [`STORY-AIBRIDGE-33-qa-readiness-configuration.md`](../STORY-AIBRIDGE-33-qa-readiness-configuration.md)  
**P1 scaffold:** 2026-09-17T20:50:14Z
**P3 closed:** 2026-09-17T20:57:41Z  
**Maps:** READY-001…015 · TECH ADR-Q1/Q2 envelope `schema_version=1.0`

## Purpose

Generate READY-001…015 envelopes into package `fixtures/` first (`schema_version=1.0`; cluster `settings`), then copy to `tests/fixtures/settings/`. Do **not** delete/move package originals. Reuse seed READY-002 where applicable.

**Out of this task:** seed promote alone (t01); pytest (t03); Railway invent; live Telegram; product invent.

## AC/DoD

- [x] Package `fixtures/` holds envelopes covering READY-001…015 (settings cluster).
- [x] Matching **copies** under `tests/fixtures/settings/`; originals hash_eq.
- [x] Envelope fields per TECH §6.2 (`schema_version=1.0`).
- [x] No characterization invent for READY-* (must-rows only unless P3 marks capture-first).
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/` — **P3**
- `doge-ai-bridge/tests/fixtures/settings/` — **P3**
