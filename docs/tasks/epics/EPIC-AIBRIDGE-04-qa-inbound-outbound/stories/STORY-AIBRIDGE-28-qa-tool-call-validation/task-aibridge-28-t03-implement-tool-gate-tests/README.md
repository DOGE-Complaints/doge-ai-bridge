# Task: test — implement tool-call validation unit suite

**Status:** Done  
**P3 closed:** 2026-09-17T19:07:11Z  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-28-qa-tool-call-validation.md`  
**Parent story:** [`STORY-AIBRIDGE-28-qa-tool-call-validation.md`](../STORY-AIBRIDGE-28-qa-tool-call-validation.md)  
**P1 scaffold:** 2026-09-17T19:00:38Z  
**Maps:** TOOL-001…014 · layer `tests/unit/`

## Purpose

Unit tests under `tests/unit/` covering TOOL-001…014 via ValidationContext + RecordingGatewayTransport pin: FC before Looks right blocked; single allowlisted call after confirmation → three gates + freeze + Send; reject shapes; gate 1–3 failures; server-owned fields stripped; persist failure → no Send; call_id replay → no gateway. No live Telegram. TOOL-014 remint FSM capture-first.

## AC/DoD

- [x] Suite under `tests/unit/` asserts TOOL-001…014 must-rows.
- [x] No Send actions / gateway on reject paths.
- [x] No live Telegram / network Telegram API in default CI path.
- [x] TOOL-014 characterization capture-first; no silent product invent.
- [x] `Skill declared: python-pro` present.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/unit/test_tool_call_validation.py -q
→ 17 passed
```

## Where to change

- `doge-ai-bridge/tests/unit/test_tool_call_validation.py` — **Done**
