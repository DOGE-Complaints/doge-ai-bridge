# STORY-AIBRIDGE-38 — QA — OAI 429/5xx channel outcome

## Meta
- **Key:** `STORY-AIBRIDGE-38-qa-oai-channel-error-outcome`
- **Status:** ✅ Done (P3) · P6 audit gaps CLOSED · next P7 · `run_mode=aibridge_38_audit_20260918` · 2026-09-18T13:56:16Z
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md`
- **decision_ref:** [`STORY-AIBRIDGE-38-….md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md) · [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE-GAPS-36-40.md) §38 · guide §10.5 OAI-* · §16 CHAR-006
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Qualification:** closes **P1-Q2** (closed)
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000037-20260918-epic-aibridge-04-story-38-qa-oai-channel-error-outcome.yaml` (immutable under `run_mode=aibridge_38_audit_20260918`)
- **P1 materialize:** 2026-09-18T13:40:25Z
- **P3 closed:** 2026-09-18T13:43:00Z · CHAR-006 Option A
- **P5 APPLY:** 2026-09-18T13:53:25Z · t05–t07 scaffold
- **P6 close:** 2026-09-18T13:56:16Z · G-01/G-02/G-03 CLOSED
- **Gate:** [t04](./task-aibridge-38-t04-story-gate/README.md) PASS · t05–t07 PASS

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Gaps §38 CHAR-006 / OAI channel | [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE-GAPS-36-40.md) §38 |
| Decision fixture | package `fixtures/openai/char-006-decision.json` |
| Suite | `tests/integration/test_openai_prompt_behavior.py` |

## Scope
Channel-path mapping of OpenAI 429 / 5xx per CHAR-006 Option A. Transport contracts remain. Characterization capture-first (as-built recorded before map).

## Вне scope
- Invent gateway publish on OAI errors; Gate-5; CHAR-008; invent OAS fields.

## Context
P1-Q2 closed: channel no longer locks 500 characterization for OpenAI 429/5xx.

## Use cases / matrix IDs

| ID | Scenario | Expected |
|----|----------|----------|
| CHAR-006 | 429/5xx channel outcome | Option A covered |
| OAI-008 | OpenAI 429 | Channel 429 `rate_limited` |
| OAI-009 | OpenAI 5xx | Channel 503 `transient_failure` |

## Target / AC
- [x] CHAR-006 owned; decision documented before invent.
- [x] Channel tests match Option A (not forever-500).
- [x] Secrets absent from error bodies/logs.
- [x] Nested tasks Done.
- [x] P1-Q2 closed.

## Nested tasks (pkg-000037 + audit override)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-38-t01-product-decision-char006](./task-aibridge-38-t01-product-decision-char006/README.md) | CHAR-006 Option A | Done |
| t02 | [task-aibridge-38-t02-split-transport-vs-channel-tests](./task-aibridge-38-t02-split-transport-vs-channel-tests/README.md) | transport/channel split | Done |
| t03 | [task-aibridge-38-t03-fixtures-oai-channel-errors](./task-aibridge-38-t03-fixtures-oai-channel-errors/README.md) | expect envelopes | Done |
| t04 | [task-aibridge-38-t04-story-gate](./task-aibridge-38-t04-story-gate/README.md) | TRACEABILITY + P1-Q2 | Done |
| t05 | [task-aibridge-38-t05-audit-g01-guide-oai-channel-honesty](./task-aibridge-38-t05-audit-g01-guide-oai-channel-honesty/README.md) | G-01 guide §10.5 honesty | Done |
| t06 | [task-aibridge-38-t06-audit-g02-middleware-vs-openai-rl-assert](./task-aibridge-38-t06-audit-g02-middleware-vs-openai-rl-assert/README.md) | G-02 middleware vs OpenAI RL | Done |
| t07 | [task-aibridge-38-t07-audit-g03-asgi-production-wire](./task-aibridge-38-t07-audit-g03-asgi-production-wire/README.md) | G-03 Production→ASGI wire | Done |
