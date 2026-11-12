# Task: Railway — verify vars or record residual (Lock C)

**Status:** Done · 2026-09-26T13:03:46Z  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-04-local-railway-verify.md`  
**Parent story:** [`STORY-AIBRIDGE-REQ9-04-local-railway-verify.md`](../STORY-AIBRIDGE-REQ9-04-local-railway-verify.md)  
**P1 scaffold:** 2026-09-26T12:58:34Z  
**Maps:** Railway · Lock C · REQ §6

## Purpose

Apply/verify Railway target var names+values from story 03 checklist **or** record explicit residual if project/service id Unknown / live access absent. **Do not invent SUCCESS.**

## AC/DoD

- [x] Railway verify evidence **or** residual note with reason (Unknown id / no access).
- [x] No invent project/service id or remote smoke PASS without disk/MCP fact.
- [x] Target names: `GATEWAY_BASE_URL` / `GATEWAY_SERVICE_API_TOKEN` / `SPA_BASE_URL`; channel Keep ≠ gateway S2S.
- [x] `Skill declared: test-master` present.

## Where to change (P3)

- Railway MCP/CLI when available; else residual in ops evidence (t03).

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-req9-04-t02-railway-verify-or-residual.md` (create at P3 close)
