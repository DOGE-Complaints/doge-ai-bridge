# STORY-AIBRIDGE-23-qa-auth-ops-boundaries — QA — Authentication and operational boundaries

## Meta
- **Key:** `STORY-AIBRIDGE-23-qa-auth-ops-boundaries`
- **Status:** Todo (statement only — no implementation in this wave)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §2.1 Trust boundaries · §4.1 Authentication · §10.1 AUTH-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Implementing tests, fixtures, or code changes in this story wave.
- Nested pipeline tasks / epic folders (name ≠ create until explicit P1).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent.

## Context

Channel Bearer is the only trust for n8n→aibridge. Gateway Bearer must never equal Channel Bearer and must never be sent to n8n. `/healthz`/`readyz`/`metrics` are operational; `/metrics` has no Channel Bearer middleware and must stay private-network-only.

## Use cases / matrix IDs (must transfer from guide)

| ID | Scenario | Expected |
|----|----------|----------|
| AUTH-001 | Valid current Channel Bearer on `/turns` | Request reaches validation/processing. |
| AUTH-002 | Valid previous Channel Bearer during rotation | Accepted. |
| AUTH-003 | Missing Authorization | 401 `unauthorized`, redacted body. |
| AUTH-004 | Wrong scheme, e.g. `Basic` | 401. |
| AUTH-005 | `Bearer` without value | 401. |
| AUTH-006 | Wrong token of same length | 401. |
| AUTH-007 | Wrong token of different length | 401 without timing-dependent functional difference. |
| AUTH-008 | Gateway Bearer supplied to channel endpoint | 401 unless misconfigured equal; readiness must reject equality. |
| AUTH-009 | Channel Bearer appears in logs/metrics/error | Fail test; secret must be absent. |
| AUTH-010 | `/healthz` without Bearer | 200 `{"status":"ok"}`. |
| AUTH-011 | `/readyz` without Bearer | 200 ready or 503 bounded reason; no generation/write. |
| AUTH-012 | `/metrics` from allowed private test network | Prometheus text; no PII/secrets. |

## Acceptance criteria (statement)

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] No nested implementation tasks created by this wave.
- [ ] Future automation must treat guide **must** as automated asserts; **characterization** as capture-first.
