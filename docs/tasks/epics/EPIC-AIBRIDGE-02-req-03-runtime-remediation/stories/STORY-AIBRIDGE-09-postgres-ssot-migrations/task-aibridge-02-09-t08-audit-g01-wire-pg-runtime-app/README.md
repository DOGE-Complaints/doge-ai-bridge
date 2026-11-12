# Task: implement — wire pg_runtime into create_app (G-01)

**Status:** Done  
**Skill declared:** postgres-pro  
**Wave:** `run_mode=aibridge_09_audit_20260913`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-09-postgres-ssot-migrations-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-09-postgres-ssot-migrations.md`](../STORY-AIBRIDGE-09-postgres-ssot-migrations.md)  
**P5 scaffold:** 2026-09-13T15:29:22Z

## Purpose

When `DATABASE_URL=postgresql://…`, default ASGI must use PostgresEventDedupeStore + PG tokens/confirm stores (not silent in-memory EventDedupeStore / ActionTokenStore).

## AC/DoD

- [x] `create_app` with postgres URL wires PG dedupe without manual inject.
- [x] ConfirmationGuard gets PG token store (+ confirm persist) when not allow_memory / on postgres URL.
- [x] Fail-closed when `AIBRIDGE_ALLOW_MEMORY_STORES=false` and URL not postgres.
- [x] Integration test with disposable PG / TestClient.
- [x] `Skill declared: postgres-pro` present.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_app_pg_runtime_wire.py
```
