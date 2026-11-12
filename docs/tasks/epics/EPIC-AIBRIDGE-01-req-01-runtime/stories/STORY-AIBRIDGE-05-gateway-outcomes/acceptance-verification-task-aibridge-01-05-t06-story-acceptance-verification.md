# Story acceptance gate — STORY-AIBRIDGE-05-gateway-outcomes

- **Story:** Gateway executor, dry-run, outcomes
- **Package:** `pkg-000005-20260912-epic-aibridge-01-story-05-gateway-outcomes.yaml`
- **Result:** PASS
- **Date:** 2026-09-12T21:54:48Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Channel Bearer never used as gateway Bearer. | PASS | `gateway.py` Authorization from `DOGESTONIA_API_BEARER_TOKEN` only; equal-token refuse; `tests/test_gateway_outcomes.py::test_executor_uses_gateway_bearer_never_channel` |
| Dry-run: Send path validates locally without `POST /story-drafts`. | PASS | `AIBRIDGE_DRY_RUN` → `DRY_RUN_OK`, zero transport calls; `test_dry_run_validates_without_post` |
| Malformed 201 → not `stashed`. | PASS | `CONTRACT_MISMATCH`; `test_malformed_201_not_stashed` |
| `unknown_outcome` blocks auto Send retry for same revision. | PASS | `unknown_outcome_revision` + `send_blocked_for_revision`; `test_timeout_maps_unknown_and_blocks_resend` / `test_unknown_blocks_confirm_send_same_revision` |
| Stash copy / UX never claims Story published. | PASS | `STASH_REPLY` explicitly «not a published Story»; `test_continuation_url_only_when_stashed` |
| Continuation URL uses `DOGESTONIA_DRAFT_REDIRECT_BASE_URL` only when outcome is `stashed`. | PASS | `build_continuation_url` only on STASHED; `test_non_stashed_has_no_continuation` |

## Commands (live verification 2026-09-12T21:54:48Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
cd doge-ai-bridge && .venv/bin/pytest -q
# → 83 passed, 1 skipped
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
