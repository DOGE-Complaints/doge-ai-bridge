# STORY-AIBRIDGE-24-qa-json-schema-boundary — QA — JSON and schema boundary

## Meta
- **Key:** `STORY-AIBRIDGE-24-qa-json-schema-boundary`
- **Status:** Todo (statement only — no implementation in this wave)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §4 Exact channel API contracts · §10.2 VAL-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Implementing tests, fixtures, or code changes in this story wave.
- Nested pipeline tasks / epic folders (name ≠ create until explicit P1).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent.

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

## Acceptance criteria (statement)

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] No nested implementation tasks created by this wave.
- [ ] Future automation must treat guide **must** as automated asserts; **characterization** as capture-first.
