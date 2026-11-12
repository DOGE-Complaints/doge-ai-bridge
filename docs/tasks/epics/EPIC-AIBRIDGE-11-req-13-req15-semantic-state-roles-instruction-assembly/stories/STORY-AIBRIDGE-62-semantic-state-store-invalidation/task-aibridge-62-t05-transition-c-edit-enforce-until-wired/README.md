# Task: Transition C EDIT enforce until store wired

**Status:** Done · P3 2026-11-02T08:45:23Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-62-semantic-state-store-invalidation.md`  
**Parent story:** [`STORY-AIBRIDGE-62-semantic-state-store-invalidation.md`](../STORY-AIBRIDGE-62-semantic-state-store-invalidation.md)  
**P1 scaffold:** 2026-11-02T08:41:40Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_62_scaffold_20261102T083726Z.plan.md) · pkg-000065  
**Maps:** t05 · STORY-62

## Purpose

Keep apply_edit → invalidate Present until semantic store e2e; do not remove C early.

## AC/DoD

- [x] apply_edit still enforces invalidate (confirm.py:441–445).
- [x] Transition C remains Present until store wired e2e.
- [x] Skill declared: python-pro present.

## Where changed (P3)

- `confirm.py:apply_edit` regression in story 62 tests

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-62-t05-transition-c-edit-enforce-until-wired.md`](./acceptance-verification-task-aibridge-62-t05-transition-c-edit-enforce-until-wired.md)
