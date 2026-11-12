# Task: implement — prompt assembly xor

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-10-responses-adapter-tools.md`  
**Parent story:** [`STORY-AIBRIDGE-10-responses-adapter-tools.md`](../STORY-AIBRIDGE-10-responses-adapter-tools.md)  
**P3 Done:** 2026-09-13T15:46:08Z
**P1 scaffold:** 2026-09-13T15:40:24Z  
**Maps:** Scope #3; AC #3

## Purpose

Canonical prompt assembly — stable prefix xor instructions=, never both (R3-P0-13).

## Code Facts (verified exists — P1)

1. Dual path risk — interview.py uses build_stable_prefix and instructions=.
2. assemble_responses_request accepts instructions= — request_assembly.py / responses_client.py.

## AC/DoD

- [x] Prompt assembly never duplicates instructions (prefix xor instructions=).
- [x] Fail-closed or clear single-channel selection documented in code/tests.
- [x] `Skill declared: python-pro` present.

## Where to change

src/aibridge/interview.py, request_assembly.py

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_story_10_responses_adapter.py -k prompt_xor
```
