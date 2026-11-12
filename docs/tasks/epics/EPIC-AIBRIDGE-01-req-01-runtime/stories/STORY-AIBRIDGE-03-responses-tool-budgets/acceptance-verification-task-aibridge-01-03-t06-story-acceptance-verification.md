# Story acceptance gate — STORY-AIBRIDGE-03-responses-tool-budgets

- **Story:** Responses loop, strict tool, LLM budgets
- **Package:** `pkg-000003-20260912-epic-aibridge-01-story-03-responses-tool.yaml`
- **Result:** PASS
- **Date:** 2026-09-12T21:23:18Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Every Responses request has `store: false`. | PASS | t01 · `tests/test_responses_store_false.py` · `src/aibridge/responses_client.py` |
| Tool schema deterministic; unsupported OpenAPI constructs fail startup (no silent non-strict). | PASS | t02 · `tests/test_tool_gen.py` · `src/aibridge/tool_gen.py` · `deployment.py` tool_gen fail → not ready |
| Budget breach → resident-safe error, no gateway call, redacted metric reason. | PASS | t04 · `tests/test_budgets.py` · `src/aibridge/budgets.py` / `interview.py` |
| Model cannot override pack / origin / URL / auth. | PASS | t02/t05 · `strip_server_owned_fields` · `tests/test_request_assembly.py` |
| Three validation gates per AIB-REQ-02 before any Send-authorized path. | PASS | t05 · `tests/test_request_assembly.py` · `src/aibridge/request_assembly.py` |

## Commands (live verification — P3)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
cd doge-ai-bridge && .venv/bin/pytest -q
# → 50 passed, 1 skipped; verify ok 6 paths; date-check ok
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
