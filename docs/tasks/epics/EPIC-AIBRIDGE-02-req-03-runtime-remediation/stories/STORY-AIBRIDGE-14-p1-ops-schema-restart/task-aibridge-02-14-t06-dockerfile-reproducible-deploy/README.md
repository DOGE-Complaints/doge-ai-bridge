# Task: implement — Dockerfile for reproducible deploy / node clone

**Status:** Done  
**Skill declared:** devops-engineer  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md`  
**Parent story:** [`STORY-AIBRIDGE-14-p1-ops-schema-restart.md`](../STORY-AIBRIDGE-14-p1-ops-schema-restart.md)  
**P1 scaffold:** 2026-09-13T17:03:24Z  
**Maps:** Scope #6 · R3-P1-07

## Purpose

Add a root `Dockerfile` so deploy / node clone is reproducible (R3-P1-07 / REQ-03 §22). Not a Railpack smoke blocker, but required for P1 close.

## Code Facts (verified exists — P1)

1. `Dockerfile` **Absent** at `doge-ai-bridge/` root (glob at P1 materialize).
2. App entry: `src/aibridge/app.py` exposes `app = create_app()`.
3. Python packaging / deps — check `pyproject.toml` / `requirements*.txt` on disk during P3.

## AC/DoD

- [x] `Dockerfile` at repo root builds image that can start ASGI app (documented CMD/ENTRYPOINT).
- [x] Document minimal build/run commands in task evidence or adjacent ops note (no invent of Railway secrets).
- [x] `Skill declared: devops-engineer` present.

## Where to change

`Dockerfile`, optionally `.dockerignore`, brief ops note under `docs/` if needed (not `docs/tasks/**` product commits unless asked).

## Verification commands

```bash
cd doge-ai-bridge && test -f Dockerfile && docker build -t aibridge:story14 .
# or document why docker unavailable in gate evidence; file must still exist and be reviewable
```
