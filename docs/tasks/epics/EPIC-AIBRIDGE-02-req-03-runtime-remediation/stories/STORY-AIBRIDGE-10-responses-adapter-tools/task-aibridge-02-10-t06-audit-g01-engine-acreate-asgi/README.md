# Task: implement — InterviewEngine arun_turn / acreate ASGI path (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_10_audit_20260913`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-10-responses-adapter-tools-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-10-responses-adapter-tools.md`](../STORY-AIBRIDGE-10-responses-adapter-tools.md)  
**P6 Done:** 2026-09-13T15:52:34Z
**P5 scaffold:** 2026-09-13T15:49:46Z

## Purpose

§5.1 non-blocking ASGI: engine must have async path using `acreate` (or `asyncio.to_thread` fallback). Real async unit test with mock/recording async transport — not callable-only smoke. Do **not** wire `/turns` (story 11).

## AC/DoD

- [x] `InterviewEngine.arun_turn` exists and uses client `acreate` when present.
- [x] `ProductionResponsesClient.acreate` testable via injected async transport / mock.
- [x] Async unit test awaits real coroutine path (not only `callable`).
- [x] Sync `run_turn` remains for tests / non-ASGI.
- [x] `Skill declared: python-pro` present.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_story_10_responses_adapter.py -k 'acreate or arun_turn or async'
```
