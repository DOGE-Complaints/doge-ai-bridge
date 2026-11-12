# STORY-AIBRIDGE-23-qa-auth-ops-boundaries — QA — Authentication and operational boundaries

## Meta
- **Key:** `STORY-AIBRIDGE-23-qa-auth-ops-boundaries`
- **Status:** 🟢 Implemented (P6 closed · next P7)
- **Pipeline:** [`STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md`](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-23-qa-auth-ops-boundaries/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md)
- **Active pkg:** `pkg-000020-20260917-epic-aibridge-04-story-23-qa-auth-ops-boundaries.yaml`
- **P1 materialize:** 2026-09-17T13:59:06Z
- **P3 closed:** 2026-09-17T14:02:23Z
- **Gate:** [acceptance-verification … t04](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-23-qa-auth-ops-boundaries/acceptance-verification-task-aibridge-23-t04-story-gate.md) PASS
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** to `tests/fixtures/{cluster}/`
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §2.1 Trust boundaries · §4.1 Authentication · §10.1 AUTH-*
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Materializing `task-*` / epic folders before explicit P1 (this story only **names** tasks).
- Deleting or moving package [`fixtures/`](./fixtures/) originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

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

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- **Originals (SSOT for generated envelopes):** [`fixtures/`](./fixtures/) — do **not** delete/move after promote.
- **Runtime test tree (after story execution):** `tests/fixtures/{cluster}/{name}.json` — **copy** from package `fixtures/` (or generate into package `fixtures/` first, then copy).
- Envelope: `schema_version=1.0` fields per [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §6.2.
- `task-*` folders below are **named only** — not materialized until explicit P1 (analysis.mdc: name ≠ create).

## Nested tasks (materialized — pkg-000020)

> Pipeline: [`STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md`](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-23-qa-auth-ops-boundaries/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md)  
> Arch: [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 layers.  
> **Clusters:** `channel`, `settings`, `spies` · **Layer:** `tests/contract/` · promote = **copy** only (P3)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-23-t01-promote-seed-fixtures` | Done | Copy seed `turns-valid-private.json` → `tests/fixtures/channel/`; keep original in package `fixtures/` |
| **T02** | `task-aibridge-23-t02-generate-auth-matrix-fixtures` | Done | Generate remaining AUTH-002…012 envelopes into package `fixtures/`, then copy to `tests/fixtures/{channel,settings,spies}/` |
| **T03** | `task-aibridge-23-t03-implement-contract-auth-tests` | Done | Contract tests in `tests/contract/` for AUTH-* using load_fixture + TestClient |
| **T04** | `task-aibridge-23-t04-story-gate` | Done | All AUTH-* covered; no Bearer in logs/assertions; originals intact |

## Acceptance criteria

- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (if any) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] Nested tasks named in this story; `task-*` folders materialized under EPIC-04 (P1.3).
- [x] On story Done: all required envelopes exist under `tests/fixtures/{cluster}/` as **copies**; originals remain in package [`fixtures/`](./fixtures/).
