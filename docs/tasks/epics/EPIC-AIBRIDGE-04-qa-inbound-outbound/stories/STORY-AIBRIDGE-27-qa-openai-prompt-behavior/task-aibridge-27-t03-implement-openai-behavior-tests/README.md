# Task: test — implement OpenAI / prompt behavior integration suite

**Status:** Done  
**P3 closed:** 2026-09-17T18:46:05Z  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md`  
**Parent story:** [`STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md`](../STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md)  
**P1 scaffold:** 2026-09-17T18:39:38Z  
**Maps:** OAI-001…016 · layer `tests/integration/`

## Purpose

Integration tests under `tests/integration/` covering OAI-001…016 via RecordingResponsesClient scripted bodies / http_error stubs: reply/fallback/`Received:` map, cache metric, store:false fail-closed, XOR prefix vs instructions, parallel_tool_calls false, 429/5xx/timeout/invalid JSON bounded errors, budgets, secret non-disclosure, tool-looking user text, stable prefix hash, bundle pin. No live Telegram. Characterization OAI-008/009/016 capture-first.

## AC/DoD

- [x] Suite under `tests/integration/` asserts matrix must-rows via RecordingResponsesClient.
- [x] No live Telegram / network Telegram API in default CI path.
- [x] Characterization rows capture-first (OAI-008/009/016); no silent product invent.
- [x] No secrets in captured OpenAI payloads / logs asserts.
- [x] `Skill declared: python-pro` present.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/integration/test_openai_prompt_behavior.py -q
→ 18 passed
```

## Where to change

- `doge-ai-bridge/tests/integration/test_openai_prompt_behavior.py` — **Done**
