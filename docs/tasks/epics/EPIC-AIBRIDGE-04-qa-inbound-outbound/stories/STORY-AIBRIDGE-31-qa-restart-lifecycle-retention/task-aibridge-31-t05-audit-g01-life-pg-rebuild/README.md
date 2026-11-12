# Task: test — LIFE PG rebuild (G-01)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_31_audit_20260917`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-31-qa-restart-lifecycle-retention-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md`](../STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md)  
**P5 scaffold:** 2026-09-17T20:17:44Z  
**P6 closed:** 2026-09-17T20:19:43Z  
**Gate:** [acceptance-verification-task-aibridge-31-t05-audit-g01-life-pg-rebuild.md](./acceptance-verification-task-aibridge-31-t05-audit-g01-life-pg-rebuild.md) PASS  
**Maps:** LIFE-002 · LIFE-003 · LIFE-004 · harness disposable PG + `rebuild_app_same_pg`

## Purpose

Strengthen LIFE-002/003/004 restart path against PostgreSQL SSOT: disposable-PG (or `@pytest.mark.skipif` when unavailable) via `rebuild_app_same_pg` + `PostgresConfirmSessionStore` / `PostgresActionTokenStore` (/history). Assert session restore, pending token usable, consumed stays consumed, zero duplicate gateway. Preference A applied: **test-first** against existing PG store seams (fake conn). Live `rebuild_app_same_pg` skipif when disposable PG absent. **No** live Telegram / Railway invent.

## AC/DoD

- [x] LIFE-002/003/004 exercised via `rebuild_app_same_pg` + PG confirm/token stores (or skipif + Preference A fake-conn seams).
- [x] Restore / pending usable / consumed stays consumed; no duplicate gateway side effect.
- [x] No live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/integration/test_lifecycle_retention.py` — **P6 Done**
- `tests/story13_e2e_helpers.py` · optionally assert-only vs `src/aibridge/pg_runtime.py`
