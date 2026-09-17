# STORY-AIBRIDGE-29-qa-action-token-fsm — QA — Action token and dual-confirm FSM

## Meta
- **Key:** `STORY-AIBRIDGE-29-qa-action-token-fsm`
- **Status:** Todo (statement only — no implementation in this wave)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §5.2–5.4 · §10.7 ACT-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Implementing tests, fixtures, or code changes in this story wave.
- Nested pipeline tasks / epic folders (name ≠ create until explicit P1).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent.

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

## Acceptance criteria (statement)

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] No nested implementation tasks created by this wave.
- [ ] Future automation must treat guide **must** as automated asserts; **characterization** as capture-first.
