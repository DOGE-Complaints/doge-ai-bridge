# Task: fixtures — sync fixture-index for stories 23–34

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-35-qa-gates-layers-dod.md`  
**Parent story:** [`STORY-AIBRIDGE-35-qa-gates-layers-dod.md`](../STORY-AIBRIDGE-35-qa-gates-layers-dod.md)  
**P1 scaffold:** 2026-09-17T21:40:06Z  
**P3 close:** 2026-09-17T21:45:30Z  
**Maps:** Gate-1…5 · meta index completeness · ADR-Q1/Q2

## Purpose

Update `fixture-index` rows for all promoted fixtures across stories 23–34; regenerate into package `fixtures/` first, then promote=copy to `tests/fixtures/meta/`. Do **not** delete/move package originals. Characterization rows remain capture-first labels — no silent product invent.

**Out of this task:** promote-only (t01); gates checklist (t03); live Gate-5; Railway invent.

## AC/DoD

- [x] Package `fixtures/fixture-index.json` lists promoted fixtures for stories 23–34 (and Gate/CHAR refs as applicable).
- [x] Copy under `tests/fixtures/meta/` hash_eq vs package original after sync.
- [x] Envelope `schema_version=1.0` preserved.
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/fixture-index.json` — **P3**
- `doge-ai-bridge/tests/fixtures/meta/fixture-index.json` — **P3**
