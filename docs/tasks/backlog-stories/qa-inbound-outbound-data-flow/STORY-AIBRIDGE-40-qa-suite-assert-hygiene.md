# STORY-AIBRIDGE-40-qa-suite-assert-hygiene — QA — Suite assert hygiene

## Meta
- **Key:** `STORY-AIBRIDGE-40-qa-suite-assert-hygiene`
- **Status:** Done (P3 · P6 gap close · pkg-000039 · `run_mode=aibridge_40_audit_20260918` · 2026-09-18T14:37:11Z)
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Tech arch gaps:** [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](./TECHNICAL-ARCHITECTURE-GAPS-36-40.md) **§40**
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** when execute creates them
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Qualification:** [`TEST-QUALIFICATION-20260918.md`](./TEST-QUALIFICATION-20260918.md) — closes **P1-Q1**, **P1-Q4**, **P2-Q2**
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-18 · from test qualification gap closure (operator package ask)
- **Pipeline:** [`../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-40-qa-suite-assert-hygiene/STORY-AIBRIDGE-40-qa-suite-assert-hygiene.md`](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-40-qa-suite-assert-hygiene/STORY-AIBRIDGE-40-qa-suite-assert-hygiene.md)

## Scope
Task statements for suite honesty hygiene: remove VAL characterization tautology band; document hash_eq as **integrity-only**; optionally add a named non-Recording GW/PG probe (not Gate-5).

## Вне scope
- Gate-5 / live TG (STORY-37); OAI channel product decision (STORY-38); CHAR-008 capture invent (STORY-39).
- Counting hash_eq alone as matrix Expected behavior.
- Invent non-Recording GW probe fixtures (QUAL-003 WAIVED).

## Context

P1-Q1: **closed (P3)** — vacuous `100 <= status < 600` band **removed**; VAL-014/018 keep explicit `== 200`.  
P1-Q4: **closed (P3)** — `*_hash_eq*` = integrity-only DoD (INDEX + gaps §40).  
P2-Q2: **closed-with-waive (P3)** — QUAL-003 WAIVE (UC+LIFE-live PG; Recording GW sufficient).

## Use cases / matrix IDs

| ID | Scenario | Expected |
|----|----------|----------|
| **QUAL-001** | VAL characterization asserts | No tautology HTTP band; explicit expected status (+ shape) for VAL-014/018 (and similar) |
| **QUAL-002** | Fixture promote hash_eq | Documented as integrity-only in DoD/INDEX/story AC; never sole evidence for matrix Expected |
| **QUAL-003** | Optional non-Recording GW or real-PG concurrency probe | Explicit WAIVE with reason (gaps §40) |

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- No new fixture invent required for QUAL-001/002.
- QUAL-003 WAIVED — no spy/GW fixture invent.
- Nested `task-*` materialized under EPIC-04 (P1.3 → P3 Done).

## Nested tasks (pipeline)

> Arch: [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](./TECHNICAL-ARCHITECTURE-GAPS-36-40.md) **§40**.  
> **Layers:** B_contract (VAL), program DoD (hash_eq), QUAL-003 **WAIVE**  
> Footnote: «named only until P1» applied pre-materialize; folders exist post P1.3 APPLY 2026-09-18T14:25:26Z.

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-40-t01-remove-val-tautology` | Done | Band removed; VAL-014/018 explicit 200 |
| **T02** | `task-aibridge-40-t02-hash-eq-integrity-policy` | Done | hash_eq integrity-only DoD |
| **T03** | `task-aibridge-40-t03-optional-non-recording-probe` | Done | QUAL-003 WAIVE recorded |
| **T04** | `task-aibridge-40-t04-story-gate` | Done · PASS | QUAL-001…003 TRACEABILITY; P1-Q1/Q4/P2-Q2 closed/waived |
| **T05** | `task-aibridge-40-t05-audit-g01-backlog-ac-checkbox-sync` | Done | G-01 backlog AC sync (this file) |
| **T06** | `task-aibridge-40-t06-audit-g02-qual-val-row-stale` | Done | G-02 QUAL §2 VAL row |

## Acceptance criteria

- [x] QUAL-001…003 appear in TRACEABILITY-MATRIX with this story key.
- [x] VAL characterization has no vacuous HTTP-band-only success path.
- [x] hash_eq policy documented as integrity-only.
- [x] QUAL-003 explicitly waived with reason (gaps §40).
- [x] Nested tasks materialized and Done (P1.3+; footnote: pre-P1 naming only).
- [x] Does not claim Gate-5 or live n8n workflow closed.
