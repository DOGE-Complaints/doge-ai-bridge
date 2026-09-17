# STORY-AIBRIDGE-33-qa-readiness-configuration — QA — Readiness and configuration

## Meta
- **Key:** `STORY-AIBRIDGE-33-qa-readiness-configuration`
- **Status:** Todo (statement only — no implementation in this wave)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §10.11 READY-* · §17 smoke examples
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Implementing tests, fixtures, or code changes in this story wave.
- Nested pipeline tasks / epic folders (name ≠ create until explicit P1).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent.

## Context

`/readyz` evaluates config/Postgres/content/tool-gen without OpenAI generation or gateway write. Missing/conflicting HTTPS intake, equal bearers, dry-run gates, migration mismatch → bounded 503 reasons.

## Use cases / matrix IDs (must transfer from guide)

| ID | Scenario | Expected |
|----|----------|----------|
| READY-001 | Complete valid configuration and migrated PostgreSQL | 200 `ready`. |
| READY-002 | Channel Bearer missing | 503 `channel_auth_missing`. |
| READY-003 | Gateway Bearer missing | 503 `gateway_bearer_missing`. |
| READY-004 | Bearers equal | 503 `channel_gateway_bearer_equal`. |
| READY-005 | Gateway URL missing/conflicting/non-HTTPS | Corresponding bounded reason. |
| READY-006 | SPA redirect base invalid | 503 `draft_redirect_base_invalid`. |
| READY-007 | OpenAI key/model missing | 503 `openai_config_missing`. |
| READY-008 | OpenAI storage requested true | Settings/readiness fails closed. |
| READY-009 | Live mode without completed schema validation flag | 503 `dry_run_required`. |
| READY-010 | Content manifest/hash/path invalid | 503 bundle reason. |
| READY-011 | Tool generation fails | 503 `tool_gen_failed:*`. |
| READY-012 | PostgreSQL unreachable | 503 `database_unreachable`. |
| READY-013 | Required migration missing/mismatch | 503 migration reason. |
| READY-014 | Non-Postgres store while memory stores forbidden | 503 `database_not_postgres`. |
| READY-015 | `/readyz` called | No OpenAI generation and no gateway write. |

## Acceptance criteria (statement)

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] No nested implementation tasks created by this wave.
- [ ] Future automation must treat guide **must** as automated asserts; **characterization** as capture-first.
