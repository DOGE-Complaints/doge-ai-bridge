# Story acceptance gate — STORY-AIBRIDGE-15-n8n-telegram-gate

- **Story:** Live n8n / Telegram integration gate
- **Package:** `pkg-000013-20260913-epic-aibridge-02-story-15-n8n-telegram-gate.yaml`
- **Result:** PASS (docs + recorded contract; live Telegram residual BLOCKED)
- **Date:** 2026-09-13T17:34:04Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| §6.1 checklist evidenced (runbook + screenshots/logs or recorded integration test). | PASS | Checklist [r3-p1-09-live-gate-checklist.md](../../../../../../ops/n8n-channel-workflow/r3-p1-09-live-gate-checklist.md) · recorded `tests/test_story_15_n8n_gate_contract.py` · live screenshots **BLOCKED** ([live-evidence-BLOCKED-20260913.md](../../../../../../ops/n8n-channel-workflow/live-evidence-BLOCKED-20260913.md)) |
| Retry of same Telegram update does not mint a new `event_id`. | PASS | README derivation + `test_story_15_event_id_derivation_stable_across_retry` · `test_story_15_same_event_id_retry_does_not_remint` |

## Commands (live verification — 2026-09-13T17:34:04Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
cd doge-ai-bridge && ./scripts/start-disposable-pg.sh && .venv/bin/pytest -q
# → ok 6 paths; ok date-check; 203 passed, 1 skipped
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
