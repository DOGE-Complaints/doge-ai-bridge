# Acceptance — task-aibridge-req9-03-t01-config-settings-hard-cut

| Field | Value |
|-------|-------|
| **Date** | 2026-09-26T12:46:12Z |
| **Result** | **Done** |

## Disk facts

| Claim | Evidence |
|-------|----------|
| R1 `GATEWAY_BASE_URL` / `gateway_base_url` | `src/aibridge/config.py` Field + `validation_alias` |
| R2 `GATEWAY_SERVICE_API_TOKEN` / `gateway_service_api_token` | same |
| R4 `SPA_BASE_URL` / `spa_base_url` | same |
| No dual-read | no `DOGESTONIA_INTAKE_*` / `API_BEARER` / `DRAFT_REDIRECT` aliases in `config.py` |
| Helpers | `intake_base_url()` / `draft_redirect_base_ok()` / `channel_gateway_bearers_equal()` read new fields |
