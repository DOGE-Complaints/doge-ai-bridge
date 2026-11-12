# Task: test — Gate 2 duplicate houses + invalid_function_parameters fixture (§5.1 #3+#5)

**Status:** Done · P3 2026-09-24T11:52:39Z  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-44-compat-merge-gate-proof.md`  
**Parent story:** [`STORY-AIBRIDGE-44-compat-merge-gate-proof.md`](../STORY-AIBRIDGE-44-compat-merge-gate-proof.md)  
**P1 scaffold:** 2026-09-24T11:49:26Z  
**P3 closed:** 2026-09-24T11:52:39Z  
**Maps:** TECH-ARCH §5.1 #3 · #5 · T-UNIQUE · AC-08

## Purpose

Merge-gate proof: Gate 2 rejects duplicate `houses`. Regression fixture for prior `invalid_function_parameters` / uniqueItems path.

## AC/DoD

- [x] Gate 2 rejects duplicate `houses` in merge-gate suite.
- [x] Regression fixture: `tests/fixtures/openai/invalid_function_parameters_uniqueitems.json`
- [x] No invent live OpenAI as sole proof.
- [x] `Skill declared: test-master` present.

## Where changed

- `tests/test_req07_merge_gate.py` — gate2 + fixture tests
- `tests/fixtures/openai/invalid_function_parameters_uniqueitems.json`
