# STORY-AIBRIDGE-25-qa-n8n-telegram-mapping — QA — n8n and Telegram mapping

## Meta
- **Key:** `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping`
- **Status:** 🟢 Implemented (P6 closed · next P7)
- **Pipeline:** [`STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md`](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md)
- **Active pkg:** `pkg-000022-20260917-epic-aibridge-04-story-25-qa-n8n-telegram-mapping.yaml`
- **P1 materialize:** 2026-09-17T17:39:14Z
- **P3 closed:** 2026-09-17T17:44:23Z
- **Gate:** [acceptance-verification … t04](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping/task-aibridge-25-t04-story-gate/acceptance-verification-task-aibridge-25-t04-story-gate.md) PASS
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** to `tests/fixtures/{cluster}/`
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §3 E2E flows · §10.3 N8N-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Deleting or moving package [`fixtures/`](./fixtures/) originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

## Context

n8n is a thin adapter only: map update→request, answerCallbackQuery before `/actions`, map response→Telegram. Ownership of FSM/OpenAI/gateway stays in aibridge. Order `answerCallbackQuery → /actions → Send/Edit` is mandatory.

## Use cases / matrix IDs (must transfer from guide)

| ID | Scenario | Expected |
|----|----------|----------|
| N8N-001 | Private text message | Correct `/turns` mapping; one reply. |
| N8N-002 | `/start` command | Sent as ordinary text; model/instructions decide response. |
| N8N-003 | Russian text | Unicode preserved; language hint optional. |
| N8N-004 | Estonian text | Unicode preserved. |
| N8N-005 | Mixed-language message | Text unchanged; hint must not override actual content. |
| N8N-006 | Emoji and combining characters | Round-trip without corruption. |
| N8N-007 | Group message from user A | Principal = A + group chat. |
| N8N-008 | Same group message from user B | Separate session. |
| N8N-009 | Edited message update | Must not be silently treated as a new ordinary message unless workflow explicitly supports it. |
| N8N-010 | Photo/document/voice without text | Do not build invalid `/turns`; route to explicit unsupported-content response or future adapter. |
| N8N-011 | Media with caption | Product decision/characterization: caption may be mapped as text only if workflow explicitly documents it. |
| N8N-012 | Channel post, poll, shipping/pre-checkout update | Must not enter this workflow branch. |
| N8N-013 | Callback query | `answerCallbackQuery` occurs before `/actions`. |
| N8N-014 | aibridge slow/unavailable after callback | Telegram callback still acknowledged promptly; later resident-safe error handling. |
| N8N-015 | `actions=[]` | No inline keyboard added. |
| N8N-016 | Three actions | Labels/tokens mapped in order; token unchanged. |
| N8N-017 | `outcome=stashed` | Render continuation link; do not claim publication. |
| N8N-018 | Non-stashed outcome with accidental draft/URL | Adapter should not present link; contract test should fail producer inconsistency. |

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- **Originals (SSOT for generated envelopes):** [`fixtures/`](./fixtures/) — do **not** delete/move after promote.
- **Runtime test tree (after story execution):** `tests/fixtures/{cluster}/{name}.json` — **copy** from package `fixtures/` (or generate into package `fixtures/` first, then copy).
- Envelope: `schema_version=1.0` fields per [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §6.2.

## Nested tasks (materialized under EPIC-04)

> Arch: [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 layers.  
> **Seed fixtures (package):** `telegram.message-private-ru-pothole`; `n8n.callback-ack-before-actions`  
> **Clusters:** `telegram`, `n8n`, `channel` · **Layer:** `tests/n8n/` = **adapter-contract** (fixture + Python helpers; not live workflow e2e) · **Harness:** Fixture-driven mapping asserts (no live Telegram) · Runtime pin honesty → [`STORY-AIBRIDGE-36`](./STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md) / N8N-WF-001

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | [task-aibridge-25-t01-promote-seed-fixtures](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping/task-aibridge-25-t01-promote-seed-fixtures/README.md) | Done | Copy telegram + n8n seed JSON → `tests/fixtures/telegram/` and `tests/fixtures/n8n/`; originals stay |
| **T02** | [task-aibridge-25-t02-generate-n8n-matrix-fixtures](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping/task-aibridge-25-t02-generate-n8n-matrix-fixtures/README.md) | Done | Generate remaining N8N-002…018 (+ linked channel refs) into package `fixtures/`, copy to `tests/fixtures/` |
| **T03** | [task-aibridge-25-t03-implement-n8n-mapping-tests](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping/task-aibridge-25-t03-implement-n8n-mapping-tests/README.md) | Done | Tests in `tests/n8n/` for mapping + ack_order; no live TG |
| **T04** | [task-aibridge-25-t04-story-gate](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping/task-aibridge-25-t04-story-gate/README.md) | Done | All N8N-* covered; claim_published_forbidden on stashed; originals intact |

## Acceptance criteria

- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (if any) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] Nested tasks materialized under EPIC-04 (P1.3 APPLY).
- [x] On story Done: all required envelopes exist under `tests/fixtures/{cluster}/` as **copies**; originals remain in package [`fixtures/`](./fixtures/).
