# STORY-AIBRIDGE-30 — QA — Gateway and SPA continuation

## Meta
- **Key:** `STORY-AIBRIDGE-30-qa-gateway-continuation`
- **Status:** 🟢 Implemented (P3 · next P4)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-30-qa-gateway-continuation.md`
- **decision_ref:** [`STORY-AIBRIDGE-30-qa-gateway-continuation.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-30-qa-gateway-continuation.md) · [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) §7 · §10.8 GW-* · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) ADR-Q1/Q2
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 · ADR-Q1/Q2
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000027-20260917-epic-aibridge-04-story-30-qa-gateway-continuation.yaml`
- **P1 materialize:** 2026-09-17T19:45:47Z
- **P3 closed:** 2026-09-17T19:51:28Z
- **Gate:** [t04](./task-aibridge-30-t04-story-gate/README.md) · [acceptance PASS](./task-aibridge-30-t04-story-gate/acceptance-verification-task-aibridge-30-t04-story-gate.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Guide §7 / §10.8 GW-* | [`AIBRIDGE-QA-…-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) |
| ADR-Q1/Q2 fixtures | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| Traceability GW-001…020 | [`TRACEABILITY-MATRIX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md) |
| Seed originals | package [`fixtures/stashed-201.json`](../../../../backlog-stories/qa-inbound-outbound-data-flow/fixtures/stashed-201.json) |
| Harness | `RecordingGatewayTransport` · `GatewayExecutor` · dry-run vs scripted 201 |

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Deleting or moving package `fixtures/` originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

## Context

Gateway uses separate Bearer and frozen body only. Dry-run must not HTTP. Outcomes map to resident-safe envelopes; unknown_outcome blocks auto-resend. Continuation URL embeds draft_id; never claim published.

## Use cases / matrix IDs (must transfer from guide)

| ID | Scenario | Expected |
|----|----------|----------|
| GW-001 | Dry-run Send | `dry_run_ok`; no HTTP transport call; no published/stashed claim. |
| GW-002 | Valid 201 | `stashed`, state `stashed`, URL-encoded continuation URL. |
| GW-003 | 201 missing `trace_id` | `contract_mismatch`. |
| GW-004 | 201 missing `draft_id` | `contract_mismatch`. |
| GW-005 | 201 invalid JSON/non-object | `contract_mismatch`. |
| GW-006 | 400 | `validation_error`. |
| GW-007 | 401 | `gateway_unauthorized`; no credential leak. |
| GW-008 | 422 | `geo_scope_mismatch`. |
| GW-009 | 429 | `transient_failure`. |
| GW-010 | 500–599 | `transient_failure`. |
| GW-011 | Timeout/disconnect after attempted post | `unknown_outcome`; same revision cannot auto-Send again. |
| GW-012 | Unusual status such as 204/409 | `unknown_outcome` under current mapping. |
| GW-013 | Redirect response/final URL changes | `contract_mismatch`; no redirect follow. |
| GW-014 | Oversized response | `contract_mismatch`. |
| GW-015 | Non-HTTPS origin | readiness/executor fails closed. |
| GW-016 | Channel and gateway Bearers equal | readiness fails; no traffic accepted as ready. |
| GW-017 | Gateway call attempted from interpretation confirmation | Fail test; zero calls. |
| GW-018 | Gateway call attempted from Edit/Cancel | Fail test. |
| GW-019 | Restart while attempt is `executing` | Recover to `unknown_outcome`; do not resend automatically. |
| GW-020 | Function-call follow-up fails after successful stash | Stash outcome remains authoritative. |

## Verified current state
- Seed `stashed-201` promoted (copy) → `tests/fixtures/gateway/stashed-201.json`; package original intact.
- TRACEABILITY-MATRIX GW-001…020 → this story key (`covered`).
- Layer `tests/integration/test_gateway_continuation.py` — GW matrix suite (22 passed).
- Product: `src/aibridge/gateway.py` RecordingGatewayTransport / GatewayExecutor; create_app readiness — assert-only.

## Target / AC
- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (GW-012) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] On story Done: required envelopes under `tests/fixtures/{cluster}/` as **copies**; originals remain in package `fixtures/`.

## Техническое решение

- **Approach (ADR-Q1/Q2):** promote seed `stashed-201` copy → `tests/fixtures/gateway/`; generate GW-* into package `fixtures/`, promote=copy; tests in `tests/integration/`; RecordingGatewayTransport; dry-run vs scripted 201; no live Telegram.
- **Skill:** python-pro · test-master

## Nested tasks (pkg-000027 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-30-t01-promote-seed-fixtures](./task-aibridge-30-t01-promote-seed-fixtures/README.md) | Promote stashed-201 seed | Done |
| t02 | [task-aibridge-30-t02-generate-gw-matrix-fixtures](./task-aibridge-30-t02-generate-gw-matrix-fixtures/README.md) | Generate GW-001…020 + promote | Done |
| t03 | [task-aibridge-30-t03-implement-gateway-outcome-tests](./task-aibridge-30-t03-implement-gateway-outcome-tests/README.md) | Gateway outcome suite | Done |
| t04 | [task-aibridge-30-t04-story-gate](./task-aibridge-30-t04-story-gate/README.md) | Gate all GW-* | Done |
| t05 | [task-aibridge-30-t05-audit-g01-gw019-pg-boot-recover](./task-aibridge-30-t05-audit-g01-gw019-pg-boot-recover/README.md) | P5 G-01 GW-019 PG/boot | Done |
| t06 | [task-aibridge-30-t06-audit-g02-gw011-spy-resend](./task-aibridge-30-t06-audit-g02-gw011-spy-resend/README.md) | P5 G-02 GW-011 spy/resend | Done |
