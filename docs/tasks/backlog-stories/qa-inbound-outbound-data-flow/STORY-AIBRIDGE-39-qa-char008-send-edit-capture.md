# STORY-AIBRIDGE-39-qa-char008-send-edit-capture — QA — CHAR-008 Send/Edit + dedupe capture

## Meta
- **Key:** `STORY-AIBRIDGE-39-qa-char008-send-edit-capture`
- **Status:** Done (P3 · pkg-000038 · next P4 · 2026-09-18T14:06:43Z) — CHAR-008 deferred (export absent)
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Tech arch gaps:** [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](./TECHNICAL-ARCHITECTURE-GAPS-36-40.md) **§39**
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** when execute creates them
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §16 CHAR-008 · n8n outbound Send/Edit
- **Qualification:** [`TEST-QUALIFICATION-20260918.md`](./TEST-QUALIFICATION-20260918.md) — closes **P1-Q3**
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-18 · from test qualification gap closure (operator package ask)

## Scope
Capture-first statements for **CHAR-008**: which Telegram API path (Send Message vs Edit Message) the n8n workflow uses per response state, and how duplicate outbound messages are prevented after n8n retry — **real capture**, not file-presence of `bound_tests` alone.

## Вне scope
- Materializing `task-*` / epic folders before explicit P1.
- Implementing capture tests or inventing Send/Edit policy without evidence.
- Gate-5 full pilot (STORY-37) — may share evidence but this story is CHAR-008 only.
- N8N-WF-001 export pin body (STORY-36) — may reuse pin as input.

## Context

P1-Q3: `test_char_capture_first_bound_refs_or_defer` requires refs/bound_tests paths (and defer_reason for CHAR-008) — does **not** execute characterization behavior. File-presence pass ≠ answered Send vs Edit / dedupe question.

## Use cases / matrix IDs

| ID | Scenario | Expected |
|----|----------|----------|
| **CHAR-008** | Does the n8n workflow use Send Message or Edit Message for each response state, and how does it prevent duplicate outbound Telegram messages after its own retry? | Captured answer recorded (fixture/notes); bound test asserts capture content (or explicit defer_reason remains visible in release DoD until capture exists) |

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- Capture envelope named under package `fixtures/` when execute creates it (e.g. `char-008-send-edit-capture.json`) — **not** created in Scaffolded wave.
- `task-*` folders named only until P1.

## Nested tasks (named — not materialized)

> Arch: [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](./TECHNICAL-ARCHITECTURE-GAPS-36-40.md) **§39**.  
> **Depends on:** STORY-36 export pin (or visible defer if pin absent) · ops README Send/Edit  
> **Clusters:** `n8n`, `meta` · **Policy:** capture-first; no silent product invent  
> `task-*` folders **named only** until P1.

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-39-t01-observe-workflow-outbound` | Done | Observe pinned export (`docs/ops/n8n-channel-workflow/exports/aibridge-telegram-channel-v1.json`) + ops README §2: map each response state → `send_message` \| `edit_message` and retry dedupe mechanism |
| **T02** | `task-aibridge-39-t02-capture-fixture` | Done | Write `fixtures/n8n/char-008-send-edit-capture.json` per gaps §39 schema (`response_states`, `retry_dedupe_policy`, `source_export_sha256`); promote copy to `tests/fixtures/n8n/` |
| **T03** | `task-aibridge-39-t03-bind-behavioral-assert` | Done | Extend CHAR-008 bind beyond file-presence: assert capture payload non-empty; keep meta path checks optional; if export absent keep **visible** `defer_reason` |
| **T04** | `task-aibridge-39-t04-story-gate` | Done | CHAR-008 TRACEABILITY open→covered or explicit defer; P1-Q3 closed |

## Acceptance criteria

- [x] CHAR-008 owned by this story key.
- [x] Capture answers Send vs Edit per response state and retry dedupe — or defer_reason remains **visible** in DoD (not silent). → **deferred** P3 (export absent)
- [x] Meta gate may keep path checks; behavioral assert required for Done.
- [x] Nested tasks named only; no `task-*` until P1. → **materialized P1.3 2026-09-18T14:03:38Z** · Done P3
- [x] P1-Q3 closed or explicit remaining defer. → **closed-with-defer**
