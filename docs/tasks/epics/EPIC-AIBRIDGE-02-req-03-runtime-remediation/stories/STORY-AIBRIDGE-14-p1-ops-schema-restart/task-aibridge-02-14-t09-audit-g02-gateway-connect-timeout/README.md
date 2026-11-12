# Task: fix — wire AIBRIDGE_HTTP_CONNECT_TIMEOUT_MS into gateway httpx (G-02)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_14_audit_20260913`  
**Gap:** G-02 (Medium) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-14-p1-ops-schema-restart-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-14-p1-ops-schema-restart.md`](../STORY-AIBRIDGE-14-p1-ops-schema-restart.md)  
**P5 scaffold:** 2026-09-13T17:18:05Z  
**P6 Done:** 2026-09-13T17:23:30Z  
**Maps:** R3-P1-06 · REQ-01 §17 gateway connect

## Purpose

Apply Settings `AIBRIDGE_HTTP_CONNECT_TIMEOUT_MS` to gateway HTTPS connect (not only OpenAI client / total timeout).

## AC/DoD

- [x] `default_executor_from_settings` / `HttpxGatewayTransport` use connect timeout from Settings (httpx.Timeout or equivalent).
- [x] Unit test asserts transport/executor receives connect timeout (not only Settings field).
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/gateway.py`, `tests/test_story_14_audit_gaps.py`

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "connect_timeout or story_14_audit or gateway" --maxfail=10
```
