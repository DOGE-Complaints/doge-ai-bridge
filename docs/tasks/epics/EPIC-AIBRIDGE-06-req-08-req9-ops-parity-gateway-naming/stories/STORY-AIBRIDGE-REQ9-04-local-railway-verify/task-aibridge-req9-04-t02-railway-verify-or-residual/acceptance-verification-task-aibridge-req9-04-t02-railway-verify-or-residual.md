# Acceptance — task-aibridge-req9-04-t02-railway-verify-or-residual

| Field | Value |
|-------|-------|
| **Date** | 2026-09-26T13:03:46Z |
| **Result** | **PASS** (vars verify) · **residual Y** (remote `/health`/`/ready`) |

## Disk facts

| Claim | Evidence |
|-------|----------|
| Project/service id (not invent) | DOGEstonia / doge-ai-bridge / tallinn-demo — MCP+CLI |
| Target names present | `GATEWAY_BASE_URL` · `GATEWAY_SERVICE_API_TOKEN` · `SPA_BASE_URL` |
| Values = legacy (lens only) | equals `DOGESTONIA_INTAKE_*` / `DOGESTONIA_API_BEARER_*` / `DOGESTONIA_DRAFT_*` |
| Channel ≠ gateway S2S | `AIBRIDGE_CHANNEL_BEARER_TOKEN` ≠ `GATEWAY_SERVICE_API_TOKEN` |
| Remote `/healthz`/`/readyz` | 200 |
| Remote `/health`/`/ready` | **404** — residual (no invent SUCCESS) |
| Ops note | [`docs/ops/req-08-req9-verify-20260926.md`](../../../../../../ops/req-08-req9-verify-20260926.md) |
| Skill | test-master |
