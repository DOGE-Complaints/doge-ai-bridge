# Acceptance — task-aibridge-52-t01-wire-text-brief-port-into-accept

| Field | Value |
|-------|-------|
| **Date** | 2026-10-16T11:05:47Z |
| **Result** | **PASS** |

## Disk facts

| Claim | Evidence |
|-------|----------|
| Purpose | Replace direct generate_sense_brief with resolve_text_brief_provider → generate_brief. |
| Code | `app.py` ports wire · `poster/pipeline.py` `poster_bytes=` · Present adapters |
| Tests | `DATABASE_URL= pytest tests/test_mock_accept_pipe_story_52.py` (+46–51) · **54 passed** |
| Scope | No 53/54 invent · accept/bind HTTP contracts unchanged |
