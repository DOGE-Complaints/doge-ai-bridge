# Task: implement — wire run_three_gates on FC freeze (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_11_audit_20260913`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-11-coordinator-pause-resume-send-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`](../STORY-AIBRIDGE-11-coordinator-pause-resume-send.md)  
**P5 scaffold:** 2026-09-13T16:07:28Z
**P6 Done:** 2026-09-13T16:12:58Z

## Purpose

REQ-03 §4 #3: function_call must pass three validation gates. Call `request_assembly.run_three_gates` when freezing FC (coordinator path); fail-closed on gate errors; cover with bad-payload test.

## AC/DoD

- [x] Coordinator freeze path invokes `run_three_gates` (injectable schemas / constants).
- [x] Gate failure → no freeze / no Send actions (fail-closed).
- [x] Unit/integration test: bad payload rejected; good payload freezes.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/coordinator.py`, `confirm.py` (optional schemas holder), `tests/test_story_11_coordinator.py`

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_story_11_coordinator.py -k 'gate or three_gates or validate'
```
