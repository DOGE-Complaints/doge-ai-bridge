# Task: implement — Responses-flat tool schema

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-10-responses-adapter-tools.md`  
**Parent story:** [`STORY-AIBRIDGE-10-responses-adapter-tools.md`](../STORY-AIBRIDGE-10-responses-adapter-tools.md)  
**P3 Done:** 2026-09-13T15:46:08Z
**P1 scaffold:** 2026-09-13T15:40:24Z  
**Maps:** Scope #2; AC #2

## Purpose

Emit Responses-flat tool shape (type/name/parameters/strict), not nested Chat Completions function wrapper.

## Code Facts (verified exists — P1)

1. Nested wrap exists — tool_gen.py lines with "function": { ... }.
2. InterviewEngine passes tools into assemble_responses_request — interview.py.

## AC/DoD

- [x] Emitted tool schema is Responses-flat (type/name/parameters/strict).
- [x] No nested Chat Completions function wrapper on production emission path.
- [x] `Skill declared: python-pro` present.

## Where to change

src/aibridge/tool_gen.py

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_story_10_responses_adapter.py -k flat_tool
```
