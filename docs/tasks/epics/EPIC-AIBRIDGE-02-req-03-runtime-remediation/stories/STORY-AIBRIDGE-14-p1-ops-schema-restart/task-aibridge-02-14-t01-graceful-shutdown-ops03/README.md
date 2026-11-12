# Task: implement — graceful shutdown (AIB-OPS-03 / R3-P1-01)

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md`  
**Parent story:** [`STORY-AIBRIDGE-14-p1-ops-schema-restart.md`](../STORY-AIBRIDGE-14-p1-ops-schema-restart.md)  
**P1 scaffold:** 2026-09-13T17:03:24Z  
**Maps:** Scope #1 · R3-P1-01

## Purpose

Graceful shutdown so a restart mid-Send does not leave ambiguous in-flight gateway state (AIB-OPS-03 / REQ-03 §18).

## Code Facts (verified exists — P1)

1. `create_app` in `src/aibridge/app.py` builds Starlette/FastAPI app **without** lifespan / SIGTERM drain handlers (grep `lifespan|SIGTERM` → empty under `src/`).
2. Send / attempt store paths live in `confirm.py` / `pg_runtime.py` / `gateway.py` (story 11/13).

## AC/DoD

- [x] Process shutdown drains or fail-closes in-flight Send/gateway attempts per AIB-OPS-03 (documented behavior + code).
- [x] Tests cover restart-during-Send ambiguity reduction (no silent double-stash claim).
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/app.py` (lifespan), optionally `gateway.py` / `confirm.py` / `pg_runtime.py`, `tests/`.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "shutdown or graceful or story_14" --maxfail=10
```
