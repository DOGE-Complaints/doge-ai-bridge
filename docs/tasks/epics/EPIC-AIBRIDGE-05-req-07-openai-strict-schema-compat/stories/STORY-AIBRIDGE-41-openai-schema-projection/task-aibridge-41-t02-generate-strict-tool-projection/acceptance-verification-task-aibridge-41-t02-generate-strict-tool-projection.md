# Acceptance verification — task-aibridge-41-t02-generate-strict-tool-projection

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-24T11:00:27Z |
| **Story** | STORY-AIBRIDGE-41-openai-schema-projection |
| **Pkg** | pkg-000040 |
| **Wave** | P3 Execute |

## AC check

- [x] `generate_strict_tool` projects via t01 helper; post-assert clean; `strict: true`; name `postStoryDraftStash`
- [x] Pack/OAS disk unchanged; input pack deep-copied before inject
- [x] Fail-closed `ToolGenError` → deployment `tool_gen_failed:*` (`unsupported_keyword_remaining:*` / `openai_schema_projection_failed`)
- [x] Optional init log `_emit_projection_ready_event` swallows logging errors
- [x] `Skill declared: python-pro` present

## Evidence

```text
src/aibridge/tool_gen.py — generate_strict_tool projection + assert + emit
src/aibridge/deployment.py — existing tool_gen_failed:{exc} wrap (unchanged)
pytest …::test_generate_tool_no_unique_items_on_canonical_pack PASSED
pytest …::test_disk_pack_and_oas_unchanged PASSED
pytest …::test_fail_closed_when_projection_leaves_keyword PASSED
```
