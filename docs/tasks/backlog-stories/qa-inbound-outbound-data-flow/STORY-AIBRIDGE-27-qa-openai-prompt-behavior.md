# STORY-AIBRIDGE-27-qa-openai-prompt-behavior — QA — OpenAI and prompt behavior

## Meta
- **Key:** `STORY-AIBRIDGE-27-qa-openai-prompt-behavior`
- **Status:** Implemented (P3 2026-09-17T18:46:05Z · OAI suite 18 passed · next P4)
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** to `tests/fixtures/{cluster}/`
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §6 OpenAI Responses data flow · §10.5 OAI-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Materializing `task-*` / epic folders before explicit P1 (this story only **names** tasks).
- Deleting or moving package [`fixtures/`](./fixtures/) originals (promote = **copy** only).
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

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- **Originals (SSOT for generated envelopes):** [`fixtures/`](./fixtures/) — do **not** delete/move after promote.
- **Runtime test tree (after story execution):** `tests/fixtures/{cluster}/{name}.json` — **copy** from package `fixtures/` (or generate into package `fixtures/` first, then copy).
- Envelope: `schema_version=1.0` fields per [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §6.2.
- `task-*` folders below are **named only** — not materialized until explicit P1 (analysis.mdc: name ≠ create).

## Nested tasks (named — not materialized)

> Arch: [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 layers.  
> **Seed fixtures (package):** `openai.text-only-ru-clarify` (OAI-001)  
> **Clusters:** `openai`, `channel` · **Layer:** `tests/integration/` (Recording client); unit where pure parse · **Harness:** RecordingResponsesClient scripted bodies / http_error stubs

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-27-t01-promote-seed-fixtures` | Done | Copy `text-only-ru-clarify.json` → `tests/fixtures/openai/`; original stays |
| **T02** | `task-aibridge-27-t02-generate-oai-matrix-fixtures` | Done | Generate OAI-002…016 into package `fixtures/`, copy to `tests/fixtures/openai/` |
| **T03** | `task-aibridge-27-t03-implement-openai-behavior-tests` | Done | Assert reply/fallback/budget/429 paths via RecordingResponsesClient |
| **T04** | `task-aibridge-27-t04-story-gate` | Done | All OAI-*; no secrets in captured payloads; originals intact |

## Acceptance criteria

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] Guide **must** → automated asserts; **characterization** → capture-first.
- [ ] Nested tasks named in this story; `task-*` folders **not** created until P1.
- [ ] On story Done: all required envelopes exist under `tests/fixtures/{cluster}/` as **copies**; originals remain in package [`fixtures/`](./fixtures/).
