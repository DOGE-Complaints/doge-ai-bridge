# Task: fixtures — compose UC-01…10 journey packs

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-34-qa-product-journey-scenarios.md`  
**Parent story:** [`STORY-AIBRIDGE-34-qa-product-journey-scenarios.md`](../STORY-AIBRIDGE-34-qa-product-journey-scenarios.md)  
**P1 scaffold:** 2026-09-17T21:14:24Z  
**Maps:** UC-01…10 · TECH ADR-Q1/Q2 envelope `schema_version=1.0`

## Purpose

Ensure UC-01…10 packs reference promoted prior-cluster fixtures; generate missing envelopes into package `fixtures/` first (`schema_version=1.0`). Do **not** delete/move package originals. Characterization capture-first for UC-06/09 adapter seams — no silent product invent.

**Out of this task:** promote copies (t02); pytest (t03); Railway invent; live Telegram; product invent.

## AC/DoD

- [x] Package `fixtures/` holds UC-01…10 journey envelopes (and/or indexes) covering matrix IDs.
- [x] Envelope fields per TECH §6.2 (`schema_version=1.0`).
- [x] Characterization IDs (if any) explicitly marked — not silent invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/` — **P3**
