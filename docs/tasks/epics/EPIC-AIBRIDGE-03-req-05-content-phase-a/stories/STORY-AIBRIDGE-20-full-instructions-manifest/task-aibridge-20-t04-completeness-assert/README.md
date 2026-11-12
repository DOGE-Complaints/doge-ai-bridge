# Task: implement — completeness assert (dir set == files set)

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md`  
**Parent story:** [`STORY-AIBRIDGE-20-full-instructions-manifest.md`](../STORY-AIBRIDGE-20-full-instructions-manifest.md)  
**P1 scaffold:** 2026-09-16T12:28:09Z  
**P3 Done:** 2026-09-16T12:32:27Z  
**Maps:** Target #1 · REQ-05 §4.2 omit = FAIL

## Purpose

Assert `set(files) == set(dir children) − {instructions.manifest.json}` so omit of any root-child is FAIL. Channel OAS must **not** appear in `files[]`.

## Code Facts (verified exists — P1)

1. Completeness rule: TECH §6 / REQ-05 §4.2.
2. Manifest lists only root children (`content.py` `_reject_path`).

## AC/DoD

- [x] Test or check fails if any root-child (except the manifest) is omitted from `files[]`.
- [x] No extra invented names in `files[]`.
- [x] `Skill declared: python-pro` present.

## Where to change

`tests/` in P3 (not P1).

## Verification commands

```bash
# P3: pytest asserting dir listing vs manifest.files
```
