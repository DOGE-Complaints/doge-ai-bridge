# STORY-AIBRIDGE-12 — Env + `/readyz` + 500 + dry-run gate

## Meta
- **Key:** `STORY-AIBRIDGE-12-readyz-env-dryrun-gate`
- **Status:** 🟢 Done (P3 · P6 audit CLOSED · next P7)
- **Parent Epic:** [`EPIC-AIBRIDGE-02-req-03-runtime-remediation.md`](../../EPIC-AIBRIDGE-02-req-03-runtime-remediation.md)
- **source:** `backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md`
- **decision_ref:** [`STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md`](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md) · [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §2 · §5.5–5.6 · P0-11
- **Parent REQ:** [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §2 · §5.5–5.6 · P0-11
- **Package:** [`req-03-runtime-remediation/INDEX.md`](../../../../backlog-stories/req-03-runtime-remediation/INDEX.md)
- **Siblings:** [09](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [13](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md) · [14](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Active pkg (wave):** `pkg-000010-20260913-epic-aibridge-02-story-12-readyz-env-dryrun-gate.yaml`
- **P1 materialize:** 2026-09-13T16:15:49Z
- **P3 Done:** 2026-09-13T16:22:32Z
- **P6 Done:** 2026-09-13T16:30:46Z · `run_mode=aibridge_12_audit_20260913`

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Wave 1 dry-run | REQ-03 [§2](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| `/readyz` | REQ-03 [§5.5](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| Env normalization | REQ-03 [§5.6](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| Bounded 500 | REQ-03 P0-11 · AC #9 |

## Scope
- Canonical `DOGESTONIA_INTAKE_BASE_URL`; removed GATEWAY_ORIGIN removed or temporary documented alias; both set differently → readiness fail.
- Settings accept TTL, max response bytes, timeouts, log level, rate limits, all LLM budget vars; `.env.example` matches.
- `/readyz`: config/DB/migration/bundle/tool/OpenAI **presence**/HTTPS origin syntax/distinct Bearers/redirect; **no** OpenAI generation; **no** gateway write; optional probes read-only/bounded/cached.
- Until R3-P1-03 (story 14): `AIBRIDGE_DRY_RUN=false` must **fail** readiness.
- Bounded JSON **500** channel envelope (REQ-03 P0-11 / AC #9).

## Вне scope
- Full schema validation implementation (14); inventing budget numeric defaults beyond «wired when set».

## Verified current state (P1)
- Soft `/readyz` (auth/bearers/bundle) — `src/aibridge/app.py`.
- Gateway origin alias removed GATEWAY_ORIGIN — `src/aibridge/config.py`.
- `AIBRIDGE_DRY_RUN` field exists — `config.py` (gate vs readiness not yet per REQ-03 §2).

## Target / AC
- [x] §5.5 and §5.6 satisfied.
- [x] Dry-run readiness gate until story 14 P1-03 complete.
- [x] Unhandled errors → bounded channel JSON 500 conforming to OpenAPI.

## Точки в коде
- `src/aibridge/app.py`, `config.py`, `readiness.py`, `.env.example`, `gateway.py`

## Dependencies
- [STORY-AIBRIDGE-09](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md)

## Nested tasks (pkg-000010 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-02-12-t01-canonical-gateway-base-url](./task-aibridge-02-12-t01-canonical-gateway-base-url/README.md) | Scope #1 | Done |
| t02 | [task-aibridge-02-12-t02-settings-env-example](./task-aibridge-02-12-t02-settings-env-example/README.md) | Scope #2 | Done |
| t03 | [task-aibridge-02-12-t03-readyz-strict-checks](./task-aibridge-02-12-t03-readyz-strict-checks/README.md) | Scope #3; §5.5 | Done |
| t04 | [task-aibridge-02-12-t04-dryrun-readiness-gate](./task-aibridge-02-12-t04-dryrun-readiness-gate/README.md) | Scope #4; AC #2 | Done |
| t05 | [task-aibridge-02-12-t05-bounded-channel-500](./task-aibridge-02-12-t05-bounded-channel-500/README.md) | Scope #5; AC #3 | Done |
| t06 | [task-aibridge-02-12-t06-story-acceptance-verification](./task-aibridge-02-12-t06-story-acceptance-verification/README.md) | Target AC gate | Done |
| t07 | [task-aibridge-02-12-t07-audit-g01-wire-settings-knobs](./task-aibridge-02-12-t07-audit-g01-wire-settings-knobs/README.md) | P5 G-01 | Done |
| t08 | [task-aibridge-02-12-t08-audit-g02-readyz-strict-tool](./task-aibridge-02-12-t08-audit-g02-readyz-strict-tool/README.md) | P5 G-02 | Done |
| t09 | [task-aibridge-02-12-t09-audit-g03-backlog-verified-sync](./task-aibridge-02-12-t09-audit-g03-backlog-verified-sync/README.md) | P5 G-03 | Done |
