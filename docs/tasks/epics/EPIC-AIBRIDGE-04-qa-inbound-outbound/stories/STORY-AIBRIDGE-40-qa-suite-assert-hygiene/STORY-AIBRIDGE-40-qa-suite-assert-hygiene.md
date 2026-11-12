# STORY-AIBRIDGE-40 — QA — Suite assert hygiene

## Meta
- **Key:** `STORY-AIBRIDGE-40-qa-suite-assert-hygiene`
- **Status:** ✅ Done (P3) · P6 gap close · next P7 · `run_mode=aibridge_40_audit_20260918` · 2026-09-18T14:37:11Z
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-40-qa-suite-assert-hygiene.md`
- **decision_ref:** [`STORY-AIBRIDGE-40-….md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-40-qa-suite-assert-hygiene.md) · [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE-GAPS-36-40.md) §40
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Qualification:** closes **P1-Q1**, **P1-Q4**, **P2-Q2** (Q2 waived)
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000039-20260918-epic-aibridge-04-story-40-qa-suite-assert-hygiene.yaml` (immutable under `run_mode=aibridge_40_audit_20260918`)
- **P1 materialize:** 2026-09-18T14:25:26Z
- **P3 closed:** 2026-09-18T14:28:02Z · VAL band removed · hash_eq DoD · QUAL-003 WAIVE · VAL 21 passed
- **P5 APPLY:** 2026-09-18T14:35:15Z · t05–t06 scaffold
- **P6 closed:** 2026-09-18T14:37:11Z · G-01/G-02 CLOSED
- **Gate:** [t04](./task-aibridge-40-t04-story-gate/README.md) PASS · t05–t06 Done

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Gaps §40 QUAL-001…003 | [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE-GAPS-36-40.md) §40 |
| VAL characterization | `tests/contract/test_json_schema_boundary.py`::`test_val_characterization_capture_first` |
| Qualification SSOT | [`TEST-QUALIFICATION-20260918.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TEST-QUALIFICATION-20260918.md) |
| Traceability | [`TRACEABILITY-MATRIX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md) QUAL-001…003 |

## Scope
Suite honesty hygiene: remove VAL characterization tautology band; document hash_eq as **integrity-only**; QUAL-003 **WAIVE default** (gaps §40).

## Вне scope
- Gate-5 / live TG (STORY-37); invent non-Recording GW probe fixtures; CHAR-008 invent (STORY-39); counting hash_eq alone as matrix Expected.

## Context
P1-Q1 band tautology; P1-Q4 hash_eq integrity vs behavior; P2-Q2 Recording/memory — QUAL-003 WAIVED.

## Use cases / matrix IDs

| ID | Scenario | Expected |
|----|----------|----------|
| QUAL-001 | VAL characterization asserts | No tautology HTTP band; explicit expected status (+ shape) |
| QUAL-002 | Fixture promote hash_eq | Integrity-only; never sole matrix Expected |
| QUAL-003 | Optional non-Recording GW/PG probe | Explicit WAIVE (default) |

## Target / AC
- [x] QUAL-001…003 owned by this story key in TRACEABILITY.
- [x] VAL characterization has no vacuous HTTP-band-only success path.
- [x] hash_eq policy documented as integrity-only.
- [x] QUAL-003 waived with reason (gaps §40).
- [x] Nested tasks Done (2026-09-18T14:28:02Z).
- [x] No Gate-5 / live n8n claim.

## Nested tasks (pkg-000039 + audit override)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-40-t01-remove-val-tautology](./task-aibridge-40-t01-remove-val-tautology/README.md) | QUAL-001 VAL band remove | Done |
| t02 | [task-aibridge-40-t02-hash-eq-integrity-policy](./task-aibridge-40-t02-hash-eq-integrity-policy/README.md) | QUAL-002 integrity-only docs | Done |
| t03 | [task-aibridge-40-t03-optional-non-recording-probe](./task-aibridge-40-t03-optional-non-recording-probe/README.md) | QUAL-003 WAIVE default | Done |
| t04 | [task-aibridge-40-t04-story-gate](./task-aibridge-40-t04-story-gate/README.md) | TRACEABILITY + P1-Q1/Q4/P2-Q2 | Done · PASS |
| t05 | [task-aibridge-40-t05-audit-g01-backlog-ac-checkbox-sync](./task-aibridge-40-t05-audit-g01-backlog-ac-checkbox-sync/README.md) | G-01 backlog AC | Done |
| t06 | [task-aibridge-40-t06-audit-g02-qual-val-row-stale](./task-aibridge-40-t06-audit-g02-qual-val-row-stale/README.md) | G-02 QUAL §2 VAL | Done |
