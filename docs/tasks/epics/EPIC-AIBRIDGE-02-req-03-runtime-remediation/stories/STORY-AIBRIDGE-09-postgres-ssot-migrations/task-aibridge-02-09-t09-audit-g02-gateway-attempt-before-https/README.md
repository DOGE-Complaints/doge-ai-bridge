# Task: implement — GatewayAttempt commit-before-HTTPS (G-02)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_09_audit_20260913`  
**Gap:** G-02 (Medium) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-09-postgres-ssot-migrations-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-09-postgres-ssot-migrations.md`](../STORY-AIBRIDGE-09-postgres-ssot-migrations.md)  
**P5 scaffold:** 2026-09-13T15:29:22Z

## Purpose

REQ-03 §5.3: create gateway_attempt `executing` and commit **before** `execute_stash` HTTPS; store outcome after; unique revision constraint fail-closed.

## AC/DoD

- [x] `ConfirmationGuard.call_gateway` records attempt before HTTPS when GatewayAttemptStore wired.
- [x] Duplicate attempt for same revision fails closed (no second HTTPS).
- [x] Outcome updated after executor returns.
- [x] Unit/integration tests (RecordingGatewayTransport + disposable PG or fake).
- [x] `Skill declared: python-pro` present.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_gateway_attempt_before_https.py
```
