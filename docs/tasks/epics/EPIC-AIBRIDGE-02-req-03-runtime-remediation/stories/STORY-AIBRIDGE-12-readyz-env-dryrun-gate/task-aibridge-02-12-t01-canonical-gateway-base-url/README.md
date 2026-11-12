# Task: implement — canonical DOGESTONIA_API_BASE_URL (+ origin alias)

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md`  
**Parent story:** [`STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md`](../STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md)  
**P1 scaffold:** 2026-09-13T16:15:49Z  
**Maps:** Scope #1; §5.6

## Purpose

Canonicalize gateway base URL as `DOGESTONIA_API_BASE_URL`; remove or document temporary `DOGESTONIA_GATEWAY_ORIGIN` alias; if both set to different values → readiness fail.

## Code Facts (verified exists — P1)

1. Gateway origin alias present — `src/aibridge/config.py` (`DOGESTONIA_GATEWAY_ORIGIN`).
2. Soft `/readyz` does not yet compare dual origins — `src/aibridge/app.py`.

## AC/DoD

- [x] `DOGESTONIA_API_BASE_URL` is canonical settings field used by gateway executor.
- [x] Alias removed **or** documented temporary; conflicting dual values fail readiness.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/config.py`, `gateway.py`, `app.py` (readyz reason), `.env.example`

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "base_url or gateway_origin or readyz" --maxfail=5
```
