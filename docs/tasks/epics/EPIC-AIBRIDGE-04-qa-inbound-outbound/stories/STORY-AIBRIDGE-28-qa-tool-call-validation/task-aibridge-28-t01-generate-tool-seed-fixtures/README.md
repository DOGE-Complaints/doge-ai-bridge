# Task: fixtures — generate TOOL-* openai/gateway envelopes

**Status:** Done  
**P3 closed:** 2026-09-17T19:07:11Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-28-qa-tool-call-validation.md`  
**Parent story:** [`STORY-AIBRIDGE-28-qa-tool-call-validation.md`](../STORY-AIBRIDGE-28-qa-tool-call-validation.md)  
**P1 scaffold:** 2026-09-17T19:00:38Z  
**Maps:** TOOL-001…014 · TECH ADR-Q1/Q2 envelope `schema_version=1.0` · `uus_veerenni_civic` v3

## Purpose

Generate TOOL-* openai tool-call + gateway schema-pin envelopes into package `fixtures/` first (`schema_version=1.0`). Civic node-pack payload: `uus_veerenni_civic` v3. Do **not** delete/move existing package originals. Promote copies = **t02**.

## AC/DoD

- [x] Package `fixtures/` holds envelopes covering TOOL-001…014 (openai + gateway clusters as needed).
- [x] Envelope fields per TECH §6.2 (`schema_version=1.0`).
- [x] Payload uses `uus_veerenni_civic` v3 where node-pack relevant.
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/tool-*.json` — **Done**
