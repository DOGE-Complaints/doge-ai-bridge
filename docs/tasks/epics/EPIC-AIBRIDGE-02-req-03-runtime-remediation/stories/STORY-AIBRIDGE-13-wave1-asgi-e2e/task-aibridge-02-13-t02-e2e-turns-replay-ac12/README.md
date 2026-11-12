# Task: test — E2E turns interview reply + transport replay (AC #1–#2)

**Status:** Done  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md`  
**Parent story:** [`STORY-AIBRIDGE-13-wave1-asgi-e2e.md`](../STORY-AIBRIDGE-13-wave1-asgi-e2e.md)  
**P1 scaffold:** 2026-09-13T16:34:47Z  
**Maps:** REQ-03 §4 AC #1–#2; Target #1

## Purpose

ASGI E2E: `POST /v1/channel/turns` returns model interview reply (not `Received:`); same `(channel, event_id)` replays stored HTTP status+body without second Responses call (Postgres dedupe).

## Code Facts (verified exists — P1)

1. Product path uses `process_turn_async` — `src/aibridge/channel.py` / `app.py`.
2. Coordinator strips leaked `Received:` — `src/aibridge/coordinator.py`.
3. No dedicated wave-1 E2E module covering AC #1–#2 end-to-end yet.

## AC/DoD

- [x] E2E turn asserts reply is interview text and does **not** contain `"Received:"`.
- [x] Duplicate `(channel, event_id)` returns previously stored status+body; fake OpenAI call count does not increase.
- [x] Depends on t01 harness.
- [x] `Skill declared: test-master` present.

## Where to change

`tests/` E2E module(s) using t01 harness.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "story_13 and (turns or replay)" --maxfail=5
```
