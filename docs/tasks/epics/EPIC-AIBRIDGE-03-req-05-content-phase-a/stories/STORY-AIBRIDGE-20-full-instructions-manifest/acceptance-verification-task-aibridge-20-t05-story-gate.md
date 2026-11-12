# Story acceptance gate — STORY-AIBRIDGE-20-full-instructions-manifest

| Field | Value |
|-------|-------|
| **Story** | STORY-AIBRIDGE-20-full-instructions-manifest |
| **Task** | task-aibridge-20-t05-story-gate |
| **Date** | 2026-09-16T12:32:27Z |
| **Result** | **PASS** |
| **Pkg** | pkg-000017-20260916-epic-aibridge-03-story-20-full-instructions-manifest.yaml |
| **pytest** | 5 passed (`tests/test_story_20_full_manifest.py`) |

## Target AC

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | REQ-05 §4.2 completeness: omit любого root-child (кроме manifest) = FAIL | **PASS** | `test_completeness_dir_set_equals_files_set` · `test_omit_would_fail_completeness` · 25 files |
| 2 | Layer order matches §4.2 | **PASS** | `test_layer_order_matches_req_05_4_2` vs REQ-05 §4.2 list |
| 3 | Pack JSON в `files[]`; `load_content_bundle` succeeds | **PASS** | `test_pack_json_in_files` · `test_load_content_bundle_full_dump` |

## Commands (live verification 2026-09-16T12:32:27Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
# ok 5 paths · ok date-check
cd doge-ai-bridge && DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 AIBRIDGE_DRY_RUN=1 \
  .venv/bin/pytest tests/test_story_20_full_manifest.py -q
# 5 passed
```

## Notes

- ADR-2: in-place `src/instructions/instructions.manifest.json`; loader schema **не** меняли.
- Channel OAS **не** в `files[]`.
