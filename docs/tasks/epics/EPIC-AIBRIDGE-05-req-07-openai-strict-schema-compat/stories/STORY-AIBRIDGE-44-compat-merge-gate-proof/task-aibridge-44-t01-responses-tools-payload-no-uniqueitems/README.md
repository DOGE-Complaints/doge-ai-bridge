# Task: test — Responses tools payload no uniqueItems (§5.1 #1 + §11.4)

**Status:** Done · P3 2026-09-24T11:52:39Z  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-44-compat-merge-gate-proof.md`  
**Parent story:** [`STORY-AIBRIDGE-44-compat-merge-gate-proof.md`](../STORY-AIBRIDGE-44-compat-merge-gate-proof.md)  
**P1 scaffold:** 2026-09-24T11:49:26Z  
**P3 closed:** 2026-09-24T11:52:39Z  
**Maps:** TECH-ARCH §5.1 #1 · REQ-07 §11.4 · AC-08

## Purpose

Automated merge-gate proof (fake/recording Responses transport): outbound `/v1/responses` body has no `uniqueItems` under `tools[*].parameters`; Responses-flat function tool; `store:false`; `parallel_tool_calls:false`.

## AC/DoD

- [x] Fake/recording transport asserts no `uniqueItems` anywhere under `tools[*].parameters`.
- [x] §11.4: Responses-flat tool, `store:false`, `parallel_tool_calls:false`.
- [x] No live OpenAI / Telegram invent.
- [x] `Skill declared: test-master` present.

## Where changed

- `tests/test_req07_merge_gate.py` — `test_merge_gate_responses_tools_payload_no_uniqueitems`, `test_merge_gate_assemble_contract_knobs`
