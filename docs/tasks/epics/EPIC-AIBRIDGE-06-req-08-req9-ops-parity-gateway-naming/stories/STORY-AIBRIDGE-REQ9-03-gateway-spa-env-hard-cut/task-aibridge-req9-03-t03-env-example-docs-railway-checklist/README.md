# Task: docs — .env.example + runbooks/manuals + Railway names checklist

**Status:** Done  
**Skill declared:** python-pro · soft code-documenter  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md`  
**Parent story:** [`STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md`](../STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md)  
**P1 scaffold:** 2026-09-26T12:38:37Z  
**Maps:** template · docs · Railway names checklist (Lock C)

## Purpose

Hard-cut `.env.example` and operator docs/runbooks/manuals to `GATEWAY_BASE_URL`, `GATEWAY_SERVICE_API_TOKEN`, `SPA_BASE_URL`. Add Railway **target var names** checklist (+ pairing note vs gateway `SERVICE_API_TOKEN`). **Do not** require live Railway access or invent SUCCESS.

## AC/DoD

- [x] `.env.example` documents only target names (old removed as primary).
- [x] Runbooks/manuals citing old DOGESTONIA_* intake/bearer/redirect updated.
- [x] Railway names checklist present (story or linked runbook); proof deferred to 04.
- [x] No dual-read invent; no live Railway invent.
- [x] `Skill declared: python-pro` (+ soft code-documenter) present.

## Where to change (P3)

- `.env.example`
- `docs/runbooks/**` / manuals as needed
- checklist in story pipeline or linked ops doc

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-req9-03-t03-env-example-docs-railway-checklist.md` (create at P3 close)
