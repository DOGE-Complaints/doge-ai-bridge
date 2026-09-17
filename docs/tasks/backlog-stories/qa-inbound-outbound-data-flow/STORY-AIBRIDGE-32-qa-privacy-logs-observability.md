# STORY-AIBRIDGE-32-qa-privacy-logs-observability — QA — Privacy, logs, and observability

## Meta
- **Key:** `STORY-AIBRIDGE-32-qa-privacy-logs-observability`
- **Status:** Todo (statement only — no implementation in this wave)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §2 trust · §10.10 SEC-* · §14 spies
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Implementing tests, fixtures, or code changes in this story wave.
- Nested pipeline tasks / epic folders (name ≠ create until explicit P1).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent.

## Context

No PII/narrative/secrets in audit/metrics. Token hashes only in DB. Channel vs Gateway Bearer separation in captures. Prompt injection must not expose system prompt or enable arbitrary tools/URLs.

## Use cases / matrix IDs (must transfer from guide)

| ID | Scenario | Expected |
|----|----------|----------|
| SEC-001 | Narrative contains email/phone/personal name | Full narrative absent from structured audit logs and metrics. |
| SEC-002 | Error raised with secret in exception text | Secret redacted from response/logs. |
| SEC-003 | Channel request audited | Log only bounded IDs/statuses/lengths; not raw Bearer or full narrative. |
| SEC-004 | `/metrics` scrape | Contains counts/latencies/cache telemetry only; no IDs, text, token, draft body, or URL secrets. |
| SEC-005 | Error envelope | Stable bounded schema and generated `request_id`. |
| SEC-006 | PostgreSQL token inspection | Only token hash stored. |
| SEC-007 | OpenAI request capture | `store=false`; no gateway/channel secrets. |
| SEC-008 | Gateway request capture | Gateway Bearer only; no Channel Bearer. |
| SEC-009 | n8n workflow export | No credentials or secrets committed. |
| SEC-010 | Prompt injection asks model to call arbitrary URL/tool | Only allowlisted generated function is available; gateway origin/path remain server-owned. |

## Acceptance criteria (statement)

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] No nested implementation tasks created by this wave.
- [ ] Future automation must treat guide **must** as automated asserts; **characterization** as capture-first.
