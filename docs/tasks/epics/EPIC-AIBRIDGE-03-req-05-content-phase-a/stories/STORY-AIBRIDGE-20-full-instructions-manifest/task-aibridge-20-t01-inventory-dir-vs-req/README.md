# Task: inventory — `src/instructions/` vs REQ-05 §4.2 layers

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md`  
**Parent story:** [`STORY-AIBRIDGE-20-full-instructions-manifest.md`](../STORY-AIBRIDGE-20-full-instructions-manifest.md)  
**P1 scaffold:** 2026-09-16T12:28:09Z  
**P3 Done:** 2026-09-16T12:32:27Z  
**Maps:** Scope #1 · TECH ADR-2 completeness

## Purpose

Inventory every root-child in `src/instructions/` (except `instructions.manifest.json`) against REQ-05 §4.2 layer list. Do not invent files. Output is the ordered candidate `files[]` for t02.

## Code Facts (verified exists — P1)

1. Current manifest = 6-file subset: `src/instructions/instructions.manifest.json`.
2. Dir has ~25 root-children besides the manifest (P1 draft count).
3. Loader root-child-only: `src/aibridge/content.py` `_reject_path`.
4. Layer order SSOT: REQ-05 §4.2 / TECH §6 (not `ls` наугад).

## AC/DoD

- [x] Inventory lists every root-child except the manifest, mapped to §4.2 layers.
- [x] No invented filenames; no nested paths.
- [x] `Skill declared: python-pro` present.

## Where to change

Docs note in this task folder and/or comment in t02 README; **P3** writes the JSON (not P1).

## Verification commands

```bash
ls -1 doge-ai-bridge/src/instructions/
python3 -c "import json; print(json.load(open('doge-ai-bridge/src/instructions/instructions.manifest.json'))['files'])"
```
