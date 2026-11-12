# Task: implement — bounded channel JSON 500 envelope

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md`  
**Parent story:** [`STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md`](../STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md)  
**P1 scaffold:** 2026-09-13T16:15:49Z  
**Maps:** Scope #5; P0-11; AC #3 / REQ-03 AC #9

## Purpose

Unhandled errors on channel routes return bounded JSON **500** conforming to OpenAPI channel error envelope (not raw framework HTML/text).

## Code Facts (verified exists — P1)

1. Channel error helper — `src/aibridge/app.py` `error_body` / `ChannelErrorBody`.
2. Validation handlers exist; unhandled exception → 500 envelope may be missing — verify on P3.

## AC/DoD

- [x] Unhandled exception on `/v1/channel/*` → HTTP 500 + bounded OpenAPI error JSON.
- [x] No stack traces / secrets in response body.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/app.py`, schemas if needed

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "500 or internal_error or unhandled" --maxfail=5
```
