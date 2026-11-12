# Task: implement — AIB-REQ validation gates + stable prefix / cache hooks

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-03-responses-tool-budgets.md`  
**Parent story:** [`STORY-AIBRIDGE-03-responses-tool-budgets.md`](../STORY-AIBRIDGE-03-responses-tool-budgets.md)

## Purpose

Three validation gates per AIB-REQ-02 before any Send-authorized path; draft hash; prompt stable-prefix ordering; cache telemetry hooks (metrics HTTP exposure deferred to story 06).

**Out of this task:** dual-confirm FSM (04); `/metrics` endpoint (06).

## Code Facts (verified exists)

1. REQ-01 §11 cache / §12 request assembly + gates.
2. Instruction assembly separator — `content.py` `STABLE_SEPARATOR` (bundle load; prompt builder still Unknown).
3. No validation-gate module in `src/` yet.

## AC/DoD

- [ ] Three validation gates per AIB-REQ-02 before Send-authorized path (AC #5).
- [ ] Draft hash computed/stored as required by AIB-REQ.
- [ ] Stable-prefix ordering; cache telemetry hooks emit (no full `/metrics` required).
- [ ] `Skill declared: python-pro` present.

## Where to change

- Request assembly / validation + prompt builder under `src/aibridge/`.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
```
