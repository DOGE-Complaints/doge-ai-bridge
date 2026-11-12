# Task: implement — wire GatewayExecutor into create_app (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_05_audit_20260912`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-12  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-05-gateway-outcomes-20260912.md`  
**Parent story:** [`STORY-AIBRIDGE-05-gateway-outcomes.md`](../STORY-AIBRIDGE-05-gateway-outcomes.md)  
**P5 scaffold:** 2026-09-12T21:58:17Z  
**P6 Done:** 2026-09-12T21:59:49Z

## Purpose

Wire `GatewayExecutor` from settings into `ConfirmationGuard` at `create_app` so default ASGI Send path is not story-04 counter-only.

## Code Facts (verified exists — post P6)

1. `create_app` → `ConfirmationGuard(executor=default_executor_from_settings(cfg0))` — `app.py`.
2. Tests — `tests/test_app_gateway_wire.py`.

## AC/DoD

- [x] Default `create_app` builds guard with executor from settings.
- [x] TestClient path exercises executor without manual inject (dry-run).
- [x] Legacy counter-only only when caller explicitly passes guard without executor.
- [x] `Skill declared: python-pro` present.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_app_gateway_wire.py
```
