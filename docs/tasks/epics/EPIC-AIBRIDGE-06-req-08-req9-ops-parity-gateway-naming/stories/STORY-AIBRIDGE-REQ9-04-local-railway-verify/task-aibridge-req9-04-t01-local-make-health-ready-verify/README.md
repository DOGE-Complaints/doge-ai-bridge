# Task: local — make serve + /health /ready + GATEWAY_* template

**Status:** Done · 2026-09-26T13:03:46Z  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-04-local-railway-verify.md`  
**Parent story:** [`STORY-AIBRIDGE-REQ9-04-local-railway-verify.md`](../STORY-AIBRIDGE-REQ9-04-local-railway-verify.md)  
**P1 scaffold:** 2026-09-26T12:58:34Z  
**Maps:** Local · tech-arch 04

## Purpose

Local verify: `make serve`/`dev` on 8080; curl `/health` + `/ready`; config/template show `GATEWAY_BASE_URL` / `GATEWAY_SERVICE_API_TOKEN` / `SPA_BASE_URL`. Evidence without secrets.

## AC/DoD

- [x] Process up on 8080 via Make.
- [x] curl `/health` and `/ready` recorded (status + minimal body, no secrets).
- [x] `.env.example` / Settings aliases show target GATEWAY_*/SPA names.
- [x] `Skill declared: test-master` present.

## Where to change (P3)

- Runtime verify only (no product invent); optional evidence excerpt in ops note (t03).

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-req9-04-t01-local-make-health-ready-verify.md` (create at P3 close)
