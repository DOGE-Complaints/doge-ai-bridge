# STORY-AIBRIDGE-14 — P1 ops + full schema + restart tests

## Meta
- **Key:** `STORY-AIBRIDGE-14-p1-ops-schema-restart`
- **Status:** 🟢 Done (P3 · P6 audit CLOSED · next P7)
- **Parent Epic:** [`EPIC-AIBRIDGE-02-req-03-runtime-remediation.md`](../../EPIC-AIBRIDGE-02-req-03-runtime-remediation.md)
- **source:** `backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md`
- **decision_ref:** [`STORY-AIBRIDGE-14-p1-ops-schema-restart.md`](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md) · [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §6 P1-01–04 · P1-06–07
- **Parent REQ:** [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §6 P1-01–04 · P1-06–07 (P1-05 superseded by P0-13)
- **Package:** [`req-03-runtime-remediation/INDEX.md`](../../../../backlog-stories/req-03-runtime-remediation/INDEX.md)
- **Siblings:** [12](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md) · [13](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md) · [16](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-16-privacy-retention.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)  
  Dockerfile slice: `devops-engineer` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/devops-engineer/SKILL.md)
- **Active pkg (wave):** `pkg-000012-20260913-epic-aibridge-02-story-14-p1-ops-schema-restart.yaml`
- **P1 materialize:** 2026-09-13T17:03:24Z
- **P3 Done:** 2026-09-13T17:14:26Z
- **P6 Done:** 2026-09-13T17:23:30Z · `run_mode=aibridge_14_audit_20260913`

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| P1 table | REQ-03 [§6](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) R3-P1-01…07 |
| Dry-run until schema | REQ-03 [§2](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) · story [12](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md) |
| Wave-1 E2E baseline | [STORY-13](../STORY-AIBRIDGE-13-wave1-asgi-e2e/STORY-AIBRIDGE-13-wave1-asgi-e2e.md) |
| Channel OpenAPI SSOT | [`docs/openapi/aibridge-channel-v1.openapi.yaml`](../../../../../openapi/aibridge-channel-v1.openapi.yaml) |

## Scope
- Graceful shutdown (AIB-OPS-03 / R3-P1-01).
- Channel **429** / rate limits + finite budget defaults; budgets enforced on `/turns` (R3-P1-02).
- **Full schema validation** (enum etc.); blocks real gateway readiness (R3-P1-03) — lifts dry-run-only gate from story 12 / REQ-03 §2.
- Restart recovery + DB race/restart tests: Send / pending-confirm / `unknown_outcome` (R3-P1-04; AC #7–#8).
- Gateway response-size limit / remaining §17 timeout knobs (R3-P1-06).
- Dockerfile for reproducible deploy / node clone (R3-P1-07).

## Вне scope
- Dual instructions (done in 10 / P0-13); n8n live gate (15); privacy (16); SPA E2E (17); P2 (18).

## Verified current state (post-P3 / P6)
- Graceful shutdown: ASGI lifespan + `accepting_traffic` drain → 503 `shutting_down`; `recover_all_executing_attempts` on stop.
- Finite rate/budget defaults in `config.py`; `BudgetGuard` always attached; channel 429 when limited.
- Schema validator: enum/const/min/max/pattern; readiness allows `DRY_RUN=false` when `SCHEMA_VALIDATION_COMPLETE=true`.
- Restart/race tests in `tests/test_story_14_ops_schema_restart.py` (in-memory) + **P6** disposable-PG suite in `tests/test_story_14_audit_gaps.py`.
- Gateway max response bytes + HTTP timeout defaults wired; **P6** connect timeout applied to gateway httpx.
- **P6 G-03:** `schema_validation_complete()` is enum/const probe (not frozenset tautology).
- `Dockerfile` + `.dockerignore` at repo root.

## Target / AC
- [x] R3-P1-01,02,03,04,06,07 closed with tests/evidence.
- [x] `AIBRIDGE_DRY_RUN=false` may pass readiness only after full schema validation is proven.
- [x] Restart/race tests cover AC #7–#8.

## Точки в коде
- `src/aibridge/app.py`, `config.py`, `readiness.py`, `request_assembly.py`, `rate_limit.py`, `budgets.py`, `gateway.py`
- `tests/test_story_14_ops_schema_restart.py`, `tests/test_story_14_audit_gaps.py`
- `Dockerfile`, `.dockerignore`, `.env.example`

## Dependencies
- [13](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md)

## Nested tasks (pkg-000012 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-02-14-t01-graceful-shutdown-ops03](./task-aibridge-02-14-t01-graceful-shutdown-ops03/README.md) | Scope #1 · R3-P1-01 | Done |
| t02 | [task-aibridge-02-14-t02-rate-limits-budget-defaults](./task-aibridge-02-14-t02-rate-limits-budget-defaults/README.md) | Scope #2 · R3-P1-02 | Done |
| t03 | [task-aibridge-02-14-t03-full-schema-validation-readyz](./task-aibridge-02-14-t03-full-schema-validation-readyz/README.md) | Scope #3 · R3-P1-03 · Target #2 | Done |
| t04 | [task-aibridge-02-14-t04-restart-race-send-confirm](./task-aibridge-02-14-t04-restart-race-send-confirm/README.md) | Scope #4 · R3-P1-04 · Target #3 | Done |
| t05 | [task-aibridge-02-14-t05-gateway-size-timeout-knobs](./task-aibridge-02-14-t05-gateway-size-timeout-knobs/README.md) | Scope #5 · R3-P1-06 | Done |
| t06 | [task-aibridge-02-14-t06-dockerfile-reproducible-deploy](./task-aibridge-02-14-t06-dockerfile-reproducible-deploy/README.md) | Scope #6 · R3-P1-07 | Done |
| t07 | [task-aibridge-02-14-t07-story-acceptance-verification](./task-aibridge-02-14-t07-story-acceptance-verification/README.md) | Target AC gate | Done |
| t08 | [task-aibridge-02-14-t08-audit-g01-pg-restart-race](./task-aibridge-02-14-t08-audit-g01-pg-restart-race/README.md) | P5 G-01 | Done |
| t09 | [task-aibridge-02-14-t09-audit-g02-gateway-connect-timeout](./task-aibridge-02-14-t09-audit-g02-gateway-connect-timeout/README.md) | P5 G-02 | Done |
| t10 | [task-aibridge-02-14-t10-audit-g03-schema-complete-probe](./task-aibridge-02-14-t10-audit-g03-schema-complete-probe/README.md) | P5 G-03 | Done |
