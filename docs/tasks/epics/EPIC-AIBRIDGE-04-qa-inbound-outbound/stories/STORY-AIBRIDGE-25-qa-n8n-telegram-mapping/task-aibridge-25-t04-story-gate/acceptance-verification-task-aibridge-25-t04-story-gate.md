# Acceptance verification — task-aibridge-25-t04-story-gate

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T17:44:23Z |
| **Story** | STORY-AIBRIDGE-25-qa-n8n-telegram-mapping |
| **Pkg** | pkg-000022 |
| **Wave** | P3 Execute |

## AC check

- [x] Every N8N-001…018 appears in TRACEABILITY with this story key and is covered by fixtures+tests.
- [x] Characterization N8N-009 / N8N-011 capture-first (no caption/edit invent).
- [x] Guide must-rows automated; `answerCallbackQuery` before `/actions` asserted.
- [x] Stashed: `claim_published_forbidden`; non-stashed accidental URL suppressed.
- [x] Seed originals hash_eq vs copies; package originals intact.
- [x] No live Telegram / Railway SUCCESS invent.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/n8n/ -q --noconftest → 19 passed
```
