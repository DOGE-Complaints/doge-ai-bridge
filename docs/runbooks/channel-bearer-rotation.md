# Runbook — channel Bearer rotation

**Service:** `doge-ai-bridge`  
**Related REQ:** [REQ-01 §7 AIB-AUTH-01](../requirements/REQ-01-doge-ai-bridge-runtime.md)  
**Architecture:** [runtime/00-overview.md](../architecture/runtime/00-overview.md) · [04-ops-security.md](../architecture/runtime/04-ops-security.md)  
**Also document in:** Operator README (REQ-01 deliverable §22)  
**As-of:** 2026-09-12

Channel Bearer (`AIBRIDGE_CHANNEL_BEARER_TOKEN`) authenticates **n8n → aibridge**. It must stay distinct from the gateway Bearer.

## Safe sequence

1. **Generate** a new high-entropy token (CSPRNG; ≥256 bits entropy per REQ).
2. **Overlap:** set on aibridge:
   - `AIBRIDGE_CHANNEL_BEARER_TOKEN` = **new** token  
   - `AIBRIDGE_CHANNEL_PREVIOUS_BEARER_TOKEN` = **old** token  
   Redeploy or refresh env so both are accepted.
3. **Update n8n** Header Auth credential to the **new** token (do not put gateway Bearer here).
4. **Live check:** from n8n, `POST /v1/channel/turns` over Railway private networking → expect 200 (or bounded business response), not 401.
5. **Drop previous:** clear `AIBRIDGE_CHANNEL_PREVIOUS_BEARER_TOKEN`; redeploy/refresh.
6. **Verify:** `/readyz` ready; logs show no auth spike; optional second live call still succeeds; old token must get 401.

## Do not

- Rotate gateway and channel tokens in one blind step without separate verification.
- Log or paste raw Bearer values into tickets/chat.
- Expose façade or `/metrics` on a public URL for this pilot.
