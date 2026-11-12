# Run summary — STORY-AIBRIDGE-13 P6 audit (`run_mode=aibridge_13_audit_20260913`)

| Field | Value |
|-------|-------|
| **When** | 2026-09-13T16:58:55Z |
| **builder_project** | aibridge |
| **Active pkg** | `pkg-000011` (default unchanged) |
| **run_mode** | `aibridge_13_audit_20260913` |
| **Skill** | python-pro (G-01) · test-master (G-02/G-03) |
| **pytest** | **177 passed, 1 skipped** |
| **Verify** | ok 6 paths; `--check-dates` ok |

## Gaps CLOSED

| ID | Task | Result |
|----|------|--------|
| G-01 | t07 | PASS — `PostgresEventDedupeStore.try_begin`/`complete`/`abort`/`wait_for_result`; ASGI claim-before-engine; concurrent single OpenAI |
| G-02 | t08 | PASS — OpenAPI error samples 401/409/500 |
| G-03 | t09 | PASS — wrong-owner 403 + double-consume 409, zero extra gateway |

## Product paths

- `src/aibridge/pg_runtime.py`, `src/aibridge/app.py` (replay status from stored `http_status`)
- `tests/test_story_13_audit_gaps.py`

## Handoff

**next=P7** (STOP before P7 re-audit until operator asks)
