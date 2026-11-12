# Task: docs — sync backlog «Verified current state» (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_20_audit_20260916`  
**Gap:** G-01 (Info) — P4 audit 2026-09-16  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-20-full-instructions-manifest-20260916.md`  
**Parent story:** [`STORY-AIBRIDGE-20-full-instructions-manifest.md`](../STORY-AIBRIDGE-20-full-instructions-manifest.md)  
**P5 scaffold:** 2026-09-16T12:41:29Z  
**P6 Done:** 2026-09-16T12:47:01Z

## Purpose

Sync backlog `$storyFile` §«Verified current state» so it matches post-P3 full 25-file manifest + §4.2 order + tests (drop stale **6-file subset FAIL** claim). Docs-only.

**Out of this task:** product `src/` edits; loader fail-closed (G-02 WAIVED); `.env` / `.env.example` (G-03 / STORY-21); inventing new AC.

## Code Facts (verified exists — post P6)

1. On-disk manifest: `src/instructions/instructions.manifest.json` — 25 `files[]` in REQ-05 §4.2 order.
2. Pipeline / nested t01–t05 **Done**; gate PASS 2026-09-16T12:32:27Z; pytest 5 passed (`tests/test_story_20_full_manifest.py`).
3. Backlog §Verified updated to post-P3 full dump (this task) — no stale 6-file FAIL claim.

## AC/DoD

- [x] `$storyFile` §«Verified current state» describes post-P3 full dump (25 files + order + tests), not 6-file subset FAIL.
- [x] Cites manifest + test paths; no product `src/` changes in this task.
- [x] `Skill declared: python-pro` present.

## Where to change

- `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md`

## Verification commands (P6)

```bash
rg -n '6-file subset|Verified current|25' \
  doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md
```
