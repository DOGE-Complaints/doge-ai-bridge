# Acceptance verification — task-aibridge-38-t07-audit-g03-asgi-production-wire

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-18T13:56:16Z |
| **Story** | STORY-AIBRIDGE-38-qa-oai-channel-error-outcome |
| **Wave** | `run_mode=aibridge_38_audit_20260918` · P6 |
| **Gap** | G-03 |

## AC check

- [x] ASGI `/v1/channel/turns` wires `ProductionResponsesClient` + scripted HTTP 429 and 503 → Option A envelopes.
- [x] Existing transport-only and `_RaiseClient` paths remain green.
- [x] No invent gateway / live TG / OAS fields.
- [x] `Skill declared: test-master` present.

## Evidence

```text
.venv/bin/python -m pytest tests/integration/test_openai_prompt_behavior.py -q
→ 22 passed
test_oai_008_asgi_production_client_wire_429
test_oai_009_asgi_production_client_wire_503
RecordingAsyncResponsesTransport → ProductionResponsesClient.acreate → ResponsesTransportError handler
```
