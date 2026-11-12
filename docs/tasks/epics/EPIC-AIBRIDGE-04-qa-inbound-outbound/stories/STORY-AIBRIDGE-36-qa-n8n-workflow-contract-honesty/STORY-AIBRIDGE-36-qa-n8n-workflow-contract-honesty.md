# STORY-AIBRIDGE-36 — QA — n8n workflow pin + Layer E honesty

## Meta
- **Key:** `STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty`
- **Status:** ✅ Done (P3 · pkg-000035 · next P4 · 2026-09-18T12:32:14Z)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md`
- **decision_ref:** [`STORY-AIBRIDGE-36-….md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md) · [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE-GAPS-36-40.md) §36 · guide §1 Layer E
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Qualification:** closes **P0-Q1**, **P2-Q1**
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000035-20260918-epic-aibridge-04-story-36-qa-n8n-workflow-contract-honesty.yaml`
- **P1 materialize:** 2026-09-18T12:27:40Z
- **Gate:** [t04](./task-aibridge-36-t04-story-gate/README.md) PASS

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Gaps §36 N8N-WF-001 / Layer E honesty | [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE-GAPS-36-40.md) |
| Layer E / TECH §5.1 | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| STORY-25 fixture owner N8N-001…018 | backlog STORY-25 · `tests/n8n/` |
| Ops checklist (out-of-CI) | [`r3-p1-09-live-gate-checklist.md`](../../../../ops/n8n-channel-workflow/r3-p1-09-live-gate-checklist.md) |
| Export pin target | `docs/ops/n8n-channel-workflow/exports/aibridge-telegram-channel-v1.json` (operator; do not invent) |

## Scope
Make Layer E / STORY-25 coverage **honest**: `tests/n8n/` = adapter-contract; runtime n8n workflow pinned + optional out-of-CI smoke. Preserve guide §1 ownership.

## Вне scope
- Inventing export JSON body; Railway SUCCESS; live Telegram in default CI; Gate-5 (STORY-37); CHAR-008 Send/Edit (STORY-39); product FSM into n8n; delete/move package fixtures originals.

## Context
Qualification P0-Q1 / P2-Q1: `tests/n8n/` never executes workflow JSON / Bot API. STORY-25 remains fixture-contract owner; this story adds runtime pin + labeling honesty.

## Use cases / matrix IDs

| ID | Scenario | Expected |
|----|----------|----------|
| N8N-001…018 | Fixture mapping (STORY-25) | Remain fixture-covered; honesty cross-note → 36 |
| N8N-WF-001 | Workflow export pin + Layer E label | SHA pin or explicit defer; adapter-contract docs; optional out-of-CI smoke |

## Verified current state (P1 scaffold)
- EPIC-04 reused; STORY-36 pipeline materialized this APPLY.
- `tests/n8n/test_n8n_telegram_mapping.py` present (adapter-contract).
- Ops checklist present; exports dir may be empty until operator places file (P3 t02).
- Product: **none** in P1.

## Target / AC
- [x] TRACEABILITY: N8N-WF-001 + honesty notes for N8N-001…018 vs STORY-25.
- [x] Layer E docs do not claim live workflow e2e from `tests/n8n/` alone.
- [x] Pin present or explicit remaining defer; no invent export body.
- [x] No CHAR-008 / live TG / Railway invent.

## Nested tasks (pkg-000035 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-36-t01-relabel-layer-e-docs](./task-aibridge-36-t01-relabel-layer-e-docs/README.md) | Layer E adapter-contract relabel | Done |
| t02 | [task-aibridge-36-t02-pin-workflow-export](./task-aibridge-36-t02-pin-workflow-export/README.md) | N8N-WF-001 pin pointer + promote=copy | Done |
| t03 | [task-aibridge-36-t03-optional-out-of-ci-smoke](./task-aibridge-36-t03-optional-out-of-ci-smoke/README.md) | Out-of-CI smoke checklist bind | Done |
| t04 | [task-aibridge-36-t04-story-gate](./task-aibridge-36-t04-story-gate/README.md) | N8N-WF-001 / P0-Q1 / P2-Q1 gate | Done |
| t05 | [task-aibridge-36-t05-audit-g02-resync-ops-traceability](./task-aibridge-36-t05-audit-g02-resync-ops-traceability/README.md) | G-02 ops TRACEABILITY resync | Done |
| t06 | [task-aibridge-36-t06-audit-g03-guide-layer-e-honesty](./task-aibridge-36-t06-audit-g03-guide-layer-e-honesty/README.md) | G-03 guide Layer E honesty | Done |
| t07 | [task-aibridge-36-t07-audit-g04-fixture-index-stories-covered](./task-aibridge-36-t07-audit-g04-fixture-index-stories-covered/README.md) | G-04 fixture-index stories_covered | Done |

**P5 note (2026-09-18T12:40:26Z):** TASKED G-02/G-03/G-04 scaffolded · `run_mode=aibridge_36_audit_20260918` · next **P6** · G-01 WAIVED (no invent export).
**P6 note (2026-09-18T12:42:35Z):** G-02/G-03/G-04 CLOSED · pin honesty 6 passed · next **P7**.
