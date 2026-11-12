# Task: test — READY-013 migration /readyz Preference A (G-02)

**Status:** Done  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Wave:** `run_mode=aibridge_33_audit_20260917`  
**Gap:** G-02 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-33-qa-readiness-configuration-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-33-qa-readiness-configuration.md`](../STORY-AIBRIDGE-33-qa-readiness-configuration.md)  
**P5 scaffold:** 2026-09-17T21:04:00Z  
**P6 closed:** 2026-09-17T21:07:50Z  
**Gate:** [acceptance-verification-task-aibridge-33-t06-audit-g02-ready013-migration-readyz.md](./acceptance-verification-task-aibridge-33-t06-audit-g02-ready013-migration-readyz.md) PASS  
**Maps:** READY-013 · `migration_version_mismatch` · missing variants

## Purpose

Expand READY-013 beyond unit-only Preference A: fake-PG `/readyz` for `migration_version_mismatch` **and** assert `migrations_missing` / `migration_version_missing` via Preference A harness. Assert-only vs `readiness.py`. **No** product invent; **no** live Telegram / Railway invent.

## AC/DoD

- [x] READY-013 `/readyz` path covers `migration_version_mismatch` (Preference A).
- [x] Asserts for `migrations_missing` and `migration_version_missing`.
- [x] No live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: python-pro` present.

## Where to change

- `tests/contract/test_readyz_configuration.py` — **P6 Done**
- `ready-migration-mismatch.json` + `ready-migration-version-missing.json` + `ready-migrations-missing.json` (promote=copy) — **P6 Done**
- `src/aibridge/readiness.py` — assert-only (no product invent)
