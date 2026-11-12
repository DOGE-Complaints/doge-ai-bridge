# Task: consumers — gateway + readiness + R8 channel ≠ gateway token

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md`  
**Parent story:** [`STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md`](../STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md)  
**P1 scaffold:** 2026-09-26T12:38:37Z  
**Maps:** R1–R4 consumers · R8

## Purpose

Update `gateway.py` and `readiness.py` (and any other runtime refs) to new Settings attribute names. Keep `AIBRIDGE_CHANNEL_BEARER_TOKEN`; readiness fails closed if channel token equals `GATEWAY_SERVICE_API_TOKEN` (R8). Do not rename channel to `SERVICE_API_TOKEN`.

## AC/DoD

- [x] Consumers use `gateway_base_url` / `gateway_service_api_token` / `spa_base_url` (or equivalent new names).
- [x] Error/log strings do not treat removed DOGESTONIA_* env as primary.
- [x] R8: channel Keep; ≠ `GATEWAY_SERVICE_API_TOKEN` enforced in readiness.
- [x] No dual-read invent.
- [x] `Skill declared: python-pro` present.

## Where to change (P3)

- `src/aibridge/gateway.py`
- `src/aibridge/readiness.py`
- other runtime refs if grepped

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-req9-03-t02-gateway-readiness-consumers-r8.md` (create at P3 close)
