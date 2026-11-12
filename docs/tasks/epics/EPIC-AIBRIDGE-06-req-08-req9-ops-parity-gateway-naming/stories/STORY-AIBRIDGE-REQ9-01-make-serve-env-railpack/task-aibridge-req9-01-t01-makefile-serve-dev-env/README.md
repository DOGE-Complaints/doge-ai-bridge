# Task: ops — Makefile serve/dev + required .env (G1/G8)

**Status:** Done · P3 2026-09-26T12:14:54Z  
**Skill declared:** python-pro · soft devops-engineer  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md`  
**Parent story:** [`STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md`](../STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md)  
**P1 scaffold:** 2026-09-26T12:12:53Z  
**P3 closed:** 2026-09-26T12:14:54Z  
**Maps:** REQ-08 G1 · G8 · tech-arch `01-runtime-and-probes.md`

## Purpose

NEW `Makefile` with `serve` / `dev` targets: uvicorn `aibridge.app:app` on `:8080` with required `.env` load (`set -a && . ./.env && set +a`, G8).

## AC/DoD

- [x] `Makefile` exists with `serve` and `dev` → uvicorn `aibridge.app:app` `:8080`.
- [x] G8: `.env` required via `set -a && . ./.env && set +a` on Make serve/dev.
- [x] No product invent beyond Makefile targets; no probe/env hard-cut (02/03).
- [x] `Skill declared: python-pro` (+ soft devops-engineer) present.

## Where changed

- `Makefile` (NEW)

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-req9-01-t01-makefile-serve-dev-env.md`](./acceptance-verification-task-aibridge-req9-01-t01-makefile-serve-dev-env.md)
