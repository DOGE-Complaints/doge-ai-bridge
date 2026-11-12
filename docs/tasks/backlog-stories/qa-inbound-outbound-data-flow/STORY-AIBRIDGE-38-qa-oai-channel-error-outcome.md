# STORY-AIBRIDGE-38-qa-oai-channel-error-outcome — QA — OAI 429/5xx channel outcome

## Meta
- **Key:** `STORY-AIBRIDGE-38-qa-oai-channel-error-outcome`
- **Status:** Done (P3 · pkg-000037 · next P4 · 2026-09-18T13:43:00Z)
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Tech arch gaps:** [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](./TECHNICAL-ARCHITECTURE-GAPS-36-40.md) **§38**
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** when execute creates them
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §10.5 OAI-* · §16 CHAR-006
- **Qualification:** [`TEST-QUALIFICATION-20260918.md`](./TEST-QUALIFICATION-20260918.md) — closes **P1-Q2**
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-18 · from test qualification gap closure (operator package ask)

## Scope
Product decision + test statements for **channel-path** mapping of OpenAI 429 / 5xx: stop treating `status_code == 500` + `internal_error` as permanent success under characterization. Transport-layer `RATE_LIMITED` / transient contracts may remain.

## Вне scope
- Materializing `task-*` / epic folders before explicit P1.
- Implementing runtime or pytest in this Scaffolded wave.
- Gate-5 live pilot (STORY-37).
- Inventing gateway publish on OpenAI errors.

## Context

P1-Q2: `test_oai_008_*` / `test_oai_009_*` assert transport outcomes correctly, then channel ASGI path asserts **500 / internal_error** as characterization — green locks undesired mapping. CHAR-006 asks whether 429/5xx should remain channel 500 or gain a distinct retryable channel outcome.

## Use cases / matrix IDs

| ID | Scenario | Expected |
|----|----------|----------|
| **CHAR-006** | Should OpenAI 429/5xx remain a channel 500, or later gain a distinct retryable channel outcome? | **Decision recorded** (capture or product MUST); tests split: (a) transport contract; (b) channel envelope matches decision — not forever-success on accidental 500 |
| OAI-008 | 429 bounded, no secret leak | Transport: rate_limited / bounded; channel: per CHAR-006 decision |
| OAI-009 | Upstream 5xx bounded | Transport: transient; channel: per CHAR-006 decision |

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- Decision note may live in package `fixtures/` or story AC when execute wave creates it — **not** invented in Scaffolded wave.
- `task-*` folders named only until P1.

## Nested tasks (materialized P1.3)

> Arch: [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](./TECHNICAL-ARCHITECTURE-GAPS-36-40.md) **§38**.  
> **Layer:** B_contract / integration · **Harness:** Recording OpenAI + ASGI channel · **Code anchors:** `ResponsesTransportError` / `unhandled_channel_exception`  
> Pipeline: [`…/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome/`](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome/)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-38-t01-product-decision-char006` | Done | CHAR-006 Option A decision fixture |
| **T02** | `task-aibridge-38-t02-split-transport-vs-channel-tests` | Done | transport keep / channel Option A + product handler |
| **T03** | `task-aibridge-38-t03-fixtures-oai-channel-errors` | Done | expect envelopes · promote=copy |
| **T04** | `task-aibridge-38-t04-story-gate` | Done | TRACEABILITY + P1-Q2 closed |

## Acceptance criteria

- [x] CHAR-006 owned by this story; decision documented before silent invent.
- [x] Channel tests do not permanently accept undesired 500 as success unless decision explicitly keeps it.
- [x] Secrets remain absent from error bodies/logs.
- [x] Nested tasks materialized at P1.3 (2026-09-18T13:40:25Z); Done at P3.
- [x] P1-Q2 closed.
