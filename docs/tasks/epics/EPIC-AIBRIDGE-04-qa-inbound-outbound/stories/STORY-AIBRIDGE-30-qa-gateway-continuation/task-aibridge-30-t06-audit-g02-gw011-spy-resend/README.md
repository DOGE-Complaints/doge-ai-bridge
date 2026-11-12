# Task: test — GW-011 spy fields + second Send block (G-02)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_30_audit_20260917`  
**Gap:** G-02 (Low) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-30-qa-gateway-continuation-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-30-qa-gateway-continuation.md`](../STORY-AIBRIDGE-30-qa-gateway-continuation.md)  
**P5 scaffold:** 2026-09-17T19:56:48Z  
**P6 closed:** 2026-09-17T19:59:20Z  
**Gate:** [acceptance-verification-task-aibridge-30-t06-audit-g02-gw011-spy-resend.md](./acceptance-verification-task-aibridge-30-t06-audit-g02-gw011-spy-resend.md) PASS  

## Purpose

Strengthen GW-011 hygiene: assert spy `gw-timeout-unknown` fields `http_posted` / `send_blocked_same_revision`; second Send blocked; optional ambiguous disconnect path. **No** live Telegram / Railway invent.

## AC/DoD

- [x] Spy fields `http_posted` / `send_blocked_same_revision` asserted from envelope.
- [x] Second Send attempt for same revision blocked (no auto-resend).
- [x] Optional: ambiguous disconnect exception path (`ConnectionError` → unknown + http_posted).
- [x] No live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/integration/test_gateway_continuation.py` — **P6 Done**
