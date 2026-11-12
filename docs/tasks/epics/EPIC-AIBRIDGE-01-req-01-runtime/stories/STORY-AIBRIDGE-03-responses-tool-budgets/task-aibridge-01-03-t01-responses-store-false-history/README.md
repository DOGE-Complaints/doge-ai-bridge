# Task: implement — Responses client store:false + local history

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-03-responses-tool-budgets.md`  
**Parent story:** [`STORY-AIBRIDGE-03-responses-tool-budgets.md`](../STORY-AIBRIDGE-03-responses-tool-budgets.md)

## Purpose

OpenAI Responses integration with every request `store: false`; persist replayable items on bundle-pinned session (story 02 session/registry).

**Out of this task:** dual-confirm Send (04); inventing budget numeric defaults; full `/metrics` (06).

## Code Facts (verified exists)

1. Channel façade stubs — `src/aibridge/channel.py` / `app.py` (no Responses client).
2. Bundle-pinned sessions — `src/aibridge/sessions.py`.
3. Wire OAS on disk — `docs/openapi/story-intake-actions.openapi.yaml`.
4. OPENAI_* env names — REQ-01 §17 (not yet in `config.py` beyond channel/content).

## AC/DoD

- [ ] Every assembled Responses request includes `store: false` (AC #1).
- [ ] Replayable history stored against bundle-pinned session.
- [ ] `Skill declared: python-pro` present.

## Where to change

- New modules under `src/aibridge/` (Responses client / history).
- `src/aibridge/config.py` OPENAI_* fields.
- Wire into channel turn path as appropriate (P3).

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# assert store:false on request payload unit tests
```
