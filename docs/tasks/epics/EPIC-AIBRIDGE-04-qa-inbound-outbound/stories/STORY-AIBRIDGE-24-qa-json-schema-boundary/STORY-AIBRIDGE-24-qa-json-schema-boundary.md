# STORY-AIBRIDGE-24 — QA — JSON and schema boundary

## Meta
- **Key:** `STORY-AIBRIDGE-24-qa-json-schema-boundary`
- **Status:** 🟢 Implemented (P6 closed · next P7)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-24-qa-json-schema-boundary.md`
- **decision_ref:** [`STORY-AIBRIDGE-24-qa-json-schema-boundary.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-24-qa-json-schema-boundary.md) · [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) §4 · §10.2 VAL-* · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) ADR-Q1/Q2
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 · ADR-Q1/Q2
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000021-20260917-epic-aibridge-04-story-24-qa-json-schema-boundary.yaml` (YAML default unchanged)
- **P1 materialize:** 2026-09-17T14:26:09Z
- **P3 closed:** 2026-09-17T14:32:38Z
- **P4 audit:** [p4-audit-STORY-AIBRIDGE-24-qa-json-schema-boundary-20260917.md](../../../../analysis/p4-audit-STORY-AIBRIDGE-24-qa-json-schema-boundary-20260917.md)
- **P5 APPLY:** 2026-09-17T14:40:05Z · `run_mode=aibridge_24_audit_20260917`
- **P6 closed:** 2026-09-17T14:44:12Z · G-01/G-02 CLOSED
- **Gate:** [t04](./acceptance-verification-task-aibridge-24-t04-story-gate.md) · [t05](./task-aibridge-24-t05-audit-g01-negative-content-length/acceptance-verification-task-aibridge-24-t05-audit-g01-negative-content-length.md) · [t06](./task-aibridge-24-t06-audit-g02-val016-db-side-effect/acceptance-verification-task-aibridge-24-t06-audit-g02-val016-db-side-effect.md) PASS
- **Run summary:** [P3](../../../../run-reports/run-summary-20260917-1432-story-aibridge-24-p3.md) · [P5](../../../../run-reports/run-summary-20260917-1440-story-aibridge-24-p5-disposition.md) · [P6](../../../../run-reports/run-summary-20260917-1444-story-aibridge-24-p6.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Guide §4 / §10.2 VAL-* | [`AIBRIDGE-QA-…-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) |
| ADR-Q1/Q2 fixtures | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| Traceability VAL-001…018 | [`TRACEABILITY-MATRIX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md) |
| Seed originals | package [`fixtures/`](../../../../backlog-stories/qa-inbound-outbound-data-flow/fixtures/) |
| Channel OAS | `docs/openapi/aibridge-channel-v1.openapi.yaml` |

## Scope
Automated **test/QA acceptance statements** covering VAL-001…018. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Deleting or moving package `fixtures/` originals (promote = **copy** only).
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

## Verified current state
- Seed copy hash_eq: `tests/fixtures/channel/turns-valid-private.json`.
- 17 `val-*.json` envelopes in package `fixtures/` + hash_eq copies under `tests/fixtures/channel/`.
- Contract: `tests/contract/test_json_schema_boundary.py` (21 passed · 2026-09-17T14:44:12Z).
- Characterization VAL-014 / VAL-018 capture current **200** (no trim / Content-Type invent).
- P6: VAL-017 negative CL → 400; VAL-016 asserts `side_effect_count==0`.
- TRACEABILITY-MATRIX VAL-001…018 → this story key.

## Target / AC
- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (VAL-014, VAL-018) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] On story Done: all required envelopes exist under `tests/fixtures/{cluster}/` as **copies**; originals remain in package `fixtures/`.

## Техническое решение

- **Approach (ADR-Q1/Q2):** promote=copy; generate VAL envelopes; contract TestClient suite; characterization capture-first.
- **Skill:** python-pro · test-master  

## Nested tasks (pkg-000021 order + P5 audit queue)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-24-t01-promote-seed-fixtures](./task-aibridge-24-t01-promote-seed-fixtures/README.md) | Seed copy → `tests/fixtures/channel/` | Done |
| t02 | [task-aibridge-24-t02-generate-val-matrix-fixtures](./task-aibridge-24-t02-generate-val-matrix-fixtures/README.md) | VAL-002…018 generate + promote copies | Done |
| t03 | [task-aibridge-24-t03-implement-schema-boundary-tests](./task-aibridge-24-t03-implement-schema-boundary-tests/README.md) | `tests/contract/` VAL-* | Done |
| t04 | [task-aibridge-24-t04-story-gate](./task-aibridge-24-t04-story-gate/README.md) | All VAL-* + originals intact | Done |
| t05 | [task-aibridge-24-t05-audit-g01-negative-content-length](./task-aibridge-24-t05-audit-g01-negative-content-length/README.md) | G-01 VAL-017 negative CL → 400 | Done |
| t06 | [task-aibridge-24-t06-audit-g02-val016-db-side-effect](./task-aibridge-24-t06-audit-g02-val016-db-side-effect/README.md) | G-02 VAL-016 DB side_effect | Done |

### P5 disposition (2026-09-17T14:40:05Z) → P6 CLOSED (2026-09-17T14:44:12Z)

| Gap | Sev | Disposition | Task |
|-----|-----|-------------|------|
| G-01 | Medium | TASKED → CLOSED | t05 |
| G-02 | Low | TASKED → CLOSED | t06 |
| G-03 | Info | WAIVED reason=info-nonblocking | — |
| G-04 | Info | WAIVED reason=info-nonblocking | — |
| G-05 | Info | WAIVED reason=info-nonblocking | — |
