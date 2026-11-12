# Task: test — READY-001 migrated PostgreSQL path (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Wave:** `run_mode=aibridge_33_audit_20260917`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-33-qa-readiness-configuration-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-33-qa-readiness-configuration.md`](../STORY-AIBRIDGE-33-qa-readiness-configuration.md)  
**P5 scaffold:** 2026-09-17T21:04:00Z  
**P6 closed:** 2026-09-17T21:07:50Z  
**Gate:** [acceptance-verification-task-aibridge-33-t05-audit-g01-ready001-migrated-pg.md](./acceptance-verification-task-aibridge-33-t05-audit-g01-ready001-migrated-pg.md) PASS  
**Maps:** READY-001 · migrated PG / Preference A stand-in

## Purpose

Strengthen READY-001: disposable-PG migrate + `/readyz` 200 when `DISPOSABLE_URL` present; else Preference A fake-conn returning expected migration version → ready via `evaluate_readiness`/`/readyz` with injected memory stores; align fixture notes / TRACEABILITY stand-in. Prefer test-first against existing `readiness._postgres_migration_ok` / `migrate.list_migration_files`. **No** product invent; **no** live Telegram / Railway SUCCESS invent.

## AC/DoD

- [x] READY-001 asserts migrated-PG (or Preference A) path to 200 `ready` beyond memory-only stand-in.
- [x] Fixture notes / TRACEABILITY stand-in aligned when Preference A used.
- [x] No live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: python-pro` present.

## Where to change

- `tests/contract/test_readyz_configuration.py` — **P6 Done**
- `tests/fixtures/settings/ready-ok.json` + `ready-ok-migrated-pg.json` (promote=copy) — **P6 Done**
- TRACEABILITY READY-001 note — **P6 Done**
