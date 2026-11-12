# Task: implement — turn serialization + parallel_tool_calls false

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-03-responses-tool-budgets.md`  
**Parent story:** [`STORY-AIBRIDGE-03-responses-tool-budgets.md`](../STORY-AIBRIDGE-03-responses-tool-budgets.md)

## Purpose

Serialize turns per session; set `parallel_tool_calls: false` where the Responses API supports it.

**Out of this task:** dual-confirm FSM (04); global rate limits productization beyond per-session turn lock if deferred to budgets task — keep focused on turn serialization.

## Code Facts (verified exists)

1. Session store — `src/aibridge/sessions.py` (minimal pin/resume; no turn lock yet).
2. Channel turn handler — `app.py` `/v1/channel/turns` (stub processor).
3. REQ-01 §10 turn serialization / parallel_tool_calls constraints.

## AC/DoD

- [ ] Concurrent turns for same session do not interleave unsafely (serialized).
- [ ] Requests set `parallel_tool_calls: false` when supported.
- [ ] `Skill declared: python-pro` present.

## Where to change

- Session turn lock / Responses request assembly under `src/aibridge/`.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
```
