# Task: implement — AIBRIDGE_DRY_RUN=false fails readiness (until story 14)

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md`  
**Parent story:** [`STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md`](../STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md)  
**P1 scaffold:** 2026-09-13T16:15:49Z  
**Maps:** Scope #4; REQ-03 §2; AC #2

## Purpose

Until R3-P1-03 (story 14) completes, `AIBRIDGE_DRY_RUN=false` must fail `/readyz` (wave-1 dry-run gate).

## Code Facts (verified exists — P1)

1. `aibridge_dry_run` Settings field — `src/aibridge/config.py`.
2. Soft `/readyz` does not gate on dry-run — `src/aibridge/app.py`.

## AC/DoD

- [x] `AIBRIDGE_DRY_RUN=false` → `/readyz` 503 with clear reason (until story 14 flag/lift).
- [x] `AIBRIDGE_DRY_RUN=true` does not fail this specific gate.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/app.py`, `config.py` (optional feature flag for post-14 lift)

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "dry_run or dryrun or readyz" --maxfail=5
```
