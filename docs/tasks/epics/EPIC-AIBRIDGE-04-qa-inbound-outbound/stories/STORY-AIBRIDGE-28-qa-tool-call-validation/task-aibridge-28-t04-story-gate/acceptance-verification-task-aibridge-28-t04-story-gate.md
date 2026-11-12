# Acceptance verification — task-aibridge-28-t04-story-gate

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T19:07:11Z |
| **Story** | STORY-AIBRIDGE-28-qa-tool-call-validation |
| **Pkg** | pkg-000025 |
| **Wave** | P3 Execute |

## AC check

- [x] Every TOOL-001…014 appears in TRACEABILITY with this story key and is covered by fixtures+tests.
- [x] Characterization TOOL-014 (awaiting_send remint → IllegalTransition; register_session_call not wired into coordinator) capture-first — no invent.
- [x] Guide must-rows automated: FC before Looks right blocked; single allowlisted → gates+freeze+Send; reject two/unknown/missing id/malformed/array; gate1–3 failures; server-owned strip/replace; persist failure no Send; no gateway on reject/replay.
- [x] No Send on reject paths.
- [x] Package originals hash_eq vs copies; originals intact.
- [x] No live Telegram / Railway SUCCESS invent.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/unit/test_tool_call_validation.py -q
→ 17 passed
```
