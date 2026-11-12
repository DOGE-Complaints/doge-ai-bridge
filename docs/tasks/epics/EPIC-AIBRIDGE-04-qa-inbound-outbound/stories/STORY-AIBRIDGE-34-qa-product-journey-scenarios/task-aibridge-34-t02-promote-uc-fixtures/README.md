# Task: fixtures — promote UC journey envelopes

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-34-qa-product-journey-scenarios.md`  
**Parent story:** [`STORY-AIBRIDGE-34-qa-product-journey-scenarios.md`](../STORY-AIBRIDGE-34-qa-product-journey-scenarios.md)  
**P1 scaffold:** 2026-09-17T21:14:24Z  
**Maps:** UC-01…10 · TECH ADR-Q1 promote=copy

## Purpose

Copy any new UC envelopes from package `fixtures/` → `tests/fixtures/**` (cluster paths per envelope). Keep originals in package `fixtures/` (do **not** move/delete). Verify hash_eq after promote.

**Out of this task:** compose packs alone (t01); pytest (t03); Railway invent; live Telegram.

## AC/DoD

- [x] Matching **copies** under `tests/fixtures/{cluster}/` for all new UC envelopes.
- [x] Package originals still present and hash_eq vs copies.
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/tests/fixtures/` — **P3**
