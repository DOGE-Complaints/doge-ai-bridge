# STORY-AIBRIDGE-24-qa-json-schema-boundary — QA — JSON and schema boundary

## Meta
- **Key:** `STORY-AIBRIDGE-24-qa-json-schema-boundary`
- **Status:** 🟢 Implemented (P6 closed · next P7)
- **Pipeline:** [`STORY-AIBRIDGE-24-qa-json-schema-boundary.md`](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-24-qa-json-schema-boundary/STORY-AIBRIDGE-24-qa-json-schema-boundary.md)
- **Active pkg:** `pkg-000021-20260917-epic-aibridge-04-story-24-qa-json-schema-boundary.yaml`
- **P1 materialize:** 2026-09-17T14:26:09Z
- **P3 closed:** 2026-09-17T14:32:38Z
- **Gate:** [acceptance-verification … t04](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-24-qa-json-schema-boundary/acceptance-verification-task-aibridge-24-t04-story-gate.md) PASS
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** to `tests/fixtures/{cluster}/`
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §4 Exact channel API contracts · §10.2 VAL-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Materializing `task-*` / epic folders before explicit P1 (this story only **names** tasks).
- Deleting or moving package [`fixtures/`](./fixtures/) originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

## Context

Façade validates Telegram-mapped JSON against channel OAS. Unknown fields → 400; missing/invalid semantic fields → 422; oversized body → 413. Characterization rows in VAL must not silently invent product trim/Content-Type policy.

## Use cases / matrix IDs (must transfer from guide)

| ID | Scenario | Expected |
|----|----------|----------|
| VAL-001 | Valid `/turns` body | 200 bounded success. |
| VAL-002 | Valid `/actions` body | 200 or token-domain 403/404/409. |
| VAL-003 | Malformed JSON | 400 `bad_request`. |
| VAL-004 | Invalid UTF-8 body | 400 `bad_request`. |
| VAL-005 | Unknown top-level field | 400 `bad_request`. |
| VAL-006 | Unknown nested field | 400 `bad_request`. |
| VAL-007 | Missing required field | 422 `semantic_invalid`. |
| VAL-008 | `channel` other than `telegram` | 422. |
| VAL-009 | Empty `event_id` | 422. |
| VAL-010 | Numeric Telegram ID instead of string | 422. |
| VAL-011 | Non-decimal `user_id`, `chat_id`, or `message_id` | 422. |
| VAL-012 | Negative group `chat_id` decimal string | Accepted. |
| VAL-013 | Empty message text | 422. |
| VAL-014 | Whitespace-only message | Characterization: currently passes min-length; record result and open product decision if trimming is required. |
| VAL-015 | Action token length 65 | 422. |
| VAL-016 | Body exceeds `AIBRIDGE_MAX_REQUEST_BYTES` | 413 `payload_too_large`; no OpenAI/DB side effect beyond request handling. |
| VAL-017 | Invalid/negative Content-Length | 400 bounded error. |
| VAL-018 | Missing `Content-Type` but valid JSON | Characterization test; OAS requires JSON even if current parser accepts raw body. |

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- **Originals (SSOT for generated envelopes):** [`fixtures/`](./fixtures/) — do **not** delete/move after promote.
- **Runtime test tree (after story execution):** `tests/fixtures/{cluster}/{name}.json` — **copy** from package `fixtures/` (or generate into package `fixtures/` first, then copy).
- Envelope: `schema_version=1.0` fields per [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §6.2.
- `task-*` folders below are **named only** — not materialized until explicit P1 (analysis.mdc: name ≠ create).

## Nested tasks (materialized under EPIC-04)

> Pipeline: [`STORY-AIBRIDGE-24-qa-json-schema-boundary.md`](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-24-qa-json-schema-boundary/STORY-AIBRIDGE-24-qa-json-schema-boundary.md)  
> Arch: [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 layers.  
> **Seed fixtures (package):** `channel.turns-valid-private` (VAL-001)  
> **Clusters:** `channel` · **Layer:** `tests/unit/` + `tests/contract/` · **Harness:** TestClient; OAS `aibridge-channel-v1`

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-24-t01-promote-seed-fixtures` | Done | Copy `turns-valid-private.json` → `tests/fixtures/channel/`; original stays in package `fixtures/` |
| **T02** | `task-aibridge-24-t02-generate-val-matrix-fixtures` | Done | Generate VAL-002…018 (valid/invalid turns+actions) into package `fixtures/`, copy to `tests/fixtures/channel/` |
| **T03** | `task-aibridge-24-t03-implement-schema-boundary-tests` | Done | Unit/contract tests asserting OAS codes (400/413/422) without fantasy APIs |
| **T04** | `task-aibridge-24-t04-story-gate` | Done | All VAL-* covered; fixtures under `tests/fixtures/channel/`; originals intact |

## Acceptance criteria

- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (if any) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] Nested tasks named in this story; `task-*` folders **not** created until P1.
- [x] On story Done: all required envelopes exist under `tests/fixtures/{cluster}/` as **copies**; originals remain in package [`fixtures/`](./fixtures/).
