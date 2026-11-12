# STORY-AIBRIDGE-REQ9-03 — GATEWAY_* + SPA_BASE_URL hard cut (R1 R2 R4 R8)

## Meta
- **Key:** `STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut`
- **Status:** P6 Done · G-01 **CLOSED** · G-02/G-03 WAIVED · pkg-000047 · next **P7** · `run_mode=aibridge_req9_03_audit_20260926` · 2026-09-26T12:53:50Z
- **Parent Epic:** [`EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming.md`](../../EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming.md)
- **source:** `backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md`
- **decision_ref:** [`STORY-AIBRIDGE-REQ9-03-….md`](../../../../backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md) · [`REQ-08`](../../../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) §2–§5 · R1 R2 R4 R8 · [`02-env-auth-url-naming.md`](../../../../../../docs/architecture/req9-ops-naming/02-env-auth-url-naming.md)
- **Package:** [`req-08-req9-ops-parity-gateway-naming/INDEX.md`](../../../../backlog-stories/req-08-req9-ops-parity-gateway-naming/INDEX.md)
- **Skill declared:** `python-pro` · soft `code-documenter` · t06 `code-documenter`
- **Operator lock:** **A** — full hard cut; **no** dual-read · **C** — Railway names checklist only (live → 04)
- **Active pkg (wave):** `pkg-000047-20260926-epic-aibridge-06-story-req9-03-gateway-spa-env-hard-cut.yaml` (immutable under override)
- **P1 materialize:** 2026-09-26T12:38:37Z
- **P3 close:** 2026-09-26T12:46:12Z · [p3](../../../run-reports/run-summary-20260926-1246-story-aibridge-req9-03-p3.md)
- **P4 audit:** 2026-09-26T12:49:31Z · [p4](../../../../analysis/p4-audit-STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut-20260926.md)
- **P5 APPLY:** 2026-09-26T12:52:08Z · [p5](../../../run-reports/run-summary-20260926-1252-story-aibridge-req9-03-p5-disposition.md)
- **P6 close:** 2026-09-26T12:53:50Z · G-01 CLOSED · [p6](../../../run-reports/run-summary-20260926-1253-story-aibridge-req9-03-p6.md)
- **Gate:** [t05](./task-aibridge-req9-03-t05-story-gate/README.md) **PASS**
- **Depends:** 01 · 02

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-08 R1/R2/R4/R8 | [`REQ-08`](../../../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) |
| Env naming | [`02-env-auth-url-naming.md`](../../../../../../docs/architecture/req9-ops-naming/02-env-auth-url-naming.md) |
| Hard cut / migration | [`03-coexistence-and-migration.md`](../../../../../../docs/architecture/req9-ops-naming/03-coexistence-and-migration.md) |

## Scope
Hard cut (no dual-read of old names):

| From (remove) | To (primary) |
|---------------|--------------|
| `DOGESTONIA_INTAKE_BASE_URL` / `dogestonia_intake_base_url` (+ helpers) | `GATEWAY_BASE_URL` / `gateway_base_url` |
| `DOGESTONIA_API_BEARER_TOKEN` / `dogestonia_api_bearer_token` | `GATEWAY_SERVICE_API_TOKEN` / `gateway_service_api_token` |
| `DOGESTONIA_DRAFT_REDIRECT_BASE_URL` / draft-redirect fields | `SPA_BASE_URL` / `spa_base_url` |

- Update `.env.example`, runbooks, manuals, QA fixtures/tests.
- Keep `AIBRIDGE_CHANNEL_BEARER_TOKEN` distinct (R8).
- Railway **target var names** checklist — no live Railway for Done of 03.

## Вне scope
- Dual-read; rename channel to `SERVICE_API_TOKEN`; OpenAPI; invent waitlist; live Railway proof (→ 04).

## Context
P3 Done: hard cut in `config.py` / consumers / `.env.example` / docs / tests. Railway live → 04.

## Target / AC
- [x] R1 R2 R4 hard cut in config + template + docs + tests (env **and** Python)
- [x] R8 channel Keep and ≠ `GATEWAY_SERVICE_API_TOKEN`
- [x] No dual-read of removed names
- [x] Railway **names checklist** present (proof deferred to 04)
- [x] Nested tasks Done at execute

## Nested tasks (pkg-000047)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-req9-03-t01-config-settings-hard-cut](./task-aibridge-req9-03-t01-config-settings-hard-cut/README.md) | R1/R2/R4 config | Done |
| t02 | [task-aibridge-req9-03-t02-gateway-readiness-consumers-r8](./task-aibridge-req9-03-t02-gateway-readiness-consumers-r8/README.md) | consumers + R8 | Done |
| t03 | [task-aibridge-req9-03-t03-env-example-docs-railway-checklist](./task-aibridge-req9-03-t03-env-example-docs-railway-checklist/README.md) | template/docs/checklist | Done |
| t04 | [task-aibridge-req9-03-t04-tests-fixtures-hard-cut](./task-aibridge-req9-03-t04-tests-fixtures-hard-cut/README.md) | tests | Done |
| t05 | [task-aibridge-req9-03-t05-story-gate](./task-aibridge-req9-03-t05-story-gate/README.md) | story AC gate | Done · PASS |
| t06 | [task-aibridge-req9-03-t06-audit-g01-req01-env-ssot](./task-aibridge-req9-03-t06-audit-g01-req01-env-ssot/README.md) | P5 G-01 REQ-01 SSOT | Done · G-01 CLOSED |
