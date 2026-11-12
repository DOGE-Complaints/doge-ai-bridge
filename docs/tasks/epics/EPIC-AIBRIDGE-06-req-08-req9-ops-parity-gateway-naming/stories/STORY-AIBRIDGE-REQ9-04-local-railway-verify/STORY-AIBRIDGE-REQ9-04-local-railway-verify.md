# STORY-AIBRIDGE-REQ9-04 — Local + Railway verify (or residual)

## Meta
- **Key:** `STORY-AIBRIDGE-REQ9-04-local-railway-verify`
- **Status:** P5 Done · TASKED=0 · WAIVED G-01…G-04 · activation none · next **P7** (skip P6) · Lock **C** residual Y · 2026-09-26T13:08:56Z
- **Parent Epic:** [`EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming.md`](../../EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming.md)
- **source:** `backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-04-local-railway-verify.md`
- **decision_ref:** [`STORY-AIBRIDGE-REQ9-04-….md`](../../../../backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-04-local-railway-verify.md) · [`REQ-08`](../../../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) §5 · §6 · [`04-verify-and-topology-sync.md`](../../../../../../docs/architecture/req9-ops-naming/04-verify-and-topology-sync.md)
- **Package:** [`req-08-req9-ops-parity-gateway-naming/INDEX.md`](../../../../backlog-stories/req-08-req9-ops-parity-gateway-naming/INDEX.md)
- **Skill declared:** `test-master` · soft `code-documenter`
- **Operator lock (Railway):** **C** — verify vars from 03 **or** residual if id Unknown / no live access; **no invent SUCCESS**
- **Active pkg (wave):** `pkg-000048-20260926-epic-aibridge-06-story-req9-04-local-railway-verify.yaml`
- **P1 materialize:** 2026-09-26T12:58:34Z
- **Gate:** [t05](./task-aibridge-req9-04-t05-story-gate/README.md) · **PASS** 2026-09-26T13:03:46Z · [p3](../../../../run-reports/run-summary-20260926-1303-story-aibridge-req9-04-p3.md) · [p5](../../../../run-reports/run-summary-20260926-1308-story-aibridge-req9-04-p5-disposition.md)
- **Depends:** 01 · 02 · 03

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-08 §5–§6 / G9 | [`REQ-08`](../../../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) |
| Verify surfaces | [`04-verify-and-topology-sync.md`](../../../../../../docs/architecture/req9-ops-naming/04-verify-and-topology-sync.md) |
| Railway names checklist (03) | [`STORY-AIBRIDGE-REQ9-03`](../../../../backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md) §Railway checklist · runbook §2.4.1 |

## Scope
- Local: `make serve`/`dev` on 8080; curl `/health` + `/ready`; template shows `GATEWAY_BASE_URL` / `GATEWAY_SERVICE_API_TOKEN` / `SPA_BASE_URL`.
- Railway: apply/verify target vars **or** explicit residual (id Unknown / no live access). Lock C — no invent SUCCESS.
- Evidence note (no secrets): pattern `docs/ops/req-08-req9-verify-YYYYMMDD.md` — **create at P3**.
- Topology sync when facts exist (tech-arch 04).

## Вне scope
- Invent Railway project/service id or SUCCESS without evidence
- Expand smoke beyond `/health`/`/ready` unless implement chooses (REQ §6 TBD)
- Re-do hard-cut from 03

## Context
Railway ids verified (DOGEstonia / doge-ai-bridge / tallinn-demo). Product hard-cut 01–03 Done. Evidence [`req-08-req9-verify-20260926.md`](../../../../../ops/req-08-req9-verify-20260926.md).

## Target / AC
- [x] Local verify per tech-arch 04
- [x] Railway verify **or** residual explicitly recorded
- [x] REQ-08 §5 G9 local+Railway verify clause satisfied or residual linked
- [x] Nested tasks Done at execute

## Nested tasks (pkg-000048)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-req9-04-t01-local-make-health-ready-verify](./task-aibridge-req9-04-t01-local-make-health-ready-verify/README.md) | Local probes | Done |
| t02 | [task-aibridge-req9-04-t02-railway-verify-or-residual](./task-aibridge-req9-04-t02-railway-verify-or-residual/README.md) | Railway · Lock C | Done · residual Y |
| t03 | [task-aibridge-req9-04-t03-evidence-ops-note](./task-aibridge-req9-04-t03-evidence-ops-note/README.md) | Evidence note | Done |
| t04 | [task-aibridge-req9-04-t04-topology-sync-devops](./task-aibridge-req9-04-t04-topology-sync-devops/README.md) | Topology sync | Done |
| t05 | [task-aibridge-req9-04-t05-story-gate](./task-aibridge-req9-04-t05-story-gate/README.md) | story AC gate | PASS |
