# STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty — QA — n8n workflow pin + Layer E honesty

## Meta
- **Key:** `STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty`
- **Status:** Done (P3 · pkg-000035 · next P4 · 2026-09-18T12:32:14Z)
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Tech arch gaps:** [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](./TECHNICAL-ARCHITECTURE-GAPS-36-40.md) **§36**
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** to `tests/fixtures/{cluster}/` (when execute wave creates them)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Qualification:** [`TEST-QUALIFICATION-20260918.md`](./TEST-QUALIFICATION-20260918.md) — closes **P0-Q1**, **P2-Q1**
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-18 · from test qualification gap closure (operator package ask)

## Scope
Task statements to make Layer E / STORY-25 coverage **honest**: fixture-driven `tests/n8n/` remains adapter-contract; runtime n8n workflow is pinned and optionally smoked **outside default CI**. Preserve ownership table from guide §1.

## Вне scope
- Materializing `task-*` / epic folders before explicit P1 (this story only **names** tasks).
- Implementing pytest/product changes in this Scaffolded wave.
- Live Telegram Gate-5 (owned by STORY-37).
- Deleting package [`fixtures/`](./fixtures/) originals.
- Moving product FSM/OpenAI/gateway logic into n8n.

## Context

Qualification P0-Q1: `tests/n8n/` asserts fixture flags and Python helpers — never executes exported n8n workflow JSON or Bot API. Matrix N8N-001…018 Expected describes live adapter behavior → false confidence if marked only «covered». P2-Q1: over-mock relative to «n8n layer» name.

STORY-25 stays the fixture-contract owner. This story adds **runtime pin + labeling honesty**.

## Use cases / matrix IDs

| ID | Scenario | Expected |
|----|----------|----------|
| N8N-001…018 | (existing) Fixture mapping / ack order / keyboard | Remain **fixture-covered** under STORY-25; TRACEABILITY note points here for runtime honesty |
| **N8N-WF-001** | Production (or staging) n8n workflow export pinned in package | SHA-pinned export (or documented path) matches ops workflow used for pilot; Layer E docs call `tests/n8n/` **adapter-contract**, not live workflow e2e; optional out-of-CI smoke checklist named (no invent Railway SUCCESS) |

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- **Originals (SSOT for generated envelopes):** [`fixtures/`](./fixtures/) — do **not** delete/move after promote.
- **Runtime test tree (after story execution):** `tests/fixtures/{cluster}/{name}.json` — **copy** from package `fixtures/`.
- Envelope: `schema_version=1.0` fields per [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §6.2.
- `task-*` folders below are **named only** — not materialized until explicit P1 (analysis.mdc: name ≠ create).

## Nested tasks (named — not materialized)

> Arch: [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](./TECHNICAL-ARCHITECTURE-GAPS-36-40.md) **§36**.  
> **Clusters:** `n8n`, `meta` · **Layer:** Layer E honesty + out-of-CI smoke · **Harness:** ops export pin / docs; no live TG in default CI  
> `task-*` folders **named only** — not materialized until explicit P1 (analysis.mdc: name ≠ create).

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-36-t01-relabel-layer-e-docs` | Done | Relabel Layer E in package INDEX + [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §5.1 + STORY-25 context: `tests/n8n/` = **adapter-contract** (fixture + Python helpers), not workflow e2e; TRACEABILITY N8N-001…018 stay fixture-covered |
| **T02** | `task-aibridge-36-t02-pin-workflow-export` | Done | Operator adds credential-stripped export at `docs/ops/n8n-channel-workflow/exports/aibridge-telegram-channel-v1.json` (do not invent body); package pointer `fixtures/meta/n8n-wf-001-pin-pointer.json` with sha256 + relative_path + verified_at; promote copy to `tests/fixtures/meta/` |
| **T03** | `task-aibridge-36-t03-optional-out-of-ci-smoke` | Done | Bind/extend [`r3-p1-09-live-gate-checklist.md`](../../../ops/n8n-channel-workflow/r3-p1-09-live-gate-checklist.md) as out-of-CI smoke for pinned export; **not** added to default pytest in TEST-MANUAL |
| **T04** | `task-aibridge-36-t04-story-gate` | Done | N8N-WF-001 coverage honest (open→covered only with pin or explicit remaining defer); P0-Q1/P2-Q1 closed per gaps arch §36 |

## Acceptance criteria

- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key where applicable.
- [x] N8N-001…018 coverage labels distinguish fixture-covered (25) from runtime pin (36 / N8N-WF-001).
- [x] Layer E naming in package docs does not claim live workflow execution from `tests/n8n/` alone.
- [x] Nested tasks named in this story; `task-*` folders **not** created until P1.
- [x] No product invent of Send/Edit policy (CHAR-008 → STORY-39).
