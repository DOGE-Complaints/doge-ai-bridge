# STORY-AIBRIDGE-26 — QA — Idempotency and concurrency

## Meta
- **Key:** `STORY-AIBRIDGE-26-qa-idempotency-concurrency`
- **Status:** 🟢 Implemented (P6 closed · next P7)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-26-qa-idempotency-concurrency.md`
- **decision_ref:** [`STORY-AIBRIDGE-26-qa-idempotency-concurrency.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-26-qa-idempotency-concurrency.md) · [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) §5 Session · §10.4 IDEM-* · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) ADR-Q1/Q2
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 · ADR-Q1/Q2
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000023-20260917-epic-aibridge-04-story-26-qa-idempotency-concurrency.yaml` (YAML default unchanged)
- **P1 materialize:** 2026-09-17T18:12:10Z
- **P3 closed:** 2026-09-17T18:21:34Z
- **P4 audit:** [p4-audit-STORY-AIBRIDGE-26-qa-idempotency-concurrency-20260917.md](../../../../analysis/p4-audit-STORY-AIBRIDGE-26-qa-idempotency-concurrency-20260917.md)
- **P5 APPLY:** 2026-09-17T18:28:05Z · `run_mode=aibridge_26_audit_20260917`
- **P6 closed:** 2026-09-17T18:30:28Z · G-01/G-03 CLOSED
- **Gate:** [t04](./task-aibridge-26-t04-story-gate/acceptance-verification-task-aibridge-26-t04-story-gate.md) · [t05](./task-aibridge-26-t05-audit-g01-idem008-lock-order/acceptance-verification-task-aibridge-26-t05-audit-g01-idem008-lock-order.md) · [t06](./task-aibridge-26-t06-audit-g03-spy-forbid-logs/acceptance-verification-task-aibridge-26-t06-audit-g03-spy-forbid-logs.md) PASS
- **Run summary:** [P3](../../../../run-reports/run-summary-20260917-1821-story-aibridge-26-p3.md) · [P5](../../../../run-reports/run-summary-20260917-1828-story-aibridge-26-p5-disposition.md) · [P6](../../../../run-reports/run-summary-20260917-1830-story-aibridge-26-p6.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Guide §5 / §10.4 IDEM-* | [`AIBRIDGE-QA-…-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) |
| ADR-Q1/Q2 fixtures | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| Traceability IDEM-001…010 | [`TRACEABILITY-MATRIX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md) |
| Seed originals | package [`fixtures/`](../../../../backlog-stories/qa-inbound-outbound-data-flow/fixtures/) |
| Harness | `src/aibridge/dedupe.py` · `RecordingResponsesClient` · `SessionTurnLock` |

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Deleting or moving package `fixtures/` originals (promote = **copy** only).
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

## Verified current state
- Seed + matrix copies under `tests/fixtures/{spies,channel,openai}/`; package originals intact (hash_eq).
- Suite: `tests/integration/test_idempotency_concurrency.py` (13 passed · 2026-09-17T18:21:34Z).
- Characterization IDEM-003 / IDEM-004 capture-first (no invent).
- TRACEABILITY-MATRIX IDEM-001…010 → this story key.

## Target / AC
- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (IDEM-003 log-if-implemented; IDEM-004 waiter-branch) marked — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] On story Done: required envelopes under `tests/fixtures/{cluster}/` as **copies**; originals remain in package `fixtures/`.

## Техническое решение

- **Approach (ADR-Q1/Q2):** promote=copy; integration tests in `tests/integration/`; EventDedupeStore; SessionTurnLock; barriers not sleep; RecordingResponsesClient; spy bag §14.
- **Skill:** python-pro · test-master  

## Nested tasks (pkg-000023 order + P5 audit queue)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-26-t01-promote-seed-fixtures](./task-aibridge-26-t01-promote-seed-fixtures/README.md) | Seed copy → spies (+ openai) | Done |
| t02 | [task-aibridge-26-t02-generate-idem-matrix-fixtures](./task-aibridge-26-t02-generate-idem-matrix-fixtures/README.md) | IDEM-002…010 generate + promote | Done |
| t03 | [task-aibridge-26-t03-implement-idempotency-tests](./task-aibridge-26-t03-implement-idempotency-tests/README.md) | `tests/integration/` side-effect counts + barriers | Done |
| t04 | [task-aibridge-26-t04-story-gate](./task-aibridge-26-t04-story-gate/README.md) | Gate PASS | Done |
| t05 | [task-aibridge-26-t05-audit-g01-idem008-lock-order](./task-aibridge-26-t05-audit-g01-idem008-lock-order/README.md) | G-01 IDEM-008 lock/history order | Done |
| t06 | [task-aibridge-26-t06-audit-g03-spy-forbid-logs](./task-aibridge-26-t06-audit-g03-spy-forbid-logs/README.md) | G-03 spy forbid live logs | Done |

### P5 disposition (2026-09-17T18:28:05Z) → P6 CLOSED (2026-09-17T18:30:28Z)

| Gap | Sev | Disposition | Task |
|-----|-----|-------------|------|
| G-01 | Medium | TASKED → CLOSED | t05 |
| G-02 | Info | WAIVED reason=info-nonblocking | — |
| G-03 | Low | TASKED → CLOSED | t06 |
| G-04 | Info | WAIVED reason=info-nonblocking | — |
| G-05 | Info | WAIVED reason=info-nonblocking | — |
