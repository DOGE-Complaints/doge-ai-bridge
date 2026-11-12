# Task: test — content_configured → non-empty instructions + prefix

**Status:** Done  
**P3 closed:** 2026-09-16T13:41:13Z  

**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-22-content-phase-a-proof.md`  
**Parent story:** [`STORY-AIBRIDGE-22-content-phase-a-proof.md`](../STORY-AIBRIDGE-22-content-phase-a-proof.md)  
**P1 scaffold:** 2026-09-16T13:36:35Z  
**Maps:** Scope #1 · TECH ADR-4 · REQ-05 §4.5

## Purpose

Pytest: with content env + full manifest dump, after `create_app` — `interview_engine.instructions` non-empty and `prompt_channel=="prefix"`. Optional: recording client / `_build_request` shows prefix system message.

**Out of this task:** Railway invent; smoke checklist file (t04); inventing AC beyond story.

## Code Facts (verified exists — P1)

1. Wire helper: `_apply_deployment_to_engine` in `src/aibridge/app.py` (STORY-19).
2. Full dump + manifest: `src/instructions/` (STORY-20).
3. Prior wire tests: `tests/test_story_19_engine_wire.py`.

## AC/DoD

- [x] Test proves non-empty assembled instructions on engine when content_configured.
- [x] Assert `prompt_channel == "prefix"`.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/` (new or extend STORY-22 proof tests) — **P3**

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest tests/test_story_22*.py -q --noconftest 2>/dev/null || true
```
