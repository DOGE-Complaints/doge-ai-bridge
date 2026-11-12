# STORY-AIBRIDGE-REQ9-01 — Makefile serve/dev + .env + railpack 8080

## Meta
- **Key:** `STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack`
- **Status:** ✅ P6 Done · G-01…G-03 **CLOSED** · next **P7** · `run_mode=aibridge_req9_01_audit_20260926` · pkg-000045 · 2026-09-26T12:20:13Z
- **Parent Epic:** [`EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming.md`](../../EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming.md)
- **source:** `backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md`
- **decision_ref:** [`STORY-AIBRIDGE-REQ9-01-….md`](../../../../backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md) · [`REQ-08`](../../../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) §1–§2 · G1 G3 G8 G9 · [`01-runtime-and-probes.md`](../../../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md)
- **Package:** [`req-08-req9-ops-parity-gateway-naming/INDEX.md`](../../../../backlog-stories/req-08-req9-ops-parity-gateway-naming/INDEX.md)
- **Skill declared:** `python-pro` · soft `devops-engineer`
- **Active pkg (wave):** `pkg-000045-20260926-epic-aibridge-06-story-req9-01-make-serve-env-railpack.yaml`
- **P1 materialize:** 2026-09-26T12:12:53Z
- **P3 close:** 2026-09-26T12:14:54Z · [run-summary](../../../../run-reports/run-summary-20260926-1214-story-aibridge-req9-01-p3.md)
- **P4 audit:** 2026-09-26T12:16:55Z · [p4](../../../../analysis/p4-audit-STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack-20260926.md)
- **P5 disposition:** 2026-09-26T12:18:29Z · [p5](../../../../run-reports/run-summary-20260926-1218-story-aibridge-req9-01-p5-disposition.md)
- **P6 close:** 2026-09-26T12:20:13Z · [p6](../../../../run-reports/run-summary-20260926-1220-story-aibridge-req9-01-p6.md)
- **Gate:** [t04](./task-aibridge-req9-01-t04-story-gate/README.md) **PASS**
- **Depends:** None (∥ 02)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-08 G1/G3/G8/G9 | [`REQ-08`](../../../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) |
| Runtime / Make / railpack | [`01-runtime-and-probes.md`](../../../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md) |

## Scope
- Add `Makefile`: `serve` / `dev` → uvicorn `aibridge.app:app` on `:8080` with required `.env` load (`set -a && . ./.env && set +a`, G8).
- README primary start → `make serve` / `make dev` (G1); `python -m aibridge` may remain thin alias.
- `railpack.json` startCommand: `${PORT:-8080}` (G3); keep `aibridge.app:app` (G9).

## Вне scope
- Probe aliases (02); env/Python hard-cut R1/R2/R4 (03); Railway live verify (04); renaming channel Bearer to `SERVICE_API_TOKEN`.

## Context
P3: Makefile + README + railpack PORT 8080 shipped. `__main__.py` already G9.

## Target / AC
- [x] G1 Makefile + README primary start
- [x] G8 `.env` required on Make serve/dev
- [x] G3 railpack fallback 8080
- [x] G9 uvicorn app string `aibridge.app:app`
- [x] Nested tasks Done at execute

## Nested tasks (pkg-000045)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-req9-01-t01-makefile-serve-dev-env](./task-aibridge-req9-01-t01-makefile-serve-dev-env/README.md) | G1/G8 Makefile+.env | **Done** |
| t02 | [task-aibridge-req9-01-t02-readme-primary-make-start](./task-aibridge-req9-01-t02-readme-primary-make-start/README.md) | G1 README | **Done** |
| t03 | [task-aibridge-req9-01-t03-railpack-port-8080-keep-app](./task-aibridge-req9-01-t03-railpack-port-8080-keep-app/README.md) | G3/G9 railpack | **Done** |
| t04 | [task-aibridge-req9-01-t04-story-gate](./task-aibridge-req9-01-t04-story-gate/README.md) | story AC gate | **PASS** |
| t05 | [task-aibridge-req9-01-t05-audit-g01-g03-backlog-verified-ac-sync](./task-aibridge-req9-01-t05-audit-g01-g03-backlog-verified-ac-sync/README.md) | G-01/G-03 backlog sync | **Done** · CLOSED |
| t06 | [task-aibridge-req9-01-t06-audit-g02-runbook-make-railpack-8080](./task-aibridge-req9-01-t06-audit-g02-runbook-make-railpack-8080/README.md) | G-02 runbook | **Done** · CLOSED |

### P5 disposition → P6 CLOSED (2026-09-26T12:20:13Z)

| Gap | Sev | Disposition | Task |
|-----|-----|-------------|------|
| G-01 | Low | TASKED → **CLOSED** (P6) | t05 Done |
| G-02 | Low | TASKED → **CLOSED** (P6) | t06 Done |
| G-03 | Info | TASKED → **CLOSED** (P6) | t05 Done |

**activation:** `run_mode=aibridge_req9_01_audit_20260926` · [p6](../../../../run-reports/run-summary-20260926-1220-story-aibridge-req9-01-p6.md) · next=P7
