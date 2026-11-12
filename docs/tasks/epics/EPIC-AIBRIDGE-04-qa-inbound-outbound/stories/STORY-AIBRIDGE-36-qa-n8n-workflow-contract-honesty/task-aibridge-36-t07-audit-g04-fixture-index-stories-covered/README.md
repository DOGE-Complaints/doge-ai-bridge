# Task: fixtures — sync fixture-index stories_covered 35–36 (G-04)

**Status:** Done · 2026-09-18T12:42:35Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_36_audit_20260918`  
**Gap:** G-04 (Medium) — P4 audit 2026-09-18  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty-20260918.md`  
**Parent story:** [`STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md`](../STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md)  
**P5 scaffold:** 2026-09-18T12:40:26Z
**P6 closed:** 2026-09-18T12:42:35Z  
**Maps:** fixture-index · STORY-35/36 · N8N-WF-001 row · ADR-Q1 promote=copy

## Purpose

Sync `fixture-index` `payload.stats.stories_covered` and envelope `story_keys` to include STORY-35 and STORY-36; bump `synced_at` (live utc at P6); promote=copy package ↔ `tests/fixtures/meta/`; assert in suite. Opportunistic: QUAL §4 count 224→225 (G-07 hygiene). **No** invent of n8n export body.

**Out of this task:** ops TRACEABILITY (t05); guide Layer E (t06); invent export; live TG; Railway; product invent.

## AC/DoD

- [x] `stories_covered` / envelope `story_keys` include STORY-35 and STORY-36; `synced_at` refreshed.
- [x] Package ↔ tests `fixture-index.json` hash_eq after promote=copy.
- [x] Suite asserts the sync (or equivalent meta check).
- [x] No invent export / live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- package `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/fixture-index.json` — **P6**
- `tests/fixtures/meta/fixture-index.json` — **P6** (promote=copy)
- optional: `TEST-QUALIFICATION-20260918.md` §4 count · suite assert — **P6**
