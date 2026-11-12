# Story acceptance gate — STORY-AIBRIDGE-02-content-bundle-registry

- **Story:** Content bundle + Postgres registry + GC
- **Package:** `pkg-000002-20260912-epic-aibridge-01-story-02-content-bundle.yaml`
- **Result:** PASS
- **Date:** 2026-09-12T21:03:47Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Missing/mismatched artifacts → `/readyz` not ready. | PASS | t03 · `tests/test_readyz_bundle.py` |
| Redeploy with new bundle does not delete prior hash while a session still references it. | PASS | t04/t05 · `tests/test_session_pin.py` · `tests/test_bundle_gc.py` |
| Bundle row immutable after register; uniqueness on `bundle_hash`. | PASS | t02 · `tests/test_registry.py` |
| No GitHub fetch of instructions at request time. | PASS | t01 · `src/aibridge/content.py` local FS only |
| Session resume uses pinned `content_bundle_hash`. | PASS | t04 · `tests/test_session_pin.py` |

## Commands (live verification — P3)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
cd doge-ai-bridge && .venv/bin/pytest -q
# → 31 passed; verify ok 6 paths; date-check ok
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
