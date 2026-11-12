# Task: implement — AIBRIDGE_DRY_RUN skips real stash

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-05-gateway-outcomes.md`  
**P3 Done:** 2026-09-12T21:54:48Z
**Parent story:** [`STORY-AIBRIDGE-05-gateway-outcomes.md`](../STORY-AIBRIDGE-05-gateway-outcomes.md)

## Purpose

When `AIBRIDGE_DRY_RUN` is set, Send path validates locally without `POST /story-drafts` (AC #2 / Scope #4 / wave-1).

**Out of this task:** inventing numeric defaults; SPA E2E.

## Code Facts (verified exists)

1. Arch dry-run / wave-1 — `03-confirm-gateway.md` §6; `00-overview.md` §7.
2. No `AIBRIDGE_DRY_RUN` in `config.py` yet (`rg` absent).
3. Tool path constant `/story-drafts` — `tool_gen.py`.

## AC/DoD

- [x] Settings expose dry-run flag from `AIBRIDGE_DRY_RUN`.
- [x] Dry-run Send validates locally and does not HTTP POST to gateway.
- [x] Non-dry-run path still uses executor (t01).
- [x] `Skill declared: python-pro` present.

## Where to change

- `config.py` / `.env.example`; executor or Send orchestration.
- Unit tests with dry-run on/off.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# dry-run → zero gateway POST; local validation still runs
```
