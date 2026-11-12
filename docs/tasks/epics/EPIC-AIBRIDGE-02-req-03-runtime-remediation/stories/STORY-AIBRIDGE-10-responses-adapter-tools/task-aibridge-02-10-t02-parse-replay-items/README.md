# Task: implement — parse Responses + preserve replay items

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-10-responses-adapter-tools.md`  
**Parent story:** [`STORY-AIBRIDGE-10-responses-adapter-tools.md`](../STORY-AIBRIDGE-10-responses-adapter-tools.md)  
**P3 Done:** 2026-09-13T15:46:08Z
**P1 scaffold:** 2026-09-13T15:40:24Z  
**Maps:** Scope #1 (parse/replay); AC #1

## Purpose

Parse function_call/call_id/arguments/usage; record cached input tokens; preserve every replay-required output item (not only output_text).

## Code Facts (verified exists — P1)

1. RecordingResponsesClient records requests — responses_client.py.
2. InterviewEngine uses client.create — interview.py.
3. Pause/resume persistence of call_id is STORY-11 (out of scope).

## AC/DoD

- [x] function_call / call_id / arguments / usage parsed from Responses payload.
- [x] Cached input tokens recorded from usage structure.
- [x] Replay-required output items preserved (not only output_text).
- [x] `Skill declared: python-pro` present.

## Where to change

src/aibridge/responses_client.py / parse helpers

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_story_10_responses_adapter.py -k parse
```
