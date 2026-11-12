# Story acceptance gate — STORY-AIBRIDGE-10-responses-adapter-tools

- **Story:** Production Responses adapter + flat tools + prompt
- **Package:** `pkg-000008-20260913-epic-aibridge-02-story-10-responses-adapter.yaml`
- **Result:** PASS
- **Date:** 2026-09-13T15:46:08Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Every §5.1 bullet satisfied on the live/production client path (tests with fake or recorded transport OK until live smoke policy). | PASS | `ProductionResponsesClient` + `RecordingResponsesTransport`; `test_client_knobs_*`, `test_client_maps_429_*`, `test_client_timeout_outcome`, `acreate` ASGI path |
| Emitted tool schema is Responses-flat. | PASS | `generate_strict_tool` flat shape; `test_flat_tool_schema_from_generator`, `test_generate_strict_tool_from_wire_oas` |
| Prompt assembly never duplicates instructions (prefix xor `instructions=`). | PASS | `assert_prompt_xor` + `InterviewEngine.prompt_channel`; `test_prompt_xor_*` |
| API key never appears in logs/exceptions. | PASS | `redact_secrets`; `test_client_maps_429_and_redacts_key` |

## Commands (live verification 2026-09-13T15:46:08Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
cd doge-ai-bridge && .venv/bin/pytest -q
# → 112 passed, 14 skipped
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
