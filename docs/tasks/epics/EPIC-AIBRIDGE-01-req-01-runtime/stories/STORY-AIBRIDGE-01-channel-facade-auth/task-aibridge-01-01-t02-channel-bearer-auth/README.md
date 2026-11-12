# Task: implement — Channel Bearer auth + readiness equal-token fail

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md`  
**Parent story:** [`STORY-AIBRIDGE-01-channel-facade-auth.md`](../STORY-AIBRIDGE-01-channel-facade-auth.md)

## Purpose

Channel Bearer (`AIBRIDGE_CHANNEL_BEARER_TOKEN` + previous-token overlap per runbook); constant-time compare; 401 generic body on `/v1/channel/*`. When channel **and** gateway Bearer both configured and equal → readiness fail (REQ-01 §7 / §18).

**Out of this task:** turns/actions handlers (t03); event dedupe (t04).

## Code Facts (verified exists)

1. Auth mode / Bearer rules — REQ-01 §7; `docs/architecture/runtime/01-channel-facade.md`.
2. Rotation overlap SSOT — `doge-ai-bridge/docs/runbooks/channel-bearer-rotation.md`.
3. Channel OAS security scheme — `doge-ai-bridge/docs/openapi/aibridge-channel-v1.openapi.yaml` (`ChannelBearer`).
4. Product auth module path: **Unknown** until t01 scaffold.

## AC/DoD

- [x] Unauthenticated `/v1/channel/*` → 401 (generic body) — story AC #1.
- [x] Previous-token overlap accepted per `channel-bearer-rotation.md`.
- [x] Constant-time compare for Bearer tokens.
- [x] Equal channel/gateway Bearer when both configured → readiness fail — story AC #5.
- [x] `Skill declared: python-pro` present.

## Where to change

- Auth middleware/deps + env load on ASGI app from t01.
- `/readyz` integration for equal-token fail.

## Verification commands

```bash
# After implement: ASGI tests for 401 + equal-token readyz fail
rg -n 'AIBRIDGE_CHANNEL_BEARER|constant' doge-ai-bridge
```
