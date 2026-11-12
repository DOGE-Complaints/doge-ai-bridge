# Task: implement — wave-1 dry-run stash + function_call_output

**Status:** Done  
**Skill declared:** fastapi-expert  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`  
**Parent story:** [`STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`](../STORY-AIBRIDGE-11-coordinator-pause-resume-send.md)  
**P1 scaffold:** 2026-09-13T15:55:55Z
**P3 Done:** 2026-09-13T16:03:23Z  
**Maps:** Scope #5; REQ-03 §4 AC #6

## Purpose

On valid gateway 201 via dry-run/fake transport: return `stashed` / `draft_id` / `continuation_url` as applicable; then send `function_call_output` with the original `call_id`; resident reply must not claim Story publish.

## Code Facts (verified exists — P1)

1. Stash outcome enum + reply copy — `src/aibridge/gateway.py` (`GatewayOutcome.STASHED`, stash contract reply text).
2. Channel success envelope already has draft fields — `src/aibridge/channel.py` `build_success` (`draft_id`, `continuation_url`, `outcome`).
3. Wave-1 real `POST /story-drafts` is out of scope until story 14 — backlog «Вне scope».

## AC/DoD

- [x] Fake/dry-run 201 yields `stashed` (+ `draft_id`/`continuation_url` when applicable) (REQ-03 §4 #6).
- [x] Follow-up Responses request includes `function_call_output` with original `call_id`.
- [x] Final resident reply does not assert Story publish.
- [x] `Skill declared: fastapi-expert` present.

## Where to change

`src/aibridge/gateway.py`, `confirm.py`, `interview.py` / Responses follow-up path

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "stash or draft_id or function_call_output" --maxfail=5
```
