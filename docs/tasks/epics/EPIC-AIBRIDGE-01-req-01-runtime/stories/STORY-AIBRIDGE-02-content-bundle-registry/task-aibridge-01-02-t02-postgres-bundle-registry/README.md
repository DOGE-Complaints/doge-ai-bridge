# Task: implement — Postgres content_bundle register-once

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-02-content-bundle-registry.md`  
**Parent story:** [`STORY-AIBRIDGE-02-content-bundle-registry.md`](../STORY-AIBRIDGE-02-content-bundle-registry.md)

## Purpose

DB model/migration for `content_bundle` (unique `bundle_hash`, hashes, source_commit, verified_at, immutable payload/components per `02-content-packaging.md` §4); **register-once** after startup verify.

**Out of this task:** GC (t05); full interview session engine beyond FK prep for t04; Railway Volume store.

## Code Facts (verified exists — post P3 + P6 t07)

1. Registry logical model — `docs/architecture/runtime/02-content-packaging.md` §4.
2. Offline: `MemoryBundleRegistry` / `SqliteBundleRegistry` — `src/aibridge/registry.py`; tests `tests/test_registry.py`.
3. Production DSN: `PostgresBundleRegistry` / `PostgresSessionStore` via `postgresql://` (`psycopg`) — wired in P6 **t07** (`task-aibridge-01-02-t07-audit-g01-postgres-adapter`).
4. Content hashes/pin from t01 — `src/aibridge/content.py`.

## AC/DoD

- [x] Uniqueness on `bundle_hash` (AC #3) — Memory/Sqlite (P3) + Postgres adapter (P6 t07).
- [x] Row immutable after register; second register same hash is no-op/safe.
- [x] Register-once after startup verify (`deployment.py`).
- [x] `Skill declared: python-pro` present.

## Where to change

- `src/aibridge/registry.py`, `sessions.py` (P3 + t07).
- DB DSN via `DATABASE_URL`.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# optional live: DATABASE_URL=postgresql://… pytest -q -m postgres
```
