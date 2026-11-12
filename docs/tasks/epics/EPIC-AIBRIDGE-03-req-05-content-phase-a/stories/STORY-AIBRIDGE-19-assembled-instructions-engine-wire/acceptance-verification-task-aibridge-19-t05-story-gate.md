# Story acceptance gate — STORY-AIBRIDGE-19-assembled-instructions-engine-wire

| Field | Value |
|-------|-------|
| **Story** | STORY-AIBRIDGE-19-assembled-instructions-engine-wire |
| **Task** | task-aibridge-19-t05-story-gate |
| **Date** | 2026-09-16T12:10:09Z |
| **Result** | **PASS** |
| **Pkg** | pkg-000016-20260916-epic-aibridge-03-story-19-assembled-instructions-engine-wire.yaml |
| **pytest** | 7 passed (`tests/test_story_19_engine_wire.py`) |

## Target AC

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | REQ-05 §4.1: `prompt_channel=prefix`; assembled in stable prefix; XOR (no API `instructions=`) | **PASS** | `test_create_app_wires_assembled_into_engine_and_prefix_xor` · `test_helper_sets_prefix_instructions_from_ready_deploy` |
| 2 | Strict tool from deploy on interview path when schema id/version | **PASS** | `test_create_app_wires_strict_tool_when_schema_configured` · `test_helper_maps_strict_tool_and_pack_id` |
| 3 | No silent empty instructions when content_configured + empty/not-ready | **PASS** | `test_helper_fail_closed_empty_assembled` · `test_readyz_fails_when_assembled_empty_after_helper` |

## Commands (live verification 2026-09-16T12:10:09Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
# ok 5 paths · ok date-check
cd doge-ai-bridge && DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 AIBRIDGE_DRY_RUN=1 \
  .venv/bin/pytest tests/test_story_19_engine_wire.py -q
# 7 passed
```

## Notes

- ADR-1: `_apply_deployment_to_engine` after `deployment_bundle` assign — **no** full `create_app` reorder.
- Empty assembled → `deployment.error=assembled_instructions_empty` → `/readyz` 503; `/healthz` stays up.
