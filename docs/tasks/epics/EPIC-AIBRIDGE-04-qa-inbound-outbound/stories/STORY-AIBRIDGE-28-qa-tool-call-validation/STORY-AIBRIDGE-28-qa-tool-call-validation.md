# STORY-AIBRIDGE-28 — QA — Tool-call validation

## Meta
- **Key:** `STORY-AIBRIDGE-28-qa-tool-call-validation`
- **Status:** 🟢 Implemented (P3 · next P4)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-28-qa-tool-call-validation.md`
- **decision_ref:** [`STORY-AIBRIDGE-28-qa-tool-call-validation.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-28-qa-tool-call-validation.md) · [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) §6.3 · §10.6 TOOL-* · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) ADR-Q1/Q2
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 · ADR-Q1/Q2
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000025-20260917-epic-aibridge-04-story-28-qa-tool-call-validation.yaml`
- **P1 materialize:** 2026-09-17T19:00:38Z
- **P3 closed:** 2026-09-17T19:07:11Z
- **P5 APPLY:** 2026-09-17T19:13:12Z · `run_mode=aibridge_28_audit_20260917`
- **P6 closed:** 2026-09-17T19:15:26Z · G-01/G-02 CLOSED
- **Gate:** [t04](./task-aibridge-28-t04-story-gate/acceptance-verification-task-aibridge-28-t04-story-gate.md) · [t05](./task-aibridge-28-t05-audit-g01-tool013-persist-rollback/acceptance-verification-task-aibridge-28-t05-audit-g01-tool013-persist-rollback.md) · [t06](./task-aibridge-28-t06-audit-g02-tool007-scalar-args/acceptance-verification-task-aibridge-28-t06-audit-g02-tool007-scalar-args.md) PASS
- **Run summary:** [P3](../../../../run-reports/run-summary-20260917-1907-story-aibridge-28-p3.md) · [P5](../../../../run-reports/run-summary-20260917-1913-story-aibridge-28-p5-disposition.md) · [P6](../../../../run-reports/run-summary-20260917-1915-story-aibridge-28-p6.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Guide §6.3 / §10.6 TOOL-* | [`AIBRIDGE-QA-…-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) |
| ADR-Q1/Q2 fixtures | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| Traceability TOOL-001…014 | [`TRACEABILITY-MATRIX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md) |
| Seed originals | package [`fixtures/`](../../../../backlog-stories/qa-inbound-outbound-data-flow/fixtures/) |
| Harness | `validate_function_calls` · `ValidationContext` · gateway OAS pin |

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Deleting or moving package `fixtures/` originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

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

## Verified current state
- TOOL-* package envelopes + copies under `tests/fixtures/{openai,gateway}/` (hash_eq).
- Suite: `tests/unit/test_tool_call_validation.py` (17 passed · 2026-09-17T19:07:11Z).
- Characterization TOOL-014 remint → IllegalTransition capture-first (no invent).
- TRACEABILITY-MATRIX TOOL-001…014 → this story key.

## Target / AC
- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (TOOL-014) marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] On story Done: required envelopes under `tests/fixtures/{cluster}/` as **copies**; originals remain in package `fixtures/`.

## Техническое решение

- **Approach (ADR-Q1/Q2):** generate TOOL-* into package `fixtures/` (`uus_veerenni_civic` v3), promote=copy → `tests/fixtures/{openai,gateway}/`; unit tests in `tests/unit/`; ValidationContext + RecordingGatewayTransport pin; no live Telegram.
- **Skill:** python-pro · test-master

## Nested tasks (pkg-000025 order + P5 audit queue)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-28-t01-generate-tool-seed-fixtures](./task-aibridge-28-t01-generate-tool-seed-fixtures/README.md) | Generate TOOL-* openai/gateway envelopes | Done |
| t02 | [task-aibridge-28-t02-promote-fixtures](./task-aibridge-28-t02-promote-fixtures/README.md) | Copy → tests/fixtures/{openai,gateway}/ | Done |
| t03 | [task-aibridge-28-t03-implement-tool-gate-tests](./task-aibridge-28-t03-implement-tool-gate-tests/README.md) | Unit TOOL suite | Done |
| t04 | [task-aibridge-28-t04-story-gate](./task-aibridge-28-t04-story-gate/README.md) | Gate all TOOL-* | Done |
| t05 | [task-aibridge-28-t05-audit-g01-tool013-persist-rollback](./task-aibridge-28-t05-audit-g01-tool013-persist-rollback/README.md) | G-01 TOOL-013 persist rollback | Done |
| t06 | [task-aibridge-28-t06-audit-g02-tool007-scalar-args](./task-aibridge-28-t06-audit-g02-tool007-scalar-args/README.md) | G-02 TOOL-007 scalar | Done |

### P5 disposition (2026-09-17T19:13:12Z) → P6 CLOSED (2026-09-17T19:15:26Z)

| Gap | Sev | Disposition | Task |
|-----|-----|-------------|------|
| G-01 | Medium | TASKED → CLOSED | t05 |
| G-02 | Low | TASKED → CLOSED | t06 |
| G-03 | Info | WAIVED reason=info-nonblocking | — |
| G-04 | Info | WAIVED reason=info-nonblocking | — |
| G-05 | Info | WAIVED reason=info-nonblocking | — |
