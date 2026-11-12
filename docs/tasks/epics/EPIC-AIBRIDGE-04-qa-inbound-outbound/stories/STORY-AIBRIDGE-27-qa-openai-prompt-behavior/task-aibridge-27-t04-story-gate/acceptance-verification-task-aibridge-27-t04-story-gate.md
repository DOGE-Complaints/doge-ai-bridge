# Acceptance verification — task-aibridge-27-t04-story-gate

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T18:46:05Z |
| **Story** | STORY-AIBRIDGE-27-qa-openai-prompt-behavior |
| **Pkg** | pkg-000024 |
| **Wave** | P3 Execute |

## AC check

- [x] Every OAI-001…016 appears in TRACEABILITY with this story key and is covered by fixtures+tests.
- [x] Characterization OAI-008 (ASGI 500 shape on raise) / OAI-009 (transient_failure; no retry invent) / OAI-016 (new pack → new prefix) capture-first — no invent.
- [x] Guide must-rows automated: text reply+actions, empty→Acknowledged., Received:→Acknowledged., cache metric, store:true fail-closed, XOR, parallel_tool_calls false, 429/5xx/timeout/invalid, budget no gateway, secret non-disclosure, tool-looking user content, stable prefix hash.
- [x] No secrets in captured payloads / audit dump.
- [x] Seed/matrix originals hash_eq vs copies; package originals intact.
- [x] No live Telegram / Railway SUCCESS invent.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/integration/test_openai_prompt_behavior.py -q
→ 18 passed
```
