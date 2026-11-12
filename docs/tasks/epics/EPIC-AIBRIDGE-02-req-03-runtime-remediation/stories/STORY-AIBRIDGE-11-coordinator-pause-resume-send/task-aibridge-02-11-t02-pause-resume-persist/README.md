# Task: implement — pause/resume persist before /turns actions

**Status:** Done  
**Skill declared:** fastapi-expert  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`  
**Parent story:** [`STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`](../STORY-AIBRIDGE-11-coordinator-pause-resume-send.md)  
**P1 scaffold:** 2026-09-13T15:55:55Z
**P3 Done:** 2026-09-13T16:03:23Z  
**Maps:** Scope #2; REQ-03 §4 #3 + pending-survive AC

## Purpose

Human confirmation pauses the tool loop across HTTP: persist pending continuation, original `call_id`, frozen body, and replayable output items **before** `/turns` returns actions; nothing left open waiting for Telegram.

## Code Facts (verified exists — P1)

1. Confirm session holds frozen intent fields — `src/aibridge/confirm.py` (`frozen_tool_intent`, `draft_hash`, persist helpers).
2. Session resume is bundle-oriented today — `src/aibridge/sessions.py` `resume_bundle` (content bundle), not Responses continuation blob.
3. REQ-03 §5.2 sequence requires persist-before-actions — `docs/requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md` §5.2.

## AC/DoD

- [x] On `function_call`, allowlisted name + validation gates; original `call_id` stored; no gateway before Send (REQ-03 §4 #3).
- [x] Pending continuation / frozen body / replay items committed before `/turns` returns actions.
- [x] Pending confirm survives a second HTTP request and process restart (09 store).
- [x] `Skill declared: fastapi-expert` present.

## Where to change

`src/aibridge/channel.py`, `confirm.py`, session/confirm PG stores (09)

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "pause or resume or pending or confirm" --maxfail=5
```
