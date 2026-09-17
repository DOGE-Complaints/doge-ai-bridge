# STORY-AIBRIDGE-26-qa-idempotency-concurrency — QA — Idempotency and concurrency

## Meta
- **Key:** `STORY-AIBRIDGE-26-qa-idempotency-concurrency`
- **Status:** Todo (statement only — no implementation in this wave)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §5 Session · §10.4 IDEM-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Implementing tests, fixtures, or code changes in this story wave.
- Nested pipeline tasks / epic folders (name ≠ create until explicit P1).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent.

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

## Acceptance criteria (statement)

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] No nested implementation tasks created by this wave.
- [ ] Future automation must treat guide **must** as automated asserts; **characterization** as capture-first.
