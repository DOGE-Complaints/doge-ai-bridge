# STORY-AIBRIDGE-23 — QA — Authentication and operational boundaries

## Meta
- **Key:** `STORY-AIBRIDGE-23-qa-auth-ops-boundaries`
- **Status:** 🟢 Implemented (P6 closed · next P7)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md`
- **decision_ref:** [`STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md) · [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) §2.1 · §4.1 · §10.1 AUTH-* · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) ADR-Q1/Q2
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 · ADR-Q1/Q2
- **Skill declared:** `test-master` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/test-master/SKILL.md) · pytest `python-pro`
- **Active pkg (wave):** `pkg-000020-20260917-epic-aibridge-04-story-23-qa-auth-ops-boundaries.yaml` (YAML default unchanged)
- **P1 materialize:** 2026-09-17T13:59:06Z
- **P3 closed:** 2026-09-17T14:02:23Z
- **P4 audit:** [p4-audit-STORY-AIBRIDGE-23-qa-auth-ops-boundaries-20260917.md](../../../../analysis/p4-audit-STORY-AIBRIDGE-23-qa-auth-ops-boundaries-20260917.md)
- **P5 APPLY:** 2026-09-17T14:14:10Z · `run_mode=aibridge_23_audit_20260917`
- **P6 closed:** 2026-09-17T14:18:28Z
- **Gate:** [acceptance-verification-task-aibridge-23-t04-story-gate.md](./acceptance-verification-task-aibridge-23-t04-story-gate.md) PASS
- **Run summary:** [P3](../../../../run-reports/run-summary-20260917-1402-story-aibridge-23-p3.md) · [P5](../../../../run-reports/run-summary-20260917-1414-story-aibridge-23-p5-disposition.md) · [P6](../../../../run-reports/run-summary-20260917-1416-story-aibridge-23-p6.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Guide §2.1 / §4.1 / AUTH-* | [`AIBRIDGE-QA-…-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) |
| ADR-Q1/Q2 fixtures | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| Traceability AUTH-001…012 | [`TRACEABILITY-MATRIX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md) |
| Seed originals | package [`fixtures/`](../../../../backlog-stories/qa-inbound-outbound-data-flow/fixtures/) |

## Scope
Automated **test/QA acceptance statements** covering AUTH-001…012. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Deleting or moving package `fixtures/` originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.
- Fixture promote / contract pytest bodies in P1 (P3).

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

## Verified current state
- Seed copy: `tests/fixtures/channel/turns-valid-private.json` (package original intact).
- AUTH envelopes + copies under `tests/fixtures/{channel,settings,spies}/`.
- Contract: `tests/contract/test_auth_ops_boundaries.py` · `tests/fixture_loader.py` (15 passed · 2026-09-17T14:02:23Z).
- TRACEABILITY-MATRIX AUTH-001…012 → this story key.

## Target / AC
- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (if any) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] On story Done: all required envelopes exist under `tests/fixtures/{cluster}/` as **copies**; originals remain in package `fixtures/`.

## Техническое решение (projected)

- **Approach (ADR-Q1/Q2):** promote fixtures as **copies** from package `fixtures/` → `tests/fixtures/{cluster}/`. Generate missing AUTH envelopes into package `fixtures/` first, then copy. Contract tests under `tests/contract/` + TestClient auth variants for AUTH-001…012. Gate: no Bearer leak; originals intact.
- **Skill:** test-master · python-pro  
- **Arch:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) ADR-Q1/Q2

## Точки в коде
- `tests/contract/` (P3), `tests/fixtures/{channel,settings,spies}/` (P3 copies)
- Package originals: `backlog-stories/qa-inbound-outbound-data-flow/fixtures/`
- Channel auth / `/healthz` / `/readyz` / `/metrics` in `src/aibridge/`

## Nested tasks (pkg-000020 order + P5 audit queue)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-23-t01-promote-seed-fixtures](./task-aibridge-23-t01-promote-seed-fixtures/README.md) | Seed copy → `tests/fixtures/channel/` | Done |
| t02 | [task-aibridge-23-t02-generate-auth-matrix-fixtures](./task-aibridge-23-t02-generate-auth-matrix-fixtures/README.md) | AUTH-002…012 generate + promote copies | Done |
| t03 | [task-aibridge-23-t03-implement-contract-auth-tests](./task-aibridge-23-t03-implement-contract-auth-tests/README.md) | `tests/contract/` AUTH-* | Done |
| t04 | [task-aibridge-23-t04-story-gate](./task-aibridge-23-t04-story-gate/README.md) | All AUTH-* + originals intact | Done |
| t05 | [task-aibridge-23-t05-audit-g01-auth009-logs](./task-aibridge-23-t05-audit-g01-auth009-logs/README.md) | G-01 AUTH-009 `forbid_substrings_in_logs` | Done |
| t06 | [task-aibridge-23-t06-audit-g05-rate-limit-principal](./task-aibridge-23-t06-audit-g05-rate-limit-principal/README.md) | G-05 hash rate-limit principal | Done |

### P5 disposition (2026-09-17T14:14:10Z)

| Gap | Sev | Disposition | Task |
|-----|-----|-------------|------|
| G-01 | Medium | TASKED | t05 |
| G-02 | Info | WAIVED reason=out-of-DoD | — |
| G-03 | Info | WAIVED reason=info-nonblocking | — |
| G-04 | Info | WAIVED reason=info-nonblocking | — |
| G-05 | Low | TASKED | t06 |
