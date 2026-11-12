# Task: test — OAI-009 channel depth mirror of 008 (G-01)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_27_audit_20260917`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-27-qa-openai-prompt-behavior-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md`](../STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md)  
**P5 scaffold:** 2026-09-17T18:52:17Z  
**P6 closed:** 2026-09-17T18:54:18Z  
**Gate:** [acceptance-verification-task-aibridge-27-t05-audit-g01-oai009-channel-depth.md](./acceptance-verification-task-aibridge-27-t05-audit-g01-oai009-channel-depth.md) PASS  

## Purpose

Mirror OAI-008 channel characterization for OAI-009 (5xx): ASGI `POST /v1/channel/turns` with raise/`TRANSIENT_FAILURE` path → bounded 500 `internal_error` (capture-first), `gw=[]`, `_assert_forbid` / no secrets, dedupe abort so retry can run. Keep existing transport `TRANSIENT_FAILURE` assert. **Do not** invent retry product policy. **No** live Telegram / Railway invent.

## AC/DoD

- [x] `test_oai_009` exercises ASGI channel path with 5xx/raise characterization like OAI-008.
- [x] Asserts: bounded error shape · gateway calls empty · forbid secrets · dedupe claim aborted.
- [x] Suite still green; no live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/integration/test_openai_prompt_behavior.py` — **P6 Done**
