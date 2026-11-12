# Task: config — Settings R1/R2/R4 hard cut (Lock A)

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md`  
**Parent story:** [`STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md`](../STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md)  
**P1 scaffold:** 2026-09-26T12:38:37Z  
**Maps:** R1 · R2 · R4 · Lock A no dual-read

## Purpose

Hard-cut `src/aibridge/config.py` Settings: rename fields and `validation_alias` to `GATEWAY_BASE_URL` / `GATEWAY_SERVICE_API_TOKEN` / `SPA_BASE_URL` (and Python `gateway_*` / `spa_base_url`). Remove old DOGESTONIA_* aliases and helpers. **No** dual-read.

## AC/DoD

- [x] R1: intake URL → `GATEWAY_BASE_URL` / `gateway_base_url` only.
- [x] R2: API bearer → `GATEWAY_SERVICE_API_TOKEN` / `gateway_service_api_token` only.
- [x] R4: draft redirect → `SPA_BASE_URL` / `spa_base_url` only.
- [x] No dual-read / soft fallback to removed names.
- [x] `Skill declared: python-pro` present.

## Where to change (P3)

- `src/aibridge/config.py`

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-req9-03-t01-config-settings-hard-cut.md` (create at P3 close)
