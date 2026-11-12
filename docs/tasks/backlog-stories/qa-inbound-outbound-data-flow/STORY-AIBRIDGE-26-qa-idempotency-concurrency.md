# STORY-AIBRIDGE-26-qa-idempotency-concurrency — QA — Idempotency and concurrency

## Meta
- **Key:** `STORY-AIBRIDGE-26-qa-idempotency-concurrency`
- **Status:** Implemented (P3 · pipeline + t01–t04 Done · gate PASS · next P4)
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** to `tests/fixtures/{cluster}/`
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §5 Session · §10.4 IDEM-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Materializing `task-*` / epic folders before explicit P1 (this story only **names** tasks).
- Deleting or moving package [`fixtures/`](./fixtures/) originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

## Context

Dedupe key is channel + event_id (Telegram update id). Retries must replay stored envelopes without duplicate OpenAI/gateway side effects. Session lock serializes same-session concurrent turns.

## Use cases / matrix IDs (must transfer from guide)

| ID | Scenario | Expected |
|----|----------|----------|
| IDEM-001 | Same `/turns` request and same event ID twice | Same stored response; one OpenAI call. |
| IDEM-002 | Retry uses new event ID | Demonstrate why this is wrong: second OpenAI call; n8n test must prevent it. |
| IDEM-003 | Same event ID but different body | First stored result wins; no second side effect; log safe collision signal if implemented. |
| IDEM-004 | Two concurrent identical turns | One claim/one OpenAI call; second waits/replays or receives bounded in-flight response. |
| IDEM-005 | OpenAI exception after dedupe claim | Claim aborted; a safe retry can process again. |
| IDEM-006 | Same callback update retried | Same stored `/actions` envelope; token not executed twice. |
| IDEM-007 | Two concurrent Send callbacks with different update IDs but same token | Exactly one consumes token/attempts gateway; other gets conflict. |
| IDEM-008 | Two different messages for same session concurrently | Serialized by session lock; history order deterministic. |
| IDEM-009 | Messages for different sessions concurrently | May proceed independently; no global serialization. |
| IDEM-010 | `/turns` and `/actions` accidentally reuse same channel/event ID | Dedupe namespace collision is safely replayed; workflow must use genuine unique Telegram update IDs. |

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- **Originals (SSOT for generated envelopes):** [`fixtures/`](./fixtures/) — do **not** delete/move after promote.
- **Runtime test tree (after story execution):** `tests/fixtures/{cluster}/{name}.json` — **copy** from package `fixtures/` (or generate into package `fixtures/` first, then copy).
- Envelope: `schema_version=1.0` fields per [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §6.2.
- `task-*` folders below are **named only** — not materialized until explicit P1 (analysis.mdc: name ≠ create).

## Nested tasks (named — not materialized)

> Arch: [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 layers.  
> **Seed fixtures (package):** `spies.idem-same-event-once-openai` (IDEM-001); reuse channel/openai seeds as needed  
> **Clusters:** `channel`, `openai`, `spies` · **Layer:** `tests/integration/` · **Harness:** EventDedupeStore / disposable PG; barriers not sleep; RecordingResponsesClient

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-26-t01-promote-seed-fixtures` | Todo | Copy spies (+ needed channel/openai) seeds → `tests/fixtures/{spies,channel,openai}/` |
| **T02** | `task-aibridge-26-t02-generate-idem-matrix-fixtures` | Todo | Generate IDEM-002…010 envelopes; copy to `tests/fixtures/` |
| **T03** | `task-aibridge-26-t03-implement-idempotency-tests` | Todo | Integration tests: side-effect counts (openai/gateway calls), barriers/events |
| **T04** | `task-aibridge-26-t04-story-gate` | Todo | All IDEM-*; spy bag §14; originals intact |

## Acceptance criteria

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] Guide **must** → automated asserts; **characterization** → capture-first.
- [ ] Nested tasks named in this story; `task-*` folders **not** created until P1.
- [ ] On story Done: all required envelopes exist under `tests/fixtures/{cluster}/` as **copies**; originals remain in package [`fixtures/`](./fixtures/).
