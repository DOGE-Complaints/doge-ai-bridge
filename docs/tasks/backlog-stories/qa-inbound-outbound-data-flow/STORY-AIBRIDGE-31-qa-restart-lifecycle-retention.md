# STORY-AIBRIDGE-31-qa-restart-lifecycle-retention — QA — Restart, lifecycle, and retention

## Meta
- **Key:** `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention`
- **Status:** Implemented (P3 · next P4)
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** to `tests/fixtures/{cluster}/`
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §8 PostgreSQL persistence · §10.9 LIFE-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Materializing `task-*` / epic folders before explicit P1 (this story only **names** tasks).
- Deleting or moving package [`fixtures/`](./fixtures/) originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

## Context

PostgreSQL is SSOT for session/history/dedupe/tokens/locks/gateway attempts. Restart must recover without duplicate consequential side effects. TTL/GC must not break active sessions. Characterization for post-cancelled/stashed resume (LIFE-009/010).

## Use cases / matrix IDs (must transfer from guide)

| ID | Scenario | Expected |
|----|----------|----------|
| LIFE-001 | Graceful shutdown begins | New channel requests receive 503 `shutting_down`, retryable true. |
| LIFE-002 | Restart during ordinary interview | PostgreSQL history/session restored; no duplicate confirmed side effect. |
| LIFE-003 | Restart after buttons issued | Pending token remains usable until TTL, if persistence is active. |
| LIFE-004 | Restart after token consumed | Token remains consumed. |
| LIFE-005 | Restart with open gateway attempt | Mark unknown and require reconciliation. |
| LIFE-006 | Session inactive beyond TTL | New session; old narrative minimized/deleted; old tokens unusable. |
| LIFE-007 | Content bundle still referenced by active session | Bundle retained until safe GC. |
| LIFE-008 | Bundle unreferenced after grace period | Eligible for GC without breaking active sessions. |
| LIFE-009 | New message after `cancelled` | Characterization test: document whether current session restarts or remains terminal; raise mismatch if resident cannot start over. |
| LIFE-010 | New message after `stashed` | Characterization test: verify intended creation of next story/session; current behavior must not silently trap resident in terminal state. |
| LIFE-011 | Edit from `unknown_outcome` | New revision/interview allowed; old revision remains non-resendable. |
| LIFE-012 | Same deployment ID changes unexpectedly | Existing token must not become valid for a different deployment. |

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- **Originals (SSOT for generated envelopes):** [`fixtures/`](./fixtures/) — do **not** delete/move after promote.
- **Runtime test tree (after story execution):** `tests/fixtures/{cluster}/{name}.json` — **copy** from package `fixtures/` (or generate into package `fixtures/` first, then copy).
- Envelope: `schema_version=1.0` fields per [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §6.2.
- `task-*` folders below are **named only** — not materialized until explicit P1 (analysis.mdc: name ≠ create).

## Nested tasks (named — not materialized)

> Arch: [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 layers.  
> **Seed fixtures (package):** none yet — settings/channel/spies + rebuild_app_same_pg patterns  
> **Clusters:** `settings`, `channel`, `spies` · **Layer:** `tests/integration/` · **Harness:** disposable PG + `rebuild_app_same_pg`; fake clock for TTL

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-31-t01-generate-life-fixtures` | Todo | Generate LIFE-* envelopes into package `fixtures/` |
| **T02** | `task-aibridge-31-t02-promote-fixtures` | Todo | Copy to `tests/fixtures/{settings,channel,spies}/`; originals stay |
| **T03** | `task-aibridge-31-t03-implement-lifecycle-tests` | Todo | Restart/TTL/GC/characterization LIFE-009/010 capture-first |
| **T04** | `task-aibridge-31-t04-story-gate` | Todo | All LIFE-*; originals intact |

## Acceptance criteria

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] Guide **must** → automated asserts; **characterization** → capture-first.
- [ ] Nested tasks named in this story; `task-*` folders **not** created until P1.
- [ ] On story Done: all required envelopes exist under `tests/fixtures/{cluster}/` as **copies**; originals remain in package [`fixtures/`](./fixtures/).
