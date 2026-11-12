# STORY-AIBRIDGE-33-qa-readiness-configuration — QA — Readiness and configuration

## Meta
- **Key:** `STORY-AIBRIDGE-33-qa-readiness-configuration`
- **Status:** Implemented (P5 disposition · next P6 · `run_mode=aibridge_33_audit_20260917`)
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** to `tests/fixtures/{cluster}/`
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §10.11 READY-* · §17 smoke examples
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Materializing `task-*` / epic folders before explicit P1 (this story only **names** tasks).
- Deleting or moving package [`fixtures/`](./fixtures/) originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

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

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- **Originals (SSOT for generated envelopes):** [`fixtures/`](./fixtures/) — do **not** delete/move after promote.
- **Runtime test tree (after story execution):** `tests/fixtures/{cluster}/{name}.json` — **copy** from package `fixtures/` (or generate into package `fixtures/` first, then copy).
- Envelope: `schema_version=1.0` fields per [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §6.2.
- `task-*` folders below are **named only** — not materialized until explicit P1 (analysis.mdc: name ≠ create).

## Nested tasks (named — not materialized)

> Arch: [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 layers.  
> **Seed fixtures (package):** `settings.ready-missing-channel-bearer` (READY-002)  
> **Clusters:** `settings` · **Layer:** `tests/contract/` / readiness unit; optional container smoke · **Harness:** Settings overrides; `/readyz` reason codes from readiness.py

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-33-t01-promote-seed-fixtures` | Done | Copy `ready-missing-channel-bearer.json` → `tests/fixtures/settings/`; original stays |
| **T02** | `task-aibridge-33-t02-generate-ready-matrix-fixtures` | Done | Generate READY-001…015 into package `fixtures/`, copy to `tests/fixtures/settings/` |
| **T03** | `task-aibridge-33-t03-implement-readyz-tests` | Done | Assert bounded reasons; no OpenAI/gateway side effects on /readyz |
| **T04** | `task-aibridge-33-t04-story-gate` | Done | All READY-*; originals intact |

## Acceptance criteria

- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (if any) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] Nested tasks named in this story; `task-*` folders **not** created until P1.
- [x] On story Done: all required envelopes exist under `tests/fixtures/{cluster}/` as **copies**; originals remain in package [`fixtures/`](./fixtures/).
