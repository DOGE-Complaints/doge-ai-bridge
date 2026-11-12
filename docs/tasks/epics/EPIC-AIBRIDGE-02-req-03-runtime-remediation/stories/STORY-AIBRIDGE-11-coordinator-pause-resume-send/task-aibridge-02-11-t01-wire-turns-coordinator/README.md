# Task: implement — wire /turns coordinator (no Received stub)

**Status:** Done  
**Skill declared:** fastapi-expert  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`  
**Parent story:** [`STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`](../STORY-AIBRIDGE-11-coordinator-pause-resume-send.md)  
**P1 scaffold:** 2026-09-13T15:55:55Z
**P3 Done:** 2026-09-13T16:03:23Z  
**Maps:** Scope #1; REQ-03 §4 AC #1

## Purpose

Wire `POST /v1/channel/turns` → session repo → Responses client → tool loop → confirm so the product path returns a model interview reply, not stub `Received: …`.

## Code Facts (verified exists — P1)

1. Stub side-effect — `src/aibridge/channel.py` `process_turn` builds `reply_text=f"Received: {body.message.text[:200]}"`.
2. ASGI calls stub path — `src/aibridge/app.py` `channel_turns` → `process_turn`.
3. Engine exists off ASGI product path — `src/aibridge/interview.py` `InterviewEngine.run_turn` / `arun_turn`.

## AC/DoD

- [x] `/v1/channel/turns` with fake/recorded Responses returns interview reply, **not** `Received: …` (REQ-03 §4 #1).
- [x] Path uses session repo + Responses client + tool loop entry toward confirm (R3-P0-01).
- [x] `Skill declared: fastapi-expert` present.

## Where to change

`src/aibridge/channel.py`, `app.py`, `interview.py` (wire only; no live OpenAI keys)

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "turn or channel" --maxfail=5
```
