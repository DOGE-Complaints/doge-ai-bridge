# Task: implement — production Responses client knobs

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-10-responses-adapter-tools.md`  
**Parent story:** [`STORY-AIBRIDGE-10-responses-adapter-tools.md`](../STORY-AIBRIDGE-10-responses-adapter-tools.md)  
**P3 Done:** 2026-09-13T15:46:08Z
**P1 scaffold:** 2026-09-13T15:40:24Z  
**Maps:** Scope #1 (transport knobs); AC #1/#4

## Purpose

Live/production client path: store:false, parallel_tool_calls:false, finite max_output_tokens, bounded timeouts, non-blocking ASGI, map 429/5xx/timeouts, never leak API key.

## Code Facts (verified exists — P1)

1. RecordingResponsesClient only — responses_client.py.
2. assemble_responses_request already sets store:false / parallel_tool_calls:false — responses_client.py.
3. No production HTTP transport client on disk yet (P1).

## AC/DoD

- [x] Production client path exists with §5.1 transport knobs.
- [x] 429/5xx/timeouts map to bounded internal outcomes.
- [x] API key never appears in logs/exceptions (AC #4).
- [x] `Skill declared: python-pro` present.

## Where to change

src/aibridge/responses_client.py (+ config knobs as needed)

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_story_10_responses_adapter.py -k client
```
