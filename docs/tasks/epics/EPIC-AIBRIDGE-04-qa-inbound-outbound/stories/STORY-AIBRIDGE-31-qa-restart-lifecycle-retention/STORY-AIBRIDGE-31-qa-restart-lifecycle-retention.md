# STORY-AIBRIDGE-31 — QA — Restart, lifecycle, and retention

## Meta
- **Key:** `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention`
- **Status:** 🟢 Implemented (P6 closed · next P7)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md`
- **decision_ref:** [`STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md) · [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) §8 · §10.9 LIFE-* · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) ADR-Q1/Q2
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 · ADR-Q1/Q2
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000028-20260917-epic-aibridge-04-story-31-qa-restart-lifecycle-retention.yaml` (**immutable** under `run_mode=aibridge_31_audit_20260917`)
- **P1 materialize:** 2026-09-17T20:05:23Z
- **P3 closed:** 2026-09-17T20:12:21Z
- **P4 audited:** 2026-09-17T20:15:03Z
- **P5 disposition:** 2026-09-17T20:17:44Z · G-01/G-02 TASKED · G-03…G-05 WAIVED
- **P6 closed:** 2026-09-17T20:19:43Z · G-01/G-02 CLOSED
- **Gate:** [t04](./task-aibridge-31-t04-story-gate/README.md) · [acceptance PASS](./task-aibridge-31-t04-story-gate/acceptance-verification-task-aibridge-31-t04-story-gate.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Guide §8 / §10.9 LIFE-* | [`AIBRIDGE-QA-…-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) |
| ADR-Q1/Q2 fixtures | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| Traceability LIFE-001…012 | [`TRACEABILITY-MATRIX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md) |
| Seed originals | none yet — generate on P3 t01 into package [`fixtures/`](../../../../backlog-stories/qa-inbound-outbound-data-flow/fixtures/) |
| Harness | disposable PG · `rebuild_app_same_pg` · fake clock for TTL |

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Deleting or moving package `fixtures/` originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

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

## Verified current state
- LIFE-* envelopes in package `fixtures/` — **present** (13 envelopes; promote=copy).
- TRACEABILITY-MATRIX LIFE-001…012 → this story key (`covered`).
- Layer `tests/integration/test_lifecycle_retention.py` — **PASS** (13 tests; LIFE-001…012).
- Preference A: MemConfirmSessions + fake GatewayAttemptStore + SessionActivityClock (disposable PG absent).

## Target / AC
- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (LIFE-009/010) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] On story Done: required envelopes under `tests/fixtures/{cluster}/` as **copies**; originals remain in package `fixtures/`.

## Техническое решение

- **Approach (ADR-Q1/Q2):** generate LIFE-* into package `fixtures/` (`schema_version=1.0`), promote=copy → `tests/fixtures/{settings,channel,spies}/`; tests in `tests/integration/`; disposable PG + `rebuild_app_same_pg`; fake clock for TTL; LIFE-009/010 capture-first; no live Telegram.
- **Skill:** python-pro · test-master

## Nested tasks (pkg-000028 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-31-t01-generate-life-fixtures](./task-aibridge-31-t01-generate-life-fixtures/README.md) | Generate LIFE-* envelopes | Done |
| t02 | [task-aibridge-31-t02-promote-fixtures](./task-aibridge-31-t02-promote-fixtures/README.md) | Promote copies | Done |
| t03 | [task-aibridge-31-t03-implement-lifecycle-tests](./task-aibridge-31-t03-implement-lifecycle-tests/README.md) | Lifecycle suite | Done |
| t04 | [task-aibridge-31-t04-story-gate](./task-aibridge-31-t04-story-gate/README.md) | Gate all LIFE-* | Done |
| t05 | [task-aibridge-31-t05-audit-g01-life-pg-rebuild](./task-aibridge-31-t05-audit-g01-life-pg-rebuild/README.md) | G-01 PG/`rebuild_app_same_pg` | Done |
| t06 | [task-aibridge-31-t06-audit-g02-life002-spy-history](./task-aibridge-31-t06-audit-g02-life002-spy-history/README.md) | G-02 spy+history | Done |
