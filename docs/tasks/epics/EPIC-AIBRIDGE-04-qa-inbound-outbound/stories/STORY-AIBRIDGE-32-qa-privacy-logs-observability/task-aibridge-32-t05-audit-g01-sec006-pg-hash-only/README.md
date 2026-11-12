# Task: test — SEC-006 Postgres token hash-only (G-01)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_32_audit_20260917`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-32-qa-privacy-logs-observability-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-32-qa-privacy-logs-observability.md`](../STORY-AIBRIDGE-32-qa-privacy-logs-observability.md)  
**P5 scaffold:** 2026-09-17T20:38:37Z  
**P6 closed:** 2026-09-17T20:42:29Z  
**Gate:** [acceptance-verification-task-aibridge-32-t05-audit-g01-sec006-pg-hash-only.md](./acceptance-verification-task-aibridge-32-t05-audit-g01-sec006-pg-hash-only.md) PASS  
**Maps:** SEC-006 · `PostgresActionTokenStore` hash-only

## Purpose

Strengthen SEC-006: exercise `PostgresActionTokenStore` (fake-conn / disposable-PG) so INSERT/select persist **token hash only** — raw absent from keys/params. Prefer test-first against existing `pg_runtime` seam (STORY-29 ACT-017 pattern); `@pytest.mark.skipif` when live PG absent + Preference A note. **No** product invent; **no** live Telegram / Railway invent. **P6 only** — do not implement in P5.

## AC/DoD

- [x] SEC-006 asserts via `PostgresActionTokenStore` (fake-conn or disposable PG / skipif).
- [x] Raw token absent from store keys/params; hash-only persist.
- [x] No live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/integration/test_privacy_observability.py` — **P6 Done**
- optionally assert-only vs `src/aibridge/pg_runtime.py`
