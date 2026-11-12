# Task: Assembly from dir+manifest + session pin

**Status:** Done · P3 2026-11-02T09:16:58Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md`  
**Parent story:** [`STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md`](../STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md)  
**P1 scaffold:** 2026-11-02T09:05:07Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_63_scaffold_20261102T090322Z.plan.md) · pkg-000066  
**Maps:** t03 · STORY-63

## Purpose

Shared core + per-role slice + session pin from DOGESTONIA_INSTRUCTIONS_DIR + manifest.

## AC/DoD

- [x] AC-AIB-13-03: assemble only from configured dir+manifest.
- [x] Session pin of core+role(+node) at start.
- [x] OOS live volume (64).
- [x] Skill declared: python-pro present.

## Where changed (P3)

- `src/aibridge/roles/assembly.py · fixtures roles.manifest.json`

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-63-t03-assembly-dir-manifest-session-pin.md`](./acceptance-verification-task-aibridge-63-t03-assembly-dir-manifest-session-pin.md)
