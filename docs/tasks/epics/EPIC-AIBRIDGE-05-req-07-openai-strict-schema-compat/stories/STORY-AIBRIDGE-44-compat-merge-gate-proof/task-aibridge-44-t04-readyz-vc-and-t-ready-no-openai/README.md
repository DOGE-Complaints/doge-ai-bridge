# Task: test — readyz VC fail-closed + T-READY without OpenAI (§5.1 #4)

**Status:** Done · P3 2026-09-24T11:52:39Z  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-44-compat-merge-gate-proof.md`  
**Parent story:** [`STORY-AIBRIDGE-44-compat-merge-gate-proof.md`](../STORY-AIBRIDGE-44-compat-merge-gate-proof.md)  
**P1 scaffold:** 2026-09-24T11:49:26Z  
**P3 closed:** 2026-09-24T11:52:39Z  
**Maps:** TECH-ARCH §5.1 #4 · T-READY · `validation_context_not_bound`

## Purpose

Merge-gate proof: missing/invalid ValidationContext → `/readyz` not_ready. T-READY without OpenAI from `/readyz`.

## AC/DoD

- [x] Missing VC → `/readyz` 503 + `validation_context_not_bound`.
- [x] No OpenAI calls from `/readyz` (RecordingResponsesClient call count unchanged).
- [x] `schema_validation_complete()` True locally.
- [x] `Skill declared: test-master` present.

## Where changed

- `tests/test_req07_merge_gate.py` — `test_merge_gate_readyz_vc_not_bound`, `test_merge_gate_t_ready_schema_validation_complete_no_openai`
