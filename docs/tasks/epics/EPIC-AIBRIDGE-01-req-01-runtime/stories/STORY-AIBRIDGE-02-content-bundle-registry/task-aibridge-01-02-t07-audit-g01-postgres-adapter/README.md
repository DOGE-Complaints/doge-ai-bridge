# Task: fix — wire PostgreSQL content_bundle / session adapter (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_02_audit_20260912`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-12  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-02-content-bundle-registry-20260912.md`  
**Parent story:** [`STORY-AIBRIDGE-02-content-bundle-registry.md`](../STORY-AIBRIDGE-02-content-bundle-registry.md)  
**P5 scaffold:** 2026-09-12T21:09:54Z  
**P6 Done:** 2026-09-12T21:13:50Z

## Purpose

Wire Postgres adapter for `open_bundle_registry` / `open_session_store` so `postgresql://` / `postgres://` matches arch `02-content-packaging.md` §4 logical model (register-once, unique `bundle_hash`, session FK). Keep Memory/Sqlite for offline tests. Fail-closed until adapter ready (preserve `_init_stores` behavior for unknown/broken DSN).

**Out of this task:** Railway Volume store; REQ-02 object storage; inventing absolute CI paths; GC lifecycle hook (G-02); Responses session engine (03); reopening story AC #1–#5 as failed (residual Medium only).

## Code Facts (verified exists — post P6)

1. `PostgresBundleRegistry` / `PostgresSessionStore` — `src/aibridge/registry.py`, `sessions.py`; `open_*` routes `postgresql://` / `postgres://`.
2. Dep: `psycopg[binary]>=3.1.0` in `pyproject.toml`.
3. Offline Memory/Sqlite unchanged; tests `tests/test_registry.py` etc.
4. Adapter unit tests with fake conn — `tests/test_postgres_adapter.py`; live `@pytest.mark.postgres` skips without `DATABASE_URL`.
5. Fail-closed: `_init_stores` catches `ImportError`/`OSError` → `database_adapter_unavailable` (no silent Memory for intended PG without surfacing error).

## AC/DoD

- [x] `postgresql://` / `postgres://` opens working BundleRegistry + SessionStore (register-once, unique hash, resume pin) — mocked unit + optional live mark.
- [x] Offline Memory/Sqlite path unchanged (34 passed + 1 skipped @ P6).
- [x] Integration: `@pytest.mark.postgres` skips when no live `DATABASE_URL` (no invented Railway credentials).
- [x] Fail-closed on missing driver / OS connect errors via `_init_stores`.
- [x] Acceptance-verification + evidence; gate Date live.
- [x] `Skill declared: python-pro` present.

## Where to change

- `doge-ai-bridge/src/aibridge/registry.py`
- `doge-ai-bridge/src/aibridge/sessions.py`
- `doge-ai-bridge/src/aibridge/app.py`
- `doge-ai-bridge/pyproject.toml`
- `doge-ai-bridge/tests/test_postgres_adapter.py`

## Verification commands (P6)

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# optional: DATABASE_URL=postgresql://… pytest -q -m postgres
```
