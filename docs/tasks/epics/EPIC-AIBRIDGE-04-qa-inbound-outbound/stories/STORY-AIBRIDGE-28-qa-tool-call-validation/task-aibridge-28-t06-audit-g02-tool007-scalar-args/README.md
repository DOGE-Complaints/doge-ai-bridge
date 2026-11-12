# Task: test — TOOL-007 scalar args sibling (G-02)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_28_audit_20260917`  
**Gap:** G-02 (Low) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-28-qa-tool-call-validation-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-28-qa-tool-call-validation.md`](../STORY-AIBRIDGE-28-qa-tool-call-validation.md)  
**P5 scaffold:** 2026-09-17T19:13:12Z  
**P6 closed:** 2026-09-17T19:15:26Z  
**Gate:** [acceptance-verification-task-aibridge-28-t06-audit-g02-tool007-scalar-args.md](./acceptance-verification-task-aibridge-28-t06-audit-g02-tool007-scalar-args.md) PASS  

## Purpose

Cover TOOL-007 **scalar** sibling (guide: array/scalar): generate `tool-fc-args-scalar` envelope into package `fixtures/` then promote=**copy** to `tests/fixtures/openai/`; parametrize reject assert alongside `tool-fc-args-array` (`JSON object` / scalar). Keep array case. **No** live Telegram / Railway invent.

## AC/DoD

- [x] Package + copy `tool-fc-args-scalar.json` exist (hash_eq); originals intact.
- [x] Unit assert rejects scalar arguments (parametrize with array).
- [x] Suite still green; no live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- package `fixtures/tool-fc-args-scalar.json` + `tests/fixtures/openai/tool-fc-args-scalar.json` — **P6 Done**
- `tests/unit/test_tool_call_validation.py` — **P6 Done**
