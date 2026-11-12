# STORY-AIBRIDGE-37 — QA — Gate-5 live pilot evidence pack

## Meta
- **Key:** `STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence`
- **Status:** ✅ Done (P3) · P6 audit gaps CLOSED · next P7 · 2026-09-18T13:03:40Z
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md`
- **decision_ref:** [`STORY-AIBRIDGE-37-….md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md) · [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE-GAPS-36-40.md) §37 · guide §9 Layer F · §15 Gate-5
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Qualification:** closes **P0-Q2**, **P0-Q3**, **P2-Q3** (closed-with-defer)
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000036-20260918-epic-aibridge-04-story-37-qa-gate5-live-pilot-evidence.yaml` (immutable under `run_mode=aibridge_37_audit_20260918`)
- **P1 materialize:** 2026-09-18T12:50:58Z
- **P5 APPLY:** 2026-09-18T13:01:18Z · t05–t07 scaffold
- **P6 close:** 2026-09-18T13:03:40Z · G-02/G-03/G-04 CLOSED
- **Gate:** [t04](./task-aibridge-37-t04-story-gate/README.md) PASS · t05–t07 PASS

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Gaps §37 Gate-5 evidence | [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE-GAPS-36-40.md) |
| Guide §9 Layer F / §15 Gate-5 | Parent SSOT guide |
| UC-01…10 PG-journey owner | STORY-34 (≠ Gate-5) |
| Ops checklist (out-of-CI) | [`r3-p1-09-live-gate-checklist.md`](../../../../ops/n8n-channel-workflow/r3-p1-09-live-gate-checklist.md) |
| Default CI defer assert | `tests/test_qa_gates_layers_dod.py`::`test_gate5_live_deferred_out_of_default_ci` |
| Evidence index (execute) | package `fixtures/meta/gate5-evidence-index.json` (name ≠ create in P1) |

## Scope
Own **Gate-5 live channel** evidence out of default CI. UC-01…10 remain PG-journey under STORY-34. No invent live Telegram PASS / Railway SUCCESS.

## Вне scope
- Inventing live TG PASS / Railway SUCCESS; production Story submit; closing N8N-WF-001 (STORY-36) or CHAR-008 (STORY-39) alone; product invent; default-CI live automation; delete/move package fixtures originals.

## Context
P0-Q2 / P0-Q3 / P2-Q3: green UC ≠ Gate-5; default CI passes when `deferred_live` is recorded. Pilot env absent → WAIVE live PASS invent; keep defer explicit (capture-first).

## Use cases / matrix IDs

| ID | Scenario | Expected |
|----|----------|----------|
| Gate-5 | Live channel (guide §15) | Evidence pack accepted **or** explicit remaining defer; out of default CI |
| UC-01…10 | Product journeys | Remain PG-journey covered under STORY-34; not Gate-5 |

## Verified current state (P1 scaffold)
- EPIC-04 reused; STORY-37 pipeline materialized this APPLY.
- Gate-5 TRACEABILITY → this story · `deferred_live`.
- Ops checklist present; `gate5-evidence-index.json` absent until execute.
- Product: **none** in P1.

## Target / AC
- [x] TRACEABILITY: Gate-5 owned by this story; UC-01…10 ≠ Gate-5.
- [x] Pilot checklist covers guide §15 Gate-5 bullets.
- [x] Default CI remains without live TG / Railway invent.
- [x] Evidence pack accepted **or** explicit defer (no invent PASS).
- [x] P0-Q2 / P0-Q3 / P2-Q3 closed or remaining defer explicit.

## Nested tasks (pkg-000036 + audit override)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-37-t01-uc-vs-gate5-docs](./task-aibridge-37-t01-uc-vs-gate5-docs/README.md) | UC ≠ Gate-5 docs cross-links | Done |
| t02 | [task-aibridge-37-t02-pilot-checklist](./task-aibridge-37-t02-pilot-checklist/README.md) | r3-p1-09 §15 Gate-5 map | Done |
| t03 | [task-aibridge-37-t03-evidence-pack](./task-aibridge-37-t03-evidence-pack/README.md) | gate5-evidence-index or defer WAIVE | Done |
| t04 | [task-aibridge-37-t04-story-gate](./task-aibridge-37-t04-story-gate/README.md) | deferred_live\|pass_with_evidence gate | Done |
| t05 | [task-aibridge-37-t05-audit-g02-qual-closed-with-defer](./task-aibridge-37-t05-audit-g02-qual-closed-with-defer/README.md) | G-02 QUAL closed-with-defer | Done |
| t06 | [task-aibridge-37-t06-audit-g03-checklist-g3-assert](./task-aibridge-37-t06-audit-g03-checklist-g3-assert/README.md) | G-03 suite G3 assert | Done |
| t07 | [task-aibridge-37-t07-audit-g04-honesty-count-docs](./task-aibridge-37-t07-audit-g04-honesty-count-docs/README.md) | G-04 honesty count 5→4 | Done |
