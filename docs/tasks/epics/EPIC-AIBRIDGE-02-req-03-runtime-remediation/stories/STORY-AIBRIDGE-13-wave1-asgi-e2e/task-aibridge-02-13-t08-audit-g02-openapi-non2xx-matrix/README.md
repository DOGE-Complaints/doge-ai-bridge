# Task: test — OpenAPI non-2xx matrix samples (G-02)

**Status:** Done  
**Skill declared:** test-master  
**Wave:** `run_mode=aibridge_13_audit_20260913`  
**Gap:** G-02 (Info) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-13-wave1-asgi-e2e-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-13-wave1-asgi-e2e.md`](../STORY-AIBRIDGE-13-wave1-asgi-e2e.md)  
**P5 scaffold:** 2026-09-13T16:54:19Z
**P6 Done:** 2026-09-13T16:58:55Z  
**Maps:** REQ-03 §4 #9 OpenAPI success/replay/non-2xx

## Purpose

Extend wave-1 E2E OpenAPI proof beyond required-key checks + lone 401: sample additional non-2xx channel envelopes (e.g. 409 conflict, 500 bounded) conforming to `ChannelErrorBody`.

## AC/DoD

- [x] E2E (or ASGI+PG) asserts ≥1 non-2xx besides 401 (409 and/or 500) against OAS error shape.
- [x] Success + replay continue to conform.
- [x] No live OpenAI/n8n/Railway.
- [x] `Skill declared: test-master` present.

## Where to change

`tests/story13_e2e_helpers.py`, `tests/test_story_13_wave1_asgi_e2e.py` (and/or dedicated audit test module)

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "story_13 and (openapi or non2xx or 409 or 500)" --maxfail=5
```
