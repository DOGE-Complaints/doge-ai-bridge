# Migrations (story 09 SSOT)

Versioned SQL under this directory is the **sole production schema mechanism**.

```bash
# Apply (Python):
cd doge-ai-bridge && .venv/bin/python -c \
  "from aibridge.migrate import apply_migrations; print(apply_migrations('postgresql://…'))"
```

Do **not** rely on boot-time `CREATE TABLE IF NOT EXISTS` for production
(`PostgresBundleRegistry` / `PostgresSessionStore` default `ensure_schema=False`).

## Disposable Postgres for tests

```bash
./scripts/start-disposable-pg.sh   # creates .pgdata-test on port 55432
cd doge-ai-bridge && .venv/bin/pytest -q -m postgres
# or story 09 suite (auto-detects .pgdata-test):
.venv/bin/pytest -q tests/test_story_09_postgres_ssot.py
./scripts/stop-disposable-pg.sh
```
