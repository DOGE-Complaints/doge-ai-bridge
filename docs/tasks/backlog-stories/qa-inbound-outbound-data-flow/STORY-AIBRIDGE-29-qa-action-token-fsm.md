# STORY-AIBRIDGE-29-qa-action-token-fsm — QA — Action token and dual-confirm FSM

## Meta
- **Key:** `STORY-AIBRIDGE-29-qa-action-token-fsm`
- **Status:** Implemented (P6 closed · pkg-000026 immutable · next P7)
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** to `tests/fixtures/{cluster}/`
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §5.2–5.4 · §10.7 ACT-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Materializing `task-*` / epic folders before explicit P1 (this story only **names** tasks).
- Deleting or moving package [`fixtures/`](./fixtures/) originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

## Context

Opaque tokens ≤64 bytes travel in callback_data; only hashes persist. Dual-confirm FSM + freeze-before-send: model cannot authorize gateway; only valid confirm_send consume does. Ownership/revision/deployment/draft_hash must bind.

## Use cases / matrix IDs (must transfer from guide)

| ID | Scenario | Expected |
|----|----------|----------|
| ACT-001 | Valid `Looks right` token by owner | 200; `interpretation_confirmed`; zero gateway calls. |
| ACT-002 | Valid Edit token | 200; `interviewing`; revision incremented; sibling tokens invalidated. |
| ACT-003 | Valid Cancel token | 200; `cancelled`; pending tokens invalidated; no gateway. |
| ACT-004 | Valid Send token | One authorized attempt using frozen body. |
| ACT-005 | Random token | 404 `not_found`. |
| ACT-006 | Token owned by different user | 403 `forbidden`. |
| ACT-007 | Correct user, different chat | 403. |
| ACT-008 | Expired token | 409 `conflict`. |
| ACT-009 | Already consumed token, new event ID | 409. |
| ACT-010 | Invalidated sibling token after another action | 409. |
| ACT-011 | Token revision differs from session | 409. |
| ACT-012 | Token expected state differs | 409. |
| ACT-013 | Token deployment differs | 409 for Send. |
| ACT-014 | Draft hash differs | 409 for Send. |
| ACT-015 | Frozen tool intent missing | 409; gateway not called. |
| ACT-016 | Illegal FSM transition | 409. |
| ACT-017 | Raw token found in PostgreSQL/logs | Fail security test; only hash may persist. |
| ACT-018 | Token longer than Telegram limit | 422 at façade; generated tokens must remain ≤64 bytes. |

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- **Originals (SSOT for generated envelopes):** [`fixtures/`](./fixtures/) — do **not** delete/move after promote.
- **Runtime test tree (after story execution):** `tests/fixtures/{cluster}/{name}.json` — **copy** from package `fixtures/` (or generate into package `fixtures/` first, then copy).
- Envelope: `schema_version=1.0` fields per [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §6.2.
- `task-*` folders below are **named only** — not materialized until explicit P1 (analysis.mdc: name ≠ create).

## Nested tasks (materialized under EPIC-04 · pkg-000026)

> Arch: [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 layers.  
> **Seed fixtures (package):** none yet — generate channel actions + spies; may reuse openai seed  
> **Clusters:** `channel`, `openai`, `spies` · **Layer:** `tests/unit/` + `tests/integration/` · **Harness:** create_app + ConfirmationGuard; fake clock for TTL  
> **Pipeline:** [`../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-29-qa-action-token-fsm/STORY-AIBRIDGE-29-qa-action-token-fsm.md`](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-29-qa-action-token-fsm/STORY-AIBRIDGE-29-qa-action-token-fsm.md)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-29-t01-generate-act-fixtures` | Done | Generate ACT-* channel/spies envelopes into package `fixtures/` |
| **T02** | `task-aibridge-29-t02-promote-fixtures` | Done | Copy to `tests/fixtures/{channel,spies}/`; originals stay |
| **T03** | `task-aibridge-29-t03-implement-fsm-token-tests` | Done | FSM/token tests; zero gateway on Looks right/Edit/Cancel |
| **T04** | `task-aibridge-29-t04-story-gate` | Done | All ACT-*; only hash in PG; originals intact |
| **T05** | `task-aibridge-29-t05-audit-g01-act017-pg-hash-only` | Done | P5 G-01 ACT-017 PG/logs hash-only |
| **T06** | `task-aibridge-29-t06-audit-g02-fixture-expect-ssot` | Done | P5 G-02 fixture expect SSOT |

## Acceptance criteria

- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (if any) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] Nested tasks named in this story; `task-*` folders materialized at P1.3 (2026-09-17T19:21:48Z).
- [x] On story Done: all required envelopes exist under `tests/fixtures/{cluster}/` as **copies**; originals remain in package [`fixtures/`](./fixtures/).
