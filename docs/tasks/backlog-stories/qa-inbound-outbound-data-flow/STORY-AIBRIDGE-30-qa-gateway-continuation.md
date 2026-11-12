# STORY-AIBRIDGE-30-qa-gateway-continuation — QA — Gateway and SPA continuation

## Meta
- **Key:** `STORY-AIBRIDGE-30-qa-gateway-continuation`
- **Status:** Implemented (P3 · gate PASS · next P4)
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** to `tests/fixtures/{cluster}/`
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §7 Gateway data flow · §10.8 GW-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Materializing `task-*` / epic folders before explicit P1 (this story only **names** tasks).
- Deleting or moving package [`fixtures/`](./fixtures/) originals (promote = **copy** only).
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

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- **Originals (SSOT for generated envelopes):** [`fixtures/`](./fixtures/) — do **not** delete/move after promote.
- **Runtime test tree (after story execution):** `tests/fixtures/{cluster}/{name}.json` — **copy** from package `fixtures/` (or generate into package `fixtures/` first, then copy).
- Envelope: `schema_version=1.0` fields per [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §6.2.
- `task-*` folders below are **named only** — not materialized until explicit P1 (analysis.mdc: name ≠ create).

## Nested tasks (materialized under EPIC-04 · pkg-000027)

> Arch: [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 layers.  
> **Seed fixtures (package):** `gateway.stashed-201` (GW-002)  
> **Clusters:** `gateway`, `channel`, `spies` · **Layer:** `tests/integration/` · **Harness:** RecordingGatewayTransport; dry-run vs scripted 201  
> **Pipeline:** [`../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-30-qa-gateway-continuation/STORY-AIBRIDGE-30-qa-gateway-continuation.md`](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-30-qa-gateway-continuation/STORY-AIBRIDGE-30-qa-gateway-continuation.md)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-30-t01-promote-seed-fixtures` | Scaffolded | Copy `stashed-201.json` → `tests/fixtures/gateway/`; original stays |
| **T02** | `task-aibridge-30-t02-generate-gw-matrix-fixtures` | Scaffolded | Generate GW-001…020 into package `fixtures/`, copy to `tests/fixtures/gateway/` (+ spies as needed) |
| **T03** | `task-aibridge-30-t03-implement-gateway-outcome-tests` | Scaffolded | Map status→outcome; continuation URL; no redirect follow |
| **T04** | `task-aibridge-30-t04-story-gate` | Scaffolded | All GW-*; no Channel Bearer on gateway capture; originals intact |

## Acceptance criteria

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] Nested tasks named in this story; `task-*` folders materialized at P1.3 (2026-09-17T19:45:47Z).
- [ ] On story Done: all required envelopes exist under `tests/fixtures/{cluster}/` as **copies**; originals remain in package [`fixtures/`](./fixtures/).
