# STORY-AIBRIDGE-34 — QA — Product-journey scenarios (UC-01…10)

## Meta
- **Key:** `STORY-AIBRIDGE-34-qa-product-journey-scenarios`
- **Status:** 🟡 P5 scaffolded (t05–t07 Todo · next P6 · `run_mode=aibridge_34_audit_20260917`)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-34-qa-product-journey-scenarios.md`
- **decision_ref:** [`STORY-AIBRIDGE-34-qa-product-journey-scenarios.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-34-qa-product-journey-scenarios.md) · [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) §11 UC-01…10 · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) ADR-Q1/Q2
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 · ADR-Q1/Q2
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000033-20260917-epic-aibridge-04-story-34-qa-product-journey-scenarios.yaml`
- **P1 materialize:** 2026-09-17T21:14:24Z
- **Gate:** [t04](./task-aibridge-34-t04-story-gate/README.md) PASS · [acceptance](./task-aibridge-34-t04-story-gate/acceptance-verification-task-aibridge-34-t04-story-gate.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Guide §11 UC-01…10 | [`AIBRIDGE-QA-…-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) |
| ADR-Q1/Q2 fixtures | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| Traceability UC-01…10 | [`TRACEABILITY-MATRIX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md) |
| Seed originals | compose from prior clusters; generate UC packs on P3 t01 into package [`fixtures/`](../../../../backlog-stories/qa-inbound-outbound-data-flow/fixtures/) |
| Harness | `E2EHarness` / `story13_e2e_helpers` · disposable PG + Recording OpenAI + Recording Gateway |

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Deleting or moving package `fixtures/` originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

## Context

End-to-end resident journeys combining turns, actions, dry-run/live stash, cancel, ownership attack, retry storm, ambiguous timeout, geo mismatch, unsupported media, multilingual. Assertions include session/revision/token/gateway invariants from the guide.

## Use cases / matrix IDs (must transfer from guide)

| ID | Scenario | Expected (summary) |
|----|----------|-------------------|
| UC-01 | Normal interview, dry-run | dry_run_ok; zero gateway; stable session/revision/tokens |
| UC-02 | Normal live stash | one gateway post; stashed + draft_id + continuation URL |
| UC-03 | Cancel at first confirmation | cancelled; no FC; no gateway; LIFE-009 follow-up |
| UC-04 | Cancel before Send | frozen draft not posted; send tokens invalid |
| UC-05 | Group ownership attack | 403 forbidden; no gateway; no cross-user leak |
| UC-06 | Telegram retry storm | one OpenAI/gateway; deterministic replay |
| UC-07 | Ambiguous gateway timeout | unknown_outcome; no auto-retry |
| UC-08 | Geo scope mismatch | geo_scope_mismatch; no draft/URL |
| UC-09 | Unsupported Telegram content | adapter text-only / characterization capture-first |
| UC-10 | Multilingual story | raw preserved; gateway `{et,ru,en}` validates |

## Verified current state
- TRACEABILITY-MATRIX UC-01…10 → this story key (`covered`).
- Package UC journey packs — **present** (promote=copy).
- Suite `tests/integration/test_product_journey_scenarios.py` — **11 passed** (P3).
- Product: assert-only in P3; no product invent in P1.

## Target / AC
- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (if any) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] On story Done: required envelopes under `tests/fixtures/{cluster}/` as **copies**; originals remain in package `fixtures/`.

## Техническое решение

- **Approach (ADR-Q1/Q2):** compose/generate UC packs into package `fixtures/` (`schema_version=1.0`), promote=copy → `tests/fixtures/**`; parameterized E2E via E2EHarness; barriers not sleep; no live Telegram / Railway invent.
- **Skill:** python-pro · test-master

## Nested tasks (pkg-000033 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-34-t01-compose-uc-fixture-packs](./task-aibridge-34-t01-compose-uc-fixture-packs/README.md) | Compose/generate UC-01…10 packs | Done |
| t02 | [task-aibridge-34-t02-promote-uc-fixtures](./task-aibridge-34-t02-promote-uc-fixtures/README.md) | Promote copies → tests/fixtures | Done |
| t03 | [task-aibridge-34-t03-implement-journey-e2e](./task-aibridge-34-t03-implement-journey-e2e/README.md) | Parameterized UC E2E | Done |
| t04 | [task-aibridge-34-t04-story-gate](./task-aibridge-34-t04-story-gate/README.md) | Gate all UC-* | Done |
| t05 | [task-aibridge-34-t05-audit-g02-uc03-life009-followup](./task-aibridge-34-t05-audit-g02-uc03-life009-followup/README.md) | G-02 UC-03 LIFE-009 | Done |
| t06 | [task-aibridge-34-t06-audit-g04-uc07-restart-ambiguity](./task-aibridge-34-t06-audit-g04-uc07-restart-ambiguity/README.md) | G-04 UC-07 restart | Done |
| t07 | [task-aibridge-34-t07-audit-g03-uc01-revision-assert](./task-aibridge-34-t07-audit-g03-uc01-revision-assert/README.md) | G-03 UC-01 revision | Done |
