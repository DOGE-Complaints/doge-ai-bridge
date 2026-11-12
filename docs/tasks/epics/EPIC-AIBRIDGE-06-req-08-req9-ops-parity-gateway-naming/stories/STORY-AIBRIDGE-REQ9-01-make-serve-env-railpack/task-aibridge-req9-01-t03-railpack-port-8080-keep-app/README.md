# Task: ops — railpack PORT 8080 + keep aibridge.app:app (G3/G9)

**Status:** Done · P3 2026-09-26T12:14:54Z  
**Skill declared:** python-pro · soft devops-engineer  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md`  
**Parent story:** [`STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md`](../STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md)  
**P1 scaffold:** 2026-09-26T12:12:53Z  
**P3 closed:** 2026-09-26T12:14:54Z  
**Maps:** REQ-08 G3 · G9 · tech-arch `01-runtime-and-probes.md`

## Purpose

Change `railpack.json` startCommand fallback to `${PORT:-8080}` (G3). Keep uvicorn app string `aibridge.app:app` (G9). `__main__.py` already uses `aibridge.app:app` — no change.

## AC/DoD

- [x] `railpack.json` uses `${PORT:-8080}`.
- [x] G9: `aibridge.app:app` retained in railpack / `__main__.py`.
- [x] No invent Railway deploy SUCCESS; out of scope 02/03/04.
- [x] `Skill declared: python-pro` (+ soft devops-engineer) present.

## Where changed

- `railpack.json` (PORT fallback 8000 → 8080)
- `src/aibridge/__main__.py` — unchanged (already G9)

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-req9-01-t03-railpack-port-8080-keep-app.md`](./acceptance-verification-task-aibridge-req9-01-t03-railpack-port-8080-keep-app.md)
