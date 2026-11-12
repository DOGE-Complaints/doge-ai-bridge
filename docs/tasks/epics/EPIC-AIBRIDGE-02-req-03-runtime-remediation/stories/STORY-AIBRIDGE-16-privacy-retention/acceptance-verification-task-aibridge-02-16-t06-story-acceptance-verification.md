# Story acceptance gate — STORY-AIBRIDGE-16-privacy-retention

| Field | Value |
|-------|-------|
| **Story** | STORY-AIBRIDGE-16-privacy-retention |
| **Task** | task-aibridge-02-16-t06-story-acceptance-verification |
| **Date** | 2026-09-13T17:49:14Z |
| **Result** | **PASS** |
| **Pkg** | pkg-000014-20260913-epic-aibridge-02-story-16-privacy-retention.yaml |
| **pytest** | 177 passed / 38 skipped (full suite; story-16: 11 passed) |

## Target AC

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | §6.2 bullets proven with tests and/or ops evidence | **PASS** | `tests/test_story_16_privacy_retention.py`; TTL default 604800; minimize; purge; ops delete; privacy-pilot §2 |
| 2 | Consumed token remains non-usable after delete/expiry (tombstone OK) | **PASS** | `test_purge_expired_pending_keeps_consumed` · `test_ops_delete_covers_history_tokens_confirm` |
| 3 | Delete surface documented as ops-only once path decided — fail-closed until then | **PASS** | `python -m aibridge.ops_session_delete` + `AIBRIDGE_OPS_BEARER_TOKEN`; **no** channel OAS invent (`test_channel_openapi_has_no_session_delete_path`); privacy-pilot §2 |

## Notes

- HTTP channel delete path remains **Unknown** (INDEX decision).
- n8n retention checklist remains ops-separate (privacy-pilot §3).
