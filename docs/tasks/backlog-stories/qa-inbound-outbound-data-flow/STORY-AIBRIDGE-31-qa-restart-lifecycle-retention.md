# STORY-AIBRIDGE-31-qa-restart-lifecycle-retention — QA — Restart, lifecycle, and retention

## Meta
- **Key:** `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention`
- **Status:** Todo (statement only — no implementation in this wave)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §8 PostgreSQL persistence · §10.9 LIFE-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Implementing tests, fixtures, or code changes in this story wave.
- Nested pipeline tasks / epic folders (name ≠ create until explicit P1).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent.

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

## Acceptance criteria (statement)

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] No nested implementation tasks created by this wave.
- [ ] Future automation must treat guide **must** as automated asserts; **characterization** as capture-first.
