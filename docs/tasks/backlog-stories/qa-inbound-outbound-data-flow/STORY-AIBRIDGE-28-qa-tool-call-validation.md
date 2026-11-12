# STORY-AIBRIDGE-28-qa-tool-call-validation — QA — Tool-call validation

## Meta
- **Key:** `STORY-AIBRIDGE-28-qa-tool-call-validation`
- **Status:** Implemented (P3 · next P4)
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** to `tests/fixtures/{cluster}/`
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §6.3 · §10.6 TOOL-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Materializing `task-*` / epic folders before explicit P1 (this story only **names** tasks).
- Deleting or moving package [`fixtures/`](./fixtures/) originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

## Context

Only the allowlisted generated consequential function may appear. Server owns schema/origin fields. Invalid/extra tools fail closed before Send actions are exposed.

## Use cases / matrix IDs (must transfer from guide)

| ID | Scenario | Expected |
|----|----------|----------|
| TOOL-001 | Function call before `Looks right` | Blocked; no Send buttons/gateway. |
| TOOL-002 | Exactly one allowed call after interpretation confirmation | Three gates run; frozen intent persisted; Send buttons returned. |
| TOOL-003 | Two function calls | Rejected. |
| TOOL-004 | Unknown tool name | Rejected. |
| TOOL-005 | Missing call ID | Rejected. |
| TOOL-006 | Malformed argument string | Rejected. |
| TOOL-007 | Arguments are array/scalar | Rejected. |
| TOOL-008 | Gate 1 type/required/enum/const/bounds failure | Rejected before freeze. |
| TOOL-009 | Missing `structured_payload` | Gate 2 failure. |
| TOOL-010 | Node-pack payload violates active schema | Gate 2 failure. |
| TOOL-011 | Complete body violates gateway wire schema | Gate 3 failure. |
| TOOL-012 | Model tries to override server-owned schema/origin fields | Values stripped/replaced by server constants. |
| TOOL-013 | Persist failure before actions are returned | No Send actions exposed; fail closed. |
| TOOL-014 | Same call ID replay | No duplicate consequential execution. |

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- **Originals (SSOT for generated envelopes):** [`fixtures/`](./fixtures/) — do **not** delete/move after promote.
- **Runtime test tree (after story execution):** `tests/fixtures/{cluster}/{name}.json` — **copy** from package `fixtures/` (or generate into package `fixtures/` first, then copy).
- Envelope: `schema_version=1.0` fields per [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §6.2.
- `task-*` folders below are **named only** — not materialized until explicit P1 (analysis.mdc: name ≠ create).

## Nested tasks (materialized under EPIC-04 · pkg-000025)

> Arch: [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 layers.  
> **Seed fixtures (package):** none yet — generate openai tool-call + gateway schema-pin fixtures  
> **Clusters:** `openai`, `gateway` · **Layer:** `tests/unit/` primary · **Harness:** RecordingResponsesClient + validation context; gateway OAS pin  
> **Pipeline:** [`../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-28-qa-tool-call-validation/STORY-AIBRIDGE-28-qa-tool-call-validation.md`](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-28-qa-tool-call-validation/STORY-AIBRIDGE-28-qa-tool-call-validation.md)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-28-t01-generate-tool-seed-fixtures` | Done | Generate TOOL-* openai/gateway envelopes into package `fixtures/` (uus_veerenni_civic v3 payload) |
| **T02** | `task-aibridge-28-t02-promote-fixtures` | Done | Copy to `tests/fixtures/openai/` and `tests/fixtures/gateway/`; originals stay |
| **T03** | `task-aibridge-28-t03-implement-tool-gate-tests` | Done | Unit tests for gates 1–3 / allowlist / reject paths |
| **T04** | `task-aibridge-28-t04-story-gate` | Done | All TOOL-*; no Send on reject; originals intact |

## Acceptance criteria

- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (TOOL-014) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] Nested tasks named in this story; `task-*` folders materialized at P1.3 (2026-09-17T19:00:38Z).
- [x] On story Done: all required envelopes exist under `tests/fixtures/{cluster}/` as **copies**; originals remain in package [`fixtures/`](./fixtures/).
