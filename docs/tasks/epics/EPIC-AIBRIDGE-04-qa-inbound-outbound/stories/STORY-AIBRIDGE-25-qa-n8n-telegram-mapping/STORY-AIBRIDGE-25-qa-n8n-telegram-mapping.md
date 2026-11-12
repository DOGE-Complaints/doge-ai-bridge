# STORY-AIBRIDGE-25 — QA — n8n and Telegram mapping

## Meta
- **Key:** `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping`
- **Status:** 🟢 Implemented (P6 closed · next P7)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md`
- **decision_ref:** [`STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md) · [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) §3 · §10.3 N8N-* · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) ADR-Q1/Q2
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 · ADR-Q1/Q2
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000022-20260917-epic-aibridge-04-story-25-qa-n8n-telegram-mapping.yaml` (YAML default unchanged)
- **P1 materialize:** 2026-09-17T17:39:14Z
- **P3 closed:** 2026-09-17T17:44:23Z
- **P4 audit:** [p4-audit-STORY-AIBRIDGE-25-qa-n8n-telegram-mapping-20260917.md](../../../../analysis/p4-audit-STORY-AIBRIDGE-25-qa-n8n-telegram-mapping-20260917.md)
- **P5 APPLY:** 2026-09-17T17:50:16Z · `run_mode=aibridge_25_audit_20260917`
- **P6 closed:** 2026-09-17T17:53:25Z · G-01/G-02 CLOSED
- **Gate:** [t04](./task-aibridge-25-t04-story-gate/acceptance-verification-task-aibridge-25-t04-story-gate.md) · [t05](./task-aibridge-25-t05-audit-g01-n8n014-post-ack-fail/acceptance-verification-task-aibridge-25-t05-audit-g01-n8n014-post-ack-fail.md) · [t06](./task-aibridge-25-t06-audit-g02-one-reply-assert/acceptance-verification-task-aibridge-25-t06-audit-g02-one-reply-assert.md) PASS
- **Run summary:** [P3](../../../../run-reports/run-summary-20260917-1744-story-aibridge-25-p3.md) · [P5](../../../../run-reports/run-summary-20260917-1750-story-aibridge-25-p5-disposition.md) · [P6](../../../../run-reports/run-summary-20260917-1752-story-aibridge-25-p6.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Guide §3 / §10.3 N8N-* | [`AIBRIDGE-QA-…-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) |
| ADR-Q1/Q2 fixtures | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| Traceability N8N-001…018 | [`TRACEABILITY-MATRIX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md) |
| Seed originals | package [`fixtures/`](../../../../backlog-stories/qa-inbound-outbound-data-flow/fixtures/) |
| Ops mapping | `docs/ops/n8n-channel-workflow/README.md` §2–§3 |

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Deleting or moving package `fixtures/` originals (promote = **copy** only).
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

## Verified current state
- Seed copies hash_eq: `tests/fixtures/telegram/message-private-ru-pothole.json` · `tests/fixtures/n8n/callback-ack-before-actions.json`.
- Matrix envelopes in package `fixtures/` + copies under `tests/fixtures/{telegram,n8n,channel}/`.
- Suite: `tests/n8n/test_n8n_telegram_mapping.py` (19 passed · 2026-09-17T17:44:23Z).
- Characterization N8N-009 / N8N-011 capture-first (no invent).
- TRACEABILITY-MATRIX N8N-001…018 → this story key.

## Target / AC
- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (N8N-011; N8N-009) marked — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] On story Done: required envelopes under `tests/fixtures/{cluster}/` as **copies**; originals remain in package `fixtures/`.

## Техническое решение

- **Approach (ADR-Q1/Q2/Q5):** promote=copy; fixture-driven mapping asserts in `tests/n8n/`; no live Telegram.
- **Skill:** python-pro · test-master  

## Nested tasks (pkg-000022 order + P5 audit queue)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-25-t01-promote-seed-fixtures](./task-aibridge-25-t01-promote-seed-fixtures/README.md) | Seed copy → telegram + n8n | Done |
| t02 | [task-aibridge-25-t02-generate-n8n-matrix-fixtures](./task-aibridge-25-t02-generate-n8n-matrix-fixtures/README.md) | N8N-002…018 generate + promote | Done |
| t03 | [task-aibridge-25-t03-implement-n8n-mapping-tests](./task-aibridge-25-t03-implement-n8n-mapping-tests/README.md) | `tests/n8n/` mapping + ack_order | Done |
| t04 | [task-aibridge-25-t04-story-gate](./task-aibridge-25-t04-story-gate/README.md) | Gate PASS | Done |
| t05 | [task-aibridge-25-t05-audit-g01-n8n014-post-ack-fail](./task-aibridge-25-t05-audit-g01-n8n014-post-ack-fail/README.md) | G-01 N8N-014 post-ack timeline | Done |
| t06 | [task-aibridge-25-t06-audit-g02-one-reply-assert](./task-aibridge-25-t06-audit-g02-one-reply-assert/README.md) | G-02 N8N-001 one_reply | Done |

### P5 disposition (2026-09-17T17:50:16Z) → P6 CLOSED (2026-09-17T17:53:25Z)

| Gap | Sev | Disposition | Task |
|-----|-----|-------------|------|
| G-01 | Medium | TASKED → CLOSED | t05 |
| G-02 | Low | TASKED → CLOSED | t06 |
| G-03 | Info | WAIVED reason=info-nonblocking | — |
| G-04 | Info | WAIVED reason=info-nonblocking | — |
| G-05 | Info | WAIVED reason=info-nonblocking | — |
