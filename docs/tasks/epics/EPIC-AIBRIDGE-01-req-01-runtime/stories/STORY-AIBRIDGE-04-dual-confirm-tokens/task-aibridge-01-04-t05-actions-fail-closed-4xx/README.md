# Task: implement — `/actions` fail-closed 4xx statuses

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-04-dual-confirm-tokens.md`  
**Parent story:** [`STORY-AIBRIDGE-04-dual-confirm-tokens.md`](../STORY-AIBRIDGE-04-dual-confirm-tokens.md)

## Purpose

Wire `process_action` beyond stub: invalid / expired / foreign / consumed token → 4xx per REQ-01 §6 (AIB-CH-03 / AIB-CH-05); fail closed.

**Out of this task:** actual gateway `POST /story-drafts` (05).

## Code Facts (verified exists)

1. `POST /v1/channel/actions` — `app.py`; stub success in `channel.process_action`.
2. Channel error envelope helpers — `app.py` `error_body`.
3. Dedupe store already wraps actions (story 01).

## AC/DoD

- [ ] Invalid / expired / foreign / consumed → 4xx fail closed (AC #2).
- [ ] Success path only after valid token consume for permitted action.
- [ ] `Skill declared: python-pro` present.

## Where to change

- `src/aibridge/channel.py`, `app.py` as needed; error codes per §6.
- Contract tests under `tests/`.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# one test per reject class + happy path without gateway HTTP
```
