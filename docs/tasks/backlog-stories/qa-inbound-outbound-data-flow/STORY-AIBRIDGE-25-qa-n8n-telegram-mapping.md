# STORY-AIBRIDGE-25-qa-n8n-telegram-mapping — QA — n8n and Telegram mapping

## Meta
- **Key:** `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping`
- **Status:** Todo (statement only — no implementation in this wave)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §3 E2E flows · §10.3 N8N-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Implementing tests, fixtures, or code changes in this story wave.
- Nested pipeline tasks / epic folders (name ≠ create until explicit P1).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent.

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

## Acceptance criteria (statement)

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] No nested implementation tasks created by this wave.
- [ ] Future automation must treat guide **must** as automated asserts; **characterization** as capture-first.
