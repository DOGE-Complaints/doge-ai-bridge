# STORY-AIBRIDGE-27 — QA — OpenAI and prompt behavior

## Meta
- **Key:** `STORY-AIBRIDGE-27-qa-openai-prompt-behavior`
- **Status:** 🟢 Implemented (P6 closed · next P7)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md`
- **decision_ref:** [`STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md) · [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) §6 OpenAI Responses · §10.5 OAI-* · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) ADR-Q1/Q2
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 · ADR-Q1/Q2
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000024-20260917-epic-aibridge-04-story-27-qa-openai-prompt-behavior.yaml` (YAML default unchanged)
- **P1 materialize:** 2026-09-17T18:39:38Z
- **P3 closed:** 2026-09-17T18:46:05Z
- **P4 audit:** [p4-audit-STORY-AIBRIDGE-27-qa-openai-prompt-behavior-20260917.md](../../../../analysis/p4-audit-STORY-AIBRIDGE-27-qa-openai-prompt-behavior-20260917.md)
- **P5 APPLY:** 2026-09-17T18:52:17Z · `run_mode=aibridge_27_audit_20260917`
- **P6 closed:** 2026-09-17T18:54:18Z · G-01/G-02 CLOSED
- **Gate:** [t04](./task-aibridge-27-t04-story-gate/acceptance-verification-task-aibridge-27-t04-story-gate.md) · [t05](./task-aibridge-27-t05-audit-g01-oai009-channel-depth/acceptance-verification-task-aibridge-27-t05-audit-g01-oai009-channel-depth.md) · [t06](./task-aibridge-27-t06-audit-g02-oai001-action-labels/acceptance-verification-task-aibridge-27-t06-audit-g02-oai001-action-labels.md) PASS
- **Run summary:** [P3](../../../../run-reports/run-summary-20260917-1846-story-aibridge-27-p3.md) · [P5](../../../../run-reports/run-summary-20260917-1852-story-aibridge-27-p5-disposition.md) · [P6](../../../../run-reports/run-summary-20260917-1854-story-aibridge-27-p6.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Guide §6 / §10.5 OAI-* | [`AIBRIDGE-QA-…-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) |
| ADR-Q1/Q2 fixtures | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| Traceability OAI-001…016 | [`TRACEABILITY-MATRIX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md) |
| Seed originals | package [`fixtures/`](../../../../backlog-stories/qa-inbound-outbound-data-flow/fixtures/) |
| Harness | `RecordingResponsesClient` · `InterviewEngine` · readiness store:false |

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Deleting or moving package `fixtures/` originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

## Context

Responses calls use store:false, explicit history, XOR stable-prefix vs instructions=, parallel_tool_calls false. Budgets and errors must not authorize gateway. Secrets must not appear in model I/O or logs.

## Use cases / matrix IDs (must transfer from guide)

| ID | Scenario | Expected |
|----|----------|----------|
| OAI-001 | Ordinary text response | 200, visible reply, interpretation buttons on first interviewing response. |
| OAI-002 | Empty output array | Bounded fallback text; no crash. |
| OAI-003 | Output containing `Received:` stub | Stub not echoed; mapped to `Acknowledged.`. |
| OAI-004 | Valid cached token usage | Cache metric records value. |
| OAI-005 | `store` attempted true by config | Startup/settings or readiness fails closed. |
| OAI-006 | Both stable prefix and `instructions` used | Fail test; mutually exclusive. |
| OAI-007 | Parallel tool calls requested | Fail test; must be false. |
| OAI-008 | OpenAI 429 | Bounded internal channel error under current implementation; no secret/raw response; no gateway. |
| OAI-009 | OpenAI 5xx | Same bounded failure; retry policy belongs outside unsafe consequential send path. |
| OAI-010 | OpenAI timeout | Bounded 500 `internal_error`, `retryable=true`; dedupe claim aborted so message retry can run. |
| OAI-011 | Invalid OpenAI JSON/body | Bounded error, no history corruption or gateway. |
| OAI-012 | Input/output/call/turn budget breach | No gateway; last confirmed state preserved; resident-safe rejection. |
| OAI-013 | Malicious prompt asks to reveal instructions/tokens | No secret or system prompt disclosure in output/logs. |
| OAI-014 | User text contains JSON/tool-looking syntax | Treated as user content, not trusted function call. |
| OAI-015 | Stable prefix across two sessions | Identical prefix bytes/hash for same bundle/model/tool/pack. |
| OAI-016 | Content bundle changes | New deployment/session uses new pinned bundle; active pinned session behavior follows bundle retention policy. |

## Verified current state
- Seed + matrix copies under `tests/fixtures/{openai,channel}/`; package originals intact (hash_eq).
- Suite: `tests/integration/test_openai_prompt_behavior.py` (18 passed · 2026-09-17T18:46:05Z).
- Characterization OAI-008 / OAI-009 / OAI-016 capture-first (no invent).
- TRACEABILITY-MATRIX OAI-001…016 → this story key.

## Target / AC
- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (OAI-008/009/016 hedges) marked — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] On story Done: required envelopes under `tests/fixtures/{cluster}/` as **copies**; originals remain in package `fixtures/`.

## Техническое решение

- **Approach (ADR-Q1/Q2):** promote=copy; integration tests in `tests/integration/`; RecordingResponsesClient scripted bodies / http_error stubs; no live Telegram.
- **Skill:** python-pro · test-master  

## Nested tasks (pkg-000024 order + P5 audit queue)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-27-t01-promote-seed-fixtures](./task-aibridge-27-t01-promote-seed-fixtures/README.md) | Seed copy → openai | Done |
| t02 | [task-aibridge-27-t02-generate-oai-matrix-fixtures](./task-aibridge-27-t02-generate-oai-matrix-fixtures/README.md) | OAI-002…016 generate + promote | Done |
| t03 | [task-aibridge-27-t03-implement-openai-behavior-tests](./task-aibridge-27-t03-implement-openai-behavior-tests/README.md) | Integration OAI suite | Done |
| t04 | [task-aibridge-27-t04-story-gate](./task-aibridge-27-t04-story-gate/README.md) | Gate all OAI-* | Done |
| t05 | [task-aibridge-27-t05-audit-g01-oai009-channel-depth](./task-aibridge-27-t05-audit-g01-oai009-channel-depth/README.md) | G-01 OAI-009 channel depth | Done |
| t06 | [task-aibridge-27-t06-audit-g02-oai001-action-labels](./task-aibridge-27-t06-audit-g02-oai001-action-labels/README.md) | G-02 OAI-001 action labels | Done |

### P5 disposition (2026-09-17T18:52:17Z) → P6 CLOSED (2026-09-17T18:54:18Z)

| Gap | Sev | Disposition | Task |
|-----|-----|-------------|------|
| G-01 | Medium | TASKED → CLOSED | t05 |
| G-02 | Low | TASKED → CLOSED | t06 |
| G-03 | Info | WAIVED reason=info-nonblocking | — |
| G-04 | Info | WAIVED reason=info-nonblocking | — |
| G-05 | Info | WAIVED reason=info-nonblocking | — |
