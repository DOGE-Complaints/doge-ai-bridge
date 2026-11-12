# STORY-AIBRIDGE-29 — QA — Action token and dual-confirm FSM

## Meta
- **Key:** `STORY-AIBRIDGE-29-qa-action-token-fsm`
- **Status:** 🟢 Implemented (P6 closed · next P7)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-29-qa-action-token-fsm.md`
- **decision_ref:** [`STORY-AIBRIDGE-29-qa-action-token-fsm.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-29-qa-action-token-fsm.md) · [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) §5.2–5.4 · §10.7 ACT-* · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) ADR-Q1/Q2
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 · ADR-Q1/Q2
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000026-20260917-epic-aibridge-04-story-29-qa-action-token-fsm.yaml` (**immutable** under audit override)
- **P1 materialize:** 2026-09-17T19:21:48Z
- **P3 closed:** 2026-09-17T19:30:03Z
- **P5 APPLY:** 2026-09-17T19:35:13Z · `run_mode=aibridge_29_audit_20260917`
- **P6 closed:** 2026-09-17T19:38:16Z · G-01/G-02 CLOSED
- **Gate:** [t04](./task-aibridge-29-t04-story-gate/acceptance-verification-task-aibridge-29-t04-story-gate.md) · [t05](./task-aibridge-29-t05-audit-g01-act017-pg-hash-only/acceptance-verification-task-aibridge-29-t05-audit-g01-act017-pg-hash-only.md) · [t06](./task-aibridge-29-t06-audit-g02-fixture-expect-ssot/acceptance-verification-task-aibridge-29-t06-audit-g02-fixture-expect-ssot.md) PASS
- **Run summary:** [P3](../../../../run-reports/run-summary-20260917-1930-story-aibridge-29-p3.md) · [P5](../../../../run-reports/run-summary-20260917-1935-story-aibridge-29-p5-disposition.md) · [P6](../../../../run-reports/run-summary-20260917-1938-story-aibridge-29-p6.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Guide §5.2–5.4 / §10.7 ACT-* | [`AIBRIDGE-QA-…-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) |
| ADR-Q1/Q2 fixtures | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| Traceability ACT-001…018 | [`TRACEABILITY-MATRIX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md) |
| Seed originals | package [`fixtures/`](../../../../backlog-stories/qa-inbound-outbound-data-flow/fixtures/) — generate first |
| Harness | `ConfirmationGuard` · `confirm_fsm` · `create_app` · fake clock for TTL |

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Deleting or moving package `fixtures/` originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

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

## Verified current state
- ACT-* package envelopes + promoted copies under `tests/fixtures/{channel,spies}/` (hash_eq).
- TRACEABILITY-MATRIX ACT-001…018 → this story key (`covered`).
- Suites: `tests/unit/test_action_token_fsm.py` · `tests/integration/test_action_token_fsm_http.py` (26 passed).
- Product: `src/aibridge/confirm.py`, `confirm_fsm.py`; RecordingGatewayTransport; create_app — assert-only in P3.

## Target / AC
- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (if any) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] On story Done: required envelopes under `tests/fixtures/{cluster}/` as **copies**; originals remain in package `fixtures/`.

## Техническое решение

- **Approach (ADR-Q1/Q2):** generate ACT-* into package `fixtures/`, promote=copy → `tests/fixtures/{channel,spies}/`; tests in `tests/unit/` + `tests/integration/`; create_app + ConfirmationGuard; fake clock for TTL; no live Telegram.
- **Skill:** python-pro · test-master

## Nested tasks (pkg-000026 order + P5 audit queue)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-29-t01-generate-act-fixtures](./task-aibridge-29-t01-generate-act-fixtures/README.md) | Generate ACT-* channel/spies envelopes | Done |
| t02 | [task-aibridge-29-t02-promote-fixtures](./task-aibridge-29-t02-promote-fixtures/README.md) | Copy → tests/fixtures/{channel,spies}/ | Done |
| t03 | [task-aibridge-29-t03-implement-fsm-token-tests](./task-aibridge-29-t03-implement-fsm-token-tests/README.md) | FSM/token suite | Done |
| t04 | [task-aibridge-29-t04-story-gate](./task-aibridge-29-t04-story-gate/README.md) | Gate all ACT-* | Done · PASS |
| t05 | [task-aibridge-29-t05-audit-g01-act017-pg-hash-only](./task-aibridge-29-t05-audit-g01-act017-pg-hash-only/README.md) | G-01 ACT-017 PG hash-only | Done · PASS |
| t06 | [task-aibridge-29-t06-audit-g02-fixture-expect-ssot](./task-aibridge-29-t06-audit-g02-fixture-expect-ssot/README.md) | G-02 fixture expect SSOT | Done · PASS |
