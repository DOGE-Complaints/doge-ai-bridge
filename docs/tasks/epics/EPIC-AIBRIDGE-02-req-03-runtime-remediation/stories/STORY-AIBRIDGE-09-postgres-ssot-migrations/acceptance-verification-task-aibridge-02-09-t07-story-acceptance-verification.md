# Story acceptance gate — STORY-AIBRIDGE-09-postgres-ssot-migrations

- **Story:** Postgres SSOT + migrations + concurrency
- **Package:** `pkg-000007-20260913-epic-aibridge-02-story-09-postgres-ssot.yaml`
- **Result:** PASS
- **Date:** 2026-09-13T15:25:46Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Versioned migrations applied; boot schema-only path not production-acceptable. | PASS | `migrations/0001_ssot_core.sql` + `migrate.apply_migrations`; PG stores default `ensure_schema=False`; `test_migrations_files_exist_and_apply` |
| Constraints above enforced; failed txn does not advance history/FSM. | PASS | unique event_dedupe / action_token / session_call / gateway_attempt; `test_gateway_attempt_unique_per_revision`, `test_session_call_unique` |
| Transport replay after restart returns previously stored HTTP status + body (REQ-03 AC #2). | PASS | `PostgresEventDedupeStore`; `test_event_dedupe_unique_and_replay_after_reconnect` |
| Disposable Postgres integration + concurrency race tests pass (constraints win). | PASS | `scripts/start-disposable-pg.sh` + `.pgdata-test`; `test_turn_lock_concurrency_one_wins`, `test_event_dedupe_concurrency_constraints_win` |
| Production path has no silent memory fallback for dedupe/session/confirm/tokens/history. | PASS | `assert_no_silent_memory_fallback` / `AIBRIDGE_ALLOW_MEMORY_STORES`; `test_no_silent_memory_fallback_policy`; PG repos in `pg_runtime.py` |

## Commands (live verification 2026-09-13T15:25:46Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
cd doge-ai-bridge && ./scripts/start-disposable-pg.sh && .venv/bin/pytest -q
# → 109 passed, 1 skipped
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
