# STORY-AIBRIDGE-30-qa-gateway-continuation — QA — Gateway and SPA continuation

## Meta
- **Key:** `STORY-AIBRIDGE-30-qa-gateway-continuation`
- **Status:** Todo (statement only — no implementation in this wave)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §7 Gateway data flow · §10.8 GW-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Implementing tests, fixtures, or code changes in this story wave.
- Nested pipeline tasks / epic folders (name ≠ create until explicit P1).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent.

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

## Acceptance criteria (statement)

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] No nested implementation tasks created by this wave.
- [ ] Future automation must treat guide **must** as automated asserts; **characterization** as capture-first.
