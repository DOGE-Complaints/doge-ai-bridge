# Acceptance — task-aibridge-req9-03-t02-gateway-readiness-consumers-r8

| Field | Value |
|-------|-------|
| **Date** | 2026-09-26T12:46:12Z |
| **Result** | **Done** |

## Disk facts

| Claim | Evidence |
|-------|----------|
| readiness uses `gateway_service_api_token` | `src/aibridge/readiness.py` |
| executor uses new attrs | `src/aibridge/gateway.py` `default_executor_from_settings` |
| Error string primary | `GATEWAY_SERVICE_API_TOKEN required for gateway` |
| R8 channel Keep ≠ gateway | `channel_gateway_bearers_equal()` + readiness `channel_gateway_bearer_equal` |
| No dual-read invent | no getattr to removed DOGESTONIA_* names |
