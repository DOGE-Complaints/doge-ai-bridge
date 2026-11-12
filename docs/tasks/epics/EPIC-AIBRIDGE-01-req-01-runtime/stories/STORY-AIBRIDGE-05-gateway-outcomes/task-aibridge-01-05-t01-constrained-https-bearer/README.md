# Task: implement — constrained HTTPS + gateway Bearer isolation

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-05-gateway-outcomes.md`  
**P3 Done:** 2026-09-12T21:54:48Z
**Parent story:** [`STORY-AIBRIDGE-05-gateway-outcomes.md`](../STORY-AIBRIDGE-05-gateway-outcomes.md)  
**P5 scaffold:** n/a (P1.3)

## Purpose

Constrained HTTPS to configured gateway origin; TLS verify; no redirects; gateway Bearer only in executor from `DOGESTONIA_API_BEARER_TOKEN` — never channel Bearer (AC #1 / AIB-HTTP-01/02).

**Out of this task:** inventing gateway lookup API; SPA E2E (06); dry-run flag (t04).

## Code Facts (verified exists)

1. Arch gateway rules — `docs/architecture/runtime/03-confirm-gateway.md` §5.
2. Settings aliases — `src/aibridge/config.py` (`AIBRIDGE_CHANNEL_BEARER_TOKEN`, `DOGESTONIA_API_BEARER_TOKEN`).
3. Send call site only — `confirm.py` `call_gateway` (no HTTP client).
4. No `GatewayExecutor` module under `src/aibridge/`.

## AC/DoD

- [x] Executor posts only to configured HTTPS origin; TLS verify on; redirects denied.
- [x] Authorization header uses gateway Bearer only; channel Bearer never passed to gateway.
- [x] Wired from Send-authorized path (story 04 gate preserved).
- [x] `Skill declared: python-pro` present.

## Where to change

- New module under `src/aibridge/` (e.g. `gateway.py` / `gateway_executor.py`).
- `config.py`, `confirm.py` call site.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# unit: channel bearer not used; wrong host / redirect rejected
```
