# Task: implement — `load_content_bundle` smoke against full dump

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md`  
**Parent story:** [`STORY-AIBRIDGE-20-full-instructions-manifest.md`](../STORY-AIBRIDGE-20-full-instructions-manifest.md)  
**P1 scaffold:** 2026-09-16T12:28:09Z  
**P3 Done:** 2026-09-16T12:32:27Z  
**Maps:** Target #3 · ADR-2 load

## Purpose

Prove `load_content_bundle` succeeds against `src/instructions/` + the full manifest; `assembled_instructions` and hashes non-empty. Do not change loader schema.

## Code Facts (verified exists — P1)

1. `load_content_bundle` / `LoadedContentBundle.assembled_instructions`: `src/aibridge/content.py`.
2. Pack path for `pack_hash` is separate `pack_schema_path` (settings); payload JSON also listed in `files[]` for assembly.

## AC/DoD

- [x] Load succeeds against dir + full manifest.
- [x] Hashes / assembled text non-empty.
- [x] `Skill declared: python-pro` present.

## Where to change

`tests/` in P3 (not P1). Loader only if a real schema bug blocks load — do not invent nested-path support.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest tests/ -q -k 'story_20 or load_content or manifest' --tb=short
```
