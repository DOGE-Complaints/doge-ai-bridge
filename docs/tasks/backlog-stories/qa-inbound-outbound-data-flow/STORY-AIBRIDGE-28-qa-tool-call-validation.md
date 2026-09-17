# STORY-AIBRIDGE-28-qa-tool-call-validation — QA — Tool-call validation

## Meta
- **Key:** `STORY-AIBRIDGE-28-qa-tool-call-validation`
- **Status:** Todo (statement only — no implementation in this wave)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §6.3 · §10.6 TOOL-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Implementing tests, fixtures, or code changes in this story wave.
- Nested pipeline tasks / epic folders (name ≠ create until explicit P1).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent.

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

## Acceptance criteria (statement)

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] No nested implementation tasks created by this wave.
- [ ] Future automation must treat guide **must** as automated asserts; **characterization** as capture-first.
