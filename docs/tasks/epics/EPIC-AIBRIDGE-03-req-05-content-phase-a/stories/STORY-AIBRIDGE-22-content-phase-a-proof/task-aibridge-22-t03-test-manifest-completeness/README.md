# Task: test — dir children vs `files[]` completeness

**Status:** Done  
**P3 closed:** 2026-09-16T13:41:13Z  

**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-22-content-phase-a-proof.md`  
**Parent story:** [`STORY-AIBRIDGE-22-content-phase-a-proof.md`](../STORY-AIBRIDGE-22-content-phase-a-proof.md)  
**P1 scaffold:** 2026-09-16T13:36:35Z  
**Maps:** Scope #1 · REQ-05 §4.2 completeness (proof wave)

## Purpose

Pytest: `set(files) == set(dir children) − {instructions.manifest.json}`; omit = fail. May extend or reuse STORY-20 completeness asserts as Phase A proof surface.

**Out of this task:** inventing files outside dump; loader schema change.

## Code Facts (verified exists — P1)

1. Full manifest: `src/instructions/instructions.manifest.json`.
2. Existing completeness: `tests/test_story_20_full_manifest.py`.

## AC/DoD

- [x] Completeness assert present in STORY-22 proof suite (or clearly re-exported/covered).
- [x] Omit of any root-child fails the assert.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/` — **P3**

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest tests/test_story_20_full_manifest.py tests/test_story_22*.py -q --noconftest 2>/dev/null || true
```
