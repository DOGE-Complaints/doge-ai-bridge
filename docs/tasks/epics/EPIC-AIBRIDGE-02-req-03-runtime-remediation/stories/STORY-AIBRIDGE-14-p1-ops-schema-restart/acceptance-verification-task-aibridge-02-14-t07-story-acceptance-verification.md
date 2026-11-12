# Story acceptance gate — STORY-AIBRIDGE-14-p1-ops-schema-restart

- **Story:** P1 ops + full schema + restart tests
- **Package:** `pkg-000012-20260913-epic-aibridge-02-story-14-p1-ops-schema-restart.yaml`
- **Result:** PASS
- **Date:** 2026-09-13T17:14:26Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| R3-P1-01,02,03,04,06,07 closed with tests/evidence. | PASS | t01–t06 · `tests/test_story_14_ops_schema_restart.py` · Dockerfile present |
| `AIBRIDGE_DRY_RUN=false` may pass readiness only after full schema validation is proven. | PASS | enum/const/bounds in `request_assembly.py` · `test_story_14_readyz_dry_run_false_after_schema_complete` |
| Restart/race tests cover AC #7–#8. | PASS | recover_all / pending-confirm / timeout→unknown_outcome tests |

## Commands (live verification — 2026-09-13T17:14:26Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
cd doge-ai-bridge && ./scripts/start-disposable-pg.sh && .venv/bin/pytest -q
# → ok 7 paths; ok date-check; 191 passed, 1 skipped
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
