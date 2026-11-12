# Task: fix — release turn_lock before gateway HTTPS (G-02)

**Status:** Done  
**Skill declared:** fastapi-expert  
**Wave:** `run_mode=aibridge_11_audit_20260913`  
**Gap:** G-02 (Medium) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-11-coordinator-pause-resume-send-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`](../STORY-AIBRIDGE-11-coordinator-pause-resume-send.md)  
**P5 scaffold:** 2026-09-13T16:07:28Z
**P6 Done:** 2026-09-13T16:12:58Z

## Purpose

Target AC: no PG session turn lock held across gateway HTTPS. `process_action` must not wrap `call_gateway` / transport.request inside `turn_lock.hold`.

## AC/DoD

- [x] Send/HTTPS segment runs **outside** `turn_lock.hold`.
- [x] Token consume + state prep may remain under lock; `create_executing` still commits before HTTPS.
- [x] Test asserts lock not held during `transport.request` (spy / ordering).
- [x] `Skill declared: fastapi-expert` present.

## Where to change

`src/aibridge/channel.py`, `confirm.py`, tests

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k 'lock or before_https or g02'
```
