# Story acceptance gate — STORY-AIBRIDGE-11-coordinator-pause-resume-send

- **Story:** Coordinator + pause/resume + Send txn
- **Package:** `pkg-000009-20260913-epic-aibridge-02-story-11-coordinator-pause-resume-send.yaml`
- **Result:** PASS
- **Date:** 2026-09-13T16:03:23Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| REQ-03 §4 acceptance criteria #1, #3, #4, #5, #6, #8 on fake/dry-run transports. | PASS | `test_turn_returns_interview_not_received`; `test_function_call_persisted_before_send_actions`; `test_interpretation_confirm_no_gateway_http`; `test_send_uses_frozen_body_only`; `test_stashed_then_function_call_output_with_call_id`; `test_recover_stale_executing_blocks_auto_resend` + existing gateway dry-run/commit suites |
| No PostgreSQL txn/lock held across gateway HTTPS. | PASS | `call_gateway` commits `create_executing` before HTTPS; `test_attempt_committed_before_https_and_outcome_after` (PG); outcome via separate `set_outcome` |
| Pending confirm survives separate HTTP requests and restart (with 09 store). | PASS | `pending_call_id` / `pending_replay_items` on ConfirmSession + persist/hydrate; `test_pending_survives_fresh_guard_memory_rehydrate` |

## Commands (live verification 2026-09-13T16:03:23Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
cd doge-ai-bridge && .venv/bin/pytest -q
# → 122 passed, 14 skipped
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
