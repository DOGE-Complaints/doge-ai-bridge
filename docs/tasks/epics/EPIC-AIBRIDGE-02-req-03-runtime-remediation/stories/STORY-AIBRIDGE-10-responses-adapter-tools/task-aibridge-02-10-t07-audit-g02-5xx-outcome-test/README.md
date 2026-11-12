# Task: test — HTTP 5xx → transient_failure (G-02)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_10_audit_20260913`  
**Gap:** G-02 (Info) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-10-responses-adapter-tools-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-10-responses-adapter-tools.md`](../STORY-AIBRIDGE-10-responses-adapter-tools.md)  
**P6 Done:** 2026-09-13T15:52:34Z
**P5 scaffold:** 2026-09-13T15:49:46Z

## Purpose

Assert recorded-transport HTTP 503 maps to `transient_failure` (parity with 429/timeout tests).

## AC/DoD

- [x] Test: status 503 → `ResponsesOutcome.TRANSIENT_FAILURE` / transport error outcome.
- [x] No live OpenAI.
- [x] `Skill declared: python-pro` present.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_story_10_responses_adapter.py -k 5xx
```
