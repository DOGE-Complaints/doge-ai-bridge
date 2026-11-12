# Story acceptance gate — STORY-AIBRIDGE-04-dual-confirm-tokens

- **Story:** Dual-confirm FSM + action tokens
- **Package:** `pkg-000004-20260912-epic-aibridge-01-story-04-dual-confirm.yaml`
- **Result:** PASS
- **Date:** 2026-09-12T21:40:45Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Interpretation confirm produces no gateway HTTP. | PASS | t02 · `tests/test_interpret_vs_send.py` · `confirm.py` |
| Invalid / expired / foreign / consumed token → 4xx per §6 statuses; fail closed. | PASS | t05 · `tests/test_actions_fail_closed.py` · `app.py` `/actions` |
| Callback payload contains only opaque token ≤64 UTF-8 bytes. | PASS | t03 · `tests/test_action_tokens.py` · `action_tokens.py` |
| Content edit increments revision and invalidates prior Send tokens. | PASS | t04 · `tests/test_edit_cancel_ownership.py` |
| Tool intent alone never equals Send permission. | PASS | t02 · `authorize_from_tool_intent_alone` → False |

## Commands (live verification — P3)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
cd doge-ai-bridge && .venv/bin/pytest -q
# → 70 passed, 1 skipped; verify ok 6 paths; date-check ok
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
