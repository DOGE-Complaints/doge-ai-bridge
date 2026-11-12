# Task: tests — fixtures hard cut to GATEWAY_* / SPA_BASE_URL

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md`  
**Parent story:** [`STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md`](../STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md)  
**P1 scaffold:** 2026-09-26T12:38:37Z  
**Maps:** R1 R2 R4 tests · Lock A

## Purpose

Update `tests/**` env fixtures and assertions to new primary names. Remove reliance on old DOGESTONIA_* intake/bearer/redirect as primary. Cover R8 inequality where readiness tests already assert channel ≠ gateway token.

## AC/DoD

- [x] Test fixtures use `GATEWAY_BASE_URL` / `GATEWAY_SERVICE_API_TOKEN` / `SPA_BASE_URL` (or Settings kwargs matching new fields).
- [x] No primary old env names left in product test paths for these three.
- [x] Suite green for touched probe/settings/gateway/readiness tests.
- [x] `Skill declared: python-pro` present.

## Where to change (P3)

- `tests/**` (conftest, settings helpers, readiness/gateway suites)

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-req9-03-t04-tests-fixtures-hard-cut.md` (create at P3 close)
