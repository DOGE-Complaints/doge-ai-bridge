# Task: implement — strict `/readyz` checks (no OpenAI gen / no gateway write)

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md`  
**Parent story:** [`STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md`](../STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md)  
**P1 scaffold:** 2026-09-13T16:15:49Z  
**Maps:** Scope #3; §5.5; AC #1

## Purpose

Harden `/readyz` for config/DB/migration/bundle/tool/OpenAI **presence**/HTTPS origin syntax/distinct Bearers/redirect. Must not call OpenAI generation or gateway write; optional probes read-only/bounded/cached.

## Code Facts (verified exists — P1)

1. Soft `/readyz` — `src/aibridge/app.py` (auth configured, bearers unequal, content bundle).
2. Migrations / PG — story 09 (`migrate.py`, `pg_runtime.py`) available for version check.

## AC/DoD

- [x] `/readyz` covers §5.5 checklist items with explicit `reason` on 503.
- [x] No OpenAI generation and no gateway write on readiness path.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/app.py` (+ helpers as needed)

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "readyz" --maxfail=8
```
