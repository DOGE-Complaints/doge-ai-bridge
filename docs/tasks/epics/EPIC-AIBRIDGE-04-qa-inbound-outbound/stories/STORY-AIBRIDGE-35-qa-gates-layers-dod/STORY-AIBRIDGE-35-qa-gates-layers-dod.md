# STORY-AIBRIDGE-35 — QA — Test layers, gates, fixtures, characterization DoD

## Meta
- **Key:** `STORY-AIBRIDGE-35-qa-gates-layers-dod`
- **Status:** 🟡 Done (P3) (P1.3 · next P4)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-35-qa-gates-layers-dod.md`
- **decision_ref:** [`STORY-AIBRIDGE-35-qa-gates-layers-dod.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-35-qa-gates-layers-dod.md) · [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) §9/§15/§16/§18 · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) ADR-Q1/Q2
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 · ADR-Q1/Q2
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000034-20260917-epic-aibridge-04-story-35-qa-gates-layers-dod.yaml`
- **P1 materialize:** 2026-09-17T21:40:06Z
- **Gate:** [t04](./task-aibridge-35-t04-story-gate/README.md) (pending P3)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Guide §9 Layers A–F · §15 Gates · §16 CHAR · §18 DoD | [`AIBRIDGE-QA-…-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) |
| ADR-Q1/Q2 fixtures | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| Traceability Gate-1…5 · CHAR-001…008 | [`TRACEABILITY-MATRIX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md) |
| Seed originals | package [`fixtures/fixture-index.json`](../../../../backlog-stories/qa-inbound-outbound-data-flow/fixtures/fixture-index.json) → promote=copy |
| Harness | Index completeness + gate checklists; live Gate-5 / Layer F out of default CI |

## Scope
Automated **test/QA acceptance statements** covering Gate-1…5 and CHAR-001…008. Preserve ownership table from guide §1.

## Вне scope
- Deleting or moving package `fixtures/` originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

## Context

Program-level statement: which automation layers exist (unit→live smoke), pass/fail gates 1–5, required fakes/spies, and characterization items that must not be silently guessed. Binds acceptance program to stories 23–34; does not re-implement those suites.

## Use cases / matrix IDs (must transfer from guide)

| ID | Scenario | Expected (summary) |
|----|----------|-------------------|
| Gate-1 | channel contract | AUTH/VAL/N8N + OAS; no secrets in body/log/metrics |
| Gate-2 | interview safety | store=false; one OpenAI/event; no FC bypass confirm |
| Gate-3 | consequential-action safety | token/TTL/revision; one GW/revision; no auto-retry unknown |
| Gate-4 | durable runtime | migrations + /readyz; restart preserve; retention |
| Gate-5 | live channel | dry-run TG→n8n→aibridge; staging stash; **out of default CI** |
| CHAR-001…008 | characterization | capture-first / defer — no silent product invent |

## Verified current state
- TRACEABILITY-MATRIX Gate-1…5 · CHAR-001…008 → this story key (`covered`).
- Package `fixture-index.json` — **present**; `tests/fixtures/meta/fixture-index.json` — **absent** (promote P3 t01).
- Prior suites 23–34 exist; this story indexes/gates — create checklist on P3 t03.
- Product: assert-only in P3; no product invent in P1.

## Target / AC
- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs marked characterization — not silent product invent.
- [ ] Guide **must** → automated asserts; **characterization** → capture-first.
- [ ] On story Done: required envelopes under `tests/fixtures/{cluster}/` as **copies**; originals remain in package `fixtures/`.

## Техническое решение

- **Approach (ADR-Q1/Q2):** promote=copy meta index; sync fixture-index across 23–34; gates/layers checklist + CHAR capture/defer; Gate-5 live out of default CI.
- **Skill:** python-pro · test-master

## Nested tasks (pkg-000034 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-35-t01-promote-meta-index](./task-aibridge-35-t01-promote-meta-index/README.md) | Promote meta fixture-index | Todo |
| t02 | [task-aibridge-35-t02-sync-fixture-index](./task-aibridge-35-t02-sync-fixture-index/README.md) | Sync index rows 23–34 | Todo |
| t03 | [task-aibridge-35-t03-gates-layers-checklist](./task-aibridge-35-t03-gates-layers-checklist/README.md) | Gate-1…5 + CHAR checklist | Todo |
| t04 | [task-aibridge-35-t04-story-gate](./task-aibridge-35-t04-story-gate/README.md) | DoD §18 story gate | Todo |
