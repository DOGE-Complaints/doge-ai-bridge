# Task: implement — settings accept ops/budget env + .env.example parity

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md`  
**Parent story:** [`STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md`](../STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md)  
**P1 scaffold:** 2026-09-13T16:15:49Z  
**Maps:** Scope #2; §5.6

## Purpose

Settings accept TTL, max response bytes, timeouts, log level, rate limits, and all LLM budget vars when set; `.env.example` matches accepted names (no inventing numeric defaults beyond «wired when set»).

## Code Facts (verified exists — P1)

1. Partial Settings fields — `src/aibridge/config.py` (budgets/timeouts/dry_run present; confirm TTL/rate/log completeness vs §5.6).
2. `.env.example` may drift — repo root `doge-ai-bridge/.env.example` (verify on P3).

## AC/DoD

- [x] Settings accept §5.6-listed knobs when env set (no silent ignore of known keys).
- [x] `.env.example` lists the same canonical names.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/config.py`, `.env.example`

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "settings or env or config" --maxfail=5
```
