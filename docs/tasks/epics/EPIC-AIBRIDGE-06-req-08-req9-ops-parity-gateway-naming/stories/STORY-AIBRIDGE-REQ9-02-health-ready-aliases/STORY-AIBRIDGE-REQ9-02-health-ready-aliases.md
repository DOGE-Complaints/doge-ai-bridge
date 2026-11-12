# STORY-AIBRIDGE-REQ9-02 — GET /health and /ready aliases

## Meta
- **Key:** `STORY-AIBRIDGE-REQ9-02-health-ready-aliases`
- **Status:** ✅ P6 Done · G-01/G-02 **CLOSED** · G-03 WAIVED · next **P7** · `run_mode=aibridge_req9_02_audit_20260926` · pkg-000046 · 2026-09-26T12:33:39Z
- **Parent Epic:** [`EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming.md`](../../EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming.md)
- **source:** `backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md`
- **decision_ref:** [`STORY-AIBRIDGE-REQ9-02-….md`](../../../../backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md) · [`REQ-08`](../../../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) §4 · G2 · [`01-runtime-and-probes.md`](../../../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md)
- **Package:** [`req-08-req9-ops-parity-gateway-naming/INDEX.md`](../../../../backlog-stories/req-08-req9-ops-parity-gateway-naming/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000046-20260926-epic-aibridge-06-story-req9-02-health-ready-aliases.yaml`
- **P1 materialize:** 2026-09-26T12:24:30Z
- **P3 close:** 2026-09-26T12:27:23Z · [run-summary](../../../../run-reports/run-summary-20260926-1227-story-aibridge-req9-02-p3.md)
- **P4 audit:** 2026-09-26T12:29:37Z · [p4](../../../../analysis/p4-audit-STORY-AIBRIDGE-REQ9-02-health-ready-aliases-20260926.md)
- **P5 disposition:** 2026-09-26T12:31:20Z · [p5](../../../../run-reports/run-summary-20260926-1231-story-aibridge-req9-02-p5-disposition.md)
- **P6 close:** 2026-09-26T12:33:39Z · [p6](../../../../run-reports/run-summary-20260926-1233-story-aibridge-req9-02-p6.md)
- **Gate:** [t04](./task-aibridge-req9-02-t04-story-gate/README.md) **PASS**
- **Depends:** None (∥ 01)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-08 G2 | [`REQ-08`](../../../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) |
| Probes / aliases | [`01-runtime-and-probes.md`](../../../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md) |

## Scope
- Expose `GET /health` and `GET /ready` with same semantics as existing `/healthz` / `/readyz` (aliases OK; keep both paths unless implement documents otherwise).
- Update docs/runbooks that cite only `z` paths to list short paths as REQ9-primary.

## Вне scope
- Changing readiness evaluation logic; Makefile (01); env renames (03); Railway live verify (04).

## Context
P3: stacked `/health` `/ready` on existing handlers; parity tests; runbooks REQ9-primary.

## Target / AC
- [x] G2: `GET /health` and `GET /ready` peer-parity probe semantics
- [x] Nested tasks Done at execute

## Nested tasks (pkg-000046)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-req9-02-t01-health-ready-route-aliases](./task-aibridge-req9-02-t01-health-ready-route-aliases/README.md) | G2 routes | **Done** |
| t02 | [task-aibridge-req9-02-t02-probe-alias-parity-tests](./task-aibridge-req9-02-t02-probe-alias-parity-tests/README.md) | parity tests | **Done** |
| t03 | [task-aibridge-req9-02-t03-runbook-req9-primary-short-paths](./task-aibridge-req9-02-t03-runbook-req9-primary-short-paths/README.md) | runbooks | **Done** |
| t04 | [task-aibridge-req9-02-t04-story-gate](./task-aibridge-req9-02-t04-story-gate/README.md) | story AC gate | **PASS** |
| t05 | [task-aibridge-req9-02-t05-audit-g01-channel-bearer-rotation-ready-alias](./task-aibridge-req9-02-t05-audit-g01-channel-bearer-rotation-ready-alias/README.md) | G-01 rotation runbook | **Done** · CLOSED |
| t06 | [task-aibridge-req9-02-t06-audit-g02-readme-health-ready-aliases](./task-aibridge-req9-02-t06-audit-g02-readme-health-ready-aliases/README.md) | G-02 README | **Done** · CLOSED |

### P5 disposition → P6 CLOSED (2026-09-26T12:33:39Z)

| Gap | Sev | Disposition | Task |
|-----|-----|-------------|------|
| G-01 | Low | TASKED → **CLOSED** (P6) | t05 Done |
| G-02 | Info | TASKED → **CLOSED** (P6) | t06 Done |
| G-03 | Info | **WAIVED** | — |

**activation:** `run_mode=aibridge_req9_02_audit_20260926` · [p6](../../../../run-reports/run-summary-20260926-1233-story-aibridge-req9-02-p6.md) · next=P7
