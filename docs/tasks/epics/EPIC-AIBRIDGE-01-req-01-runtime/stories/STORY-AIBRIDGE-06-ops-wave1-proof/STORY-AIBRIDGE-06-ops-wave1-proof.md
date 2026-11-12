# STORY-AIBRIDGE-06 — Ops, metrics, wave-1 proof

## Meta
- **Key:** `STORY-AIBRIDGE-06-ops-wave1-proof`
- **Status:** 🟢 Done (P3 gate PASS · awaiting P4)
- **Parent Epic:** [`EPIC-AIBRIDGE-01-req-01-runtime.md`](../../EPIC-AIBRIDGE-01-req-01-runtime.md)
- **source:** `backlog-stories/req-01-runtime/STORY-AIBRIDGE-06-ops-wave1-proof.md`
- **decision_ref:** [`STORY-AIBRIDGE-06-ops-wave1-proof.md`](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-06-ops-wave1-proof.md) · [`REQ-01`](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §18–§19, §22 · [`04-ops-security.md`](../../../../../architecture/runtime/04-ops-security.md)
- **Parent REQ:** [`REQ-01`](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §18–§19, §22 deliverables; arch wave-1
- **Package:** [`req-01-runtime/INDEX.md`](../../../../backlog-stories/req-01-runtime/INDEX.md)
- **Siblings:** [01](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md) … [05](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-05-gateway-outcomes.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Active pkg (wave):** `pkg-000006-20260912-epic-aibridge-01-story-06-ops-wave1.yaml`
- **P1 materialize:** 2026-09-12T22:02:06Z
- **P3 Done:** 2026-09-12T22:06:45Z
- **Gate:** [acceptance-verification … t06](./acceptance-verification-task-aibridge-01-06-t06-story-acceptance-verification.md) PASS
- **Run summary:** [run-summary-20260912-2206-story-aibridge-06-p3.md](../../../../run-reports/run-summary-20260912-2206-story-aibridge-06-p3.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Observability & privacy boundary | [00-overview.md §8](../../../../../architecture/runtime/00-overview.md) |
| Startup/health, budgets, metrics/logs, secrets, privacy, wave/node checklists | [04-ops-security.md](../../../../../architecture/runtime/04-ops-security.md) (§1–§6) |
| Wave-1 live façade proof | [01-channel-facade.md §7](../../../../../architecture/runtime/01-channel-facade.md); [00-overview.md §7](../../../../../architecture/runtime/00-overview.md) |
| Startup, health, shutdown | REQ-01 [§18 AIB-OPS-01…03](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Trust boundaries, logging, defensive controls | REQ-01 [§19 AIB-SEC-01…03](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Testing / acceptance / deliverables checklist | REQ-01 [§20–§22](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Channel Bearer rotation | [`channel-bearer-rotation.md`](../../../../../runbooks/channel-bearer-rotation.md) |
| Privacy pilot | [`privacy-pilot.md`](../../../../../runbooks/privacy-pilot.md) |
| Unknown outcome ops | [`unknown-outcome-reconciliation.md`](../../../../../runbooks/unknown-outcome-reconciliation.md) |
| n8n import/smoke contract | [`n8n-channel-workflow/README.md`](../../../../../ops/n8n-channel-workflow/README.md) |
| Config env names | REQ-01 [§17](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |

## Scope
- `/metrics` Prometheus-compatible, private-only, no PII / narrative / secrets; include budget-stop reasons.
- Redacted audit logging per AIB-SEC-02.
- Operator README stubs: private net, n8n mapping, rotation (link existing runbooks — do not duplicate secrets).
- Disk verify: privacy-pilot, unknown-outcome, channel-bearer-rotation, n8n-channel-workflow README.
- Wave-1 gate checklist: `/readyz` + 401 smoke + live n8n → `/v1/channel/turns` (dry-run/interview) without stash.
- `.env.example` **names only** incl. budget knobs (no secret values).

## Вне scope
- Full wave-2 mobile SPA E2E as separate later story if needed; inventing n8n workflow JSON body; APM SaaS; REQ-02.

## Verified current state (post-P3)
- `src/aibridge/metrics.py`, `audit.py`; `/metrics` in `app.py`.
- Ops stubs + wave-1 checklist on disk; runbooks present.
- Tests: `tests/test_ops_wave1.py` · suite **96 passed, 1 skipped**.

## Target / AC
- [x] `/metrics` without channel Bearer on private interface returns series without narrative samples.
- [x] Unique test phrase absent from default logs/metrics after a turn ([privacy-pilot.md](../../../../../runbooks/privacy-pilot.md)).
- [x] Wave-1 checklist documented and executable (live n8n call may be manual ops proof).
- [x] Runbook/ops paths exist (`ls` verify against Doc pointers table).
- [x] `.env.example` lists required knobs from REQ-01 §17 without secret values.

## Точки в коде
- `src/aibridge/metrics.py`, `audit.py`, `budgets.py`, `channel.py`, `app.py`
- `docs/ops/operator-pilot-readme.md`, `docs/ops/wave1-gate-checklist.md`
- `.env.example` · `tests/test_ops_wave1.py`

## Dependencies
- [STORY-AIBRIDGE-01](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md) … [STORY-AIBRIDGE-05](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-05-gateway-outcomes.md).

## Nested tasks (pkg-000006 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-01-06-t01-metrics-prometheus](./task-aibridge-01-06-t01-metrics-prometheus/README.md) | Scope #1; AC #1 | Done |
| t02 | [task-aibridge-01-06-t02-redacted-audit-logs](./task-aibridge-01-06-t02-redacted-audit-logs/README.md) | Scope #2; AC #2 | Done |
| t03 | [task-aibridge-01-06-t03-ops-readme-runbook-verify](./task-aibridge-01-06-t03-ops-readme-runbook-verify/README.md) | Scope #3,#4; AC #4 | Done |
| t04 | [task-aibridge-01-06-t04-wave1-gate-checklist](./task-aibridge-01-06-t04-wave1-gate-checklist/README.md) | Scope #5; AC #3 | Done |
| t05 | [task-aibridge-01-06-t05-env-example-knobs](./task-aibridge-01-06-t05-env-example-knobs/README.md) | Scope #6; AC #5 | Done |
| t06 | [task-aibridge-01-06-t06-story-acceptance-verification](./task-aibridge-01-06-t06-story-acceptance-verification/README.md) | AC #1–#5 gate | Done |
| t07 | [task-aibridge-01-06-t07-audit-g01-wire-metric-increments](./task-aibridge-01-06-t07-audit-g01-wire-metric-increments/README.md) | P4 G-01 | Done (P6) |
