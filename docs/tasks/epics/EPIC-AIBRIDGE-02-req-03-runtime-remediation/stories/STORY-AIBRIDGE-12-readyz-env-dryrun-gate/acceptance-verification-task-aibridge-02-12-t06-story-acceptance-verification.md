# Story acceptance gate — STORY-AIBRIDGE-12-readyz-env-dryrun-gate

- **Story:** Env + `/readyz` + 500 + dry-run gate
- **Package:** `pkg-000010-20260913-epic-aibridge-02-story-12-readyz-env-dryrun-gate.yaml`
- **Result:** PASS
- **Date:** 2026-09-13T16:22:32Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| §5.5 and §5.6 satisfied. | PASS | `readiness.py` strict checks; `config.py` TTL/timeouts/log/rate/budgets + `DOGESTONIA_API_BASE_URL`; `.env.example` parity; tests `test_story_12_readyz_env.py` |
| Dry-run readiness gate until story 14 P1-03 complete. | PASS | `dry_run_required` when `AIBRIDGE_DRY_RUN=false` unless `AIBRIDGE_SCHEMA_VALIDATION_COMPLETE=true` |
| Unhandled errors → bounded channel JSON 500 conforming to OpenAPI. | PASS | `Exception` handler on `/v1/channel/*` → `ChannelErrorBody` `internal_error`; no stack/secrets |

## Commands (live verification — 2026-09-13T16:22:32Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
cd doge-ai-bridge && .venv/bin/pytest -q
# → ok 6 paths; ok date-check; 136 passed, 15 skipped
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
