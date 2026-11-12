# Task: routes — GET /health and /ready aliases (G2)

**Status:** Done · P3 2026-09-26T12:27:23Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md`  
**Parent story:** [`STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md`](../STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md)  
**P1 scaffold:** 2026-09-26T12:24:30Z  
**P3 closed:** 2026-09-26T12:27:23Z  
**Maps:** REQ-08 G2 · tech-arch `01-runtime-and-probes.md`

## Purpose

Register `GET /health` and `GET /ready` in `src/aibridge/app.py` with the same semantics as existing `/healthz` / `/readyz`. Keep z-paths unless implement documents otherwise. Do **not** change readiness evaluation logic.

## AC/DoD

- [x] `GET /health` registered; same semantics as `/healthz`.
- [x] `GET /ready` registered; same semantics as `/readyz`.
- [x] Existing `/healthz` `/readyz` remain (unless documented otherwise).
- [x] No change to `evaluate_readiness` / readiness payload logic.
- [x] `Skill declared: python-pro` present.

## Where changed

- `src/aibridge/app.py` — stacked `@app.get("/health")` / `@app.get("/ready")`

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-req9-02-t01-health-ready-route-aliases.md`](./acceptance-verification-task-aibridge-req9-02-t01-health-ready-route-aliases.md)
