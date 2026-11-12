# Story acceptance gate — STORY-AIBRIDGE-06-ops-wave1-proof

- **Story:** Ops, metrics, wave-1 proof
- **Package:** `pkg-000006-20260912-epic-aibridge-01-story-06-ops-wave1.yaml`
- **Result:** PASS
- **Date:** 2026-09-12T22:06:45Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `/metrics` without channel Bearer on private interface returns series without narrative samples. | PASS | `app.py` GET `/metrics` PlainTextResponse (no channel auth); `tests/test_ops_wave1.py::test_metrics_without_bearer_no_narrative`; budget reasons via `test_budget_stop_reason_in_metrics` |
| Unique test phrase absent from default logs/metrics after a turn (privacy-pilot.md). | PASS | `audit.py` redacted events; `test_privacy_phrase_absent_from_audit_and_metrics` |
| Wave-1 checklist documented and executable (live n8n call may be manual ops proof). | PASS | `docs/ops/wave1-gate-checklist.md`; automated `/readyz`+401 in `test_wave1_readyz_and_401_smoke`; live n8n → turns remains manual ops |
| Runbook/ops paths exist (`ls` verify against Doc pointers table). | PASS | `test_runbook_and_ops_paths_exist` + `docs/ops/operator-pilot-readme.md` |
| `.env.example` lists required knobs from REQ-01 §17 without secret values. | PASS | `.env.example`; `test_env_example_lists_required_knobs_without_secrets` |

## Commands (live verification 2026-09-12T22:06:45Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
cd doge-ai-bridge && .venv/bin/pytest -q
# → 96 passed, 1 skipped
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
