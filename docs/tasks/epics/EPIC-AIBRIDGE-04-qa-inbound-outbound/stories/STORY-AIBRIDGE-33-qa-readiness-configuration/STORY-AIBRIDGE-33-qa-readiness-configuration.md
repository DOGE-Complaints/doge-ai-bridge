# STORY-AIBRIDGE-33 — QA — Readiness and configuration

## Meta
- **Key:** `STORY-AIBRIDGE-33-qa-readiness-configuration`
- **Status:** 🟡 Implemented (P6 closed · next P7 · `run_mode=aibridge_33_audit_20260917`)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-33-qa-readiness-configuration.md`
- **decision_ref:** [`STORY-AIBRIDGE-33-qa-readiness-configuration.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-33-qa-readiness-configuration.md) · [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) §10.11 READY-* · §17 smoke · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) ADR-Q1/Q2
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 · ADR-Q1/Q2
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000030-20260917-epic-aibridge-04-story-33-qa-readiness-configuration.yaml`
- **P1 materialize:** 2026-09-17T20:50:14Z
- **P3 closed:** 2026-09-17T20:57:41Z
- **P4 audited:** 2026-09-17T21:00:46Z
- **P5 disposition:** 2026-09-17T21:04:00Z · G-01…G-03 TASKED · G-04/G-05 WAIVED · `run_mode=aibridge_33_audit_20260917`
- **P6 closed:** 2026-09-17T21:07:50Z · G-01…G-03 CLOSED · t05/t06/t07 PASS
- **Gate:** [t04](./task-aibridge-33-t04-story-gate/README.md) · [acceptance PASS](./task-aibridge-33-t04-story-gate/acceptance-verification-task-aibridge-33-t04-story-gate.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Guide §10.11 READY-* / §17 smoke | [`AIBRIDGE-QA-…-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) |
| ADR-Q1/Q2 fixtures | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| Traceability READY-001…015 | [`TRACEABILITY-MATRIX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md) |
| Seed originals | package [`fixtures/ready-missing-channel-bearer.json`](../../../../backlog-stories/qa-inbound-outbound-data-flow/fixtures/ready-missing-channel-bearer.json) (READY-002); generate READY-* on P3 t02 |
| Harness | Settings overrides · `/readyz` reason codes from `readiness.py` |

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Deleting or moving package `fixtures/` originals (promote = **copy** only).
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

## Verified current state
- Seed `ready-missing-channel-bearer.json` — promoted copy hash_eq (P3 t01).
- READY-001…015 envelopes in package `fixtures/` + `tests/fixtures/settings/` (P3 t02).
- TRACEABILITY-MATRIX READY-001…015 → this story key (`covered`).
- Suite: `tests/contract/test_readyz_configuration.py` (17 passed, P3 t03).
- Product: `readiness.py` / Settings — assert-only; no product invent.

## Target / AC
- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (if any) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] On story Done: required envelopes under `tests/fixtures/settings/` as **copies**; originals remain in package `fixtures/`.

## Техническое решение

- **Approach (ADR-Q1/Q2):** promote seed copy; generate READY-* into package `fixtures/` (`schema_version=1.0`), promote=copy → `tests/fixtures/settings/`; tests in `tests/contract/` / readiness unit; Settings overrides; bounded `/readyz` reasons; no live Telegram.
- **Skill:** python-pro · test-master

## Nested tasks (pkg-000030 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-33-t01-promote-seed-fixtures](./task-aibridge-33-t01-promote-seed-fixtures/README.md) | Promote seed READY-002 | Done |
| t02 | [task-aibridge-33-t02-generate-ready-matrix-fixtures](./task-aibridge-33-t02-generate-ready-matrix-fixtures/README.md) | Generate READY-001…015 | Done |
| t03 | [task-aibridge-33-t03-implement-readyz-tests](./task-aibridge-33-t03-implement-readyz-tests/README.md) | /readyz contract suite | Done |
| t04 | [task-aibridge-33-t04-story-gate](./task-aibridge-33-t04-story-gate/README.md) | Gate all READY-* | Done |
| t05 | [task-aibridge-33-t05-audit-g01-ready001-migrated-pg](./task-aibridge-33-t05-audit-g01-ready001-migrated-pg/README.md) | G-01 READY-001 migrated PG | Done |
| t06 | [task-aibridge-33-t06-audit-g02-ready013-migration-readyz](./task-aibridge-33-t06-audit-g02-ready013-migration-readyz/README.md) | G-02 READY-013 /readyz + missing | Done |
| t07 | [task-aibridge-33-t07-audit-g03-ready005-intake-missing](./task-aibridge-33-t07-audit-g03-ready005-intake-missing/README.md) | G-03 READY-005 intake missing | Done |
