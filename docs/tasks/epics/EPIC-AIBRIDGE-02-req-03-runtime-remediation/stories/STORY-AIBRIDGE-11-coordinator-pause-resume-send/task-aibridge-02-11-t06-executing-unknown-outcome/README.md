# Task: implement — executing restart → unknown_outcome (no auto-resend)

**Status:** Done  
**Skill declared:** fastapi-expert  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`  
**Parent story:** [`STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`](../STORY-AIBRIDGE-11-coordinator-pause-resume-send.md)  
**P1 scaffold:** 2026-09-13T15:55:55Z
**P3 Done:** 2026-09-13T16:03:23Z  
**Maps:** Scope #6; REQ-03 §4 AC #8

## Purpose

If the process restarts (or loses the response) while a gateway attempt remains `executing`, recovery marks `unknown_outcome` and **must not** automatically resend.

## Code Facts (verified exists — P1)

1. Block auto Send on unknown_outcome — `src/aibridge/confirm.py` `send_blocked_for_revision`.
2. FSM + gateway outcomes include `UNKNOWN_OUTCOME` — `confirm_fsm.py`, `gateway.py`.
3. REQ-03 §5.3 recovery rule — committed `executing` → `unknown_outcome`; no automatic resend.

## AC/DoD

- [x] Restart/`executing` recovery → `unknown_outcome` (REQ-03 §4 #8).
- [x] No automatic second HTTPS for the same authorized revision.
- [x] `Skill declared: fastapi-expert` present.

## Where to change

`src/aibridge/confirm.py`, `gateway.py`, boot/recovery wiring as needed

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "unknown_outcome or executing" --maxfail=5
```
