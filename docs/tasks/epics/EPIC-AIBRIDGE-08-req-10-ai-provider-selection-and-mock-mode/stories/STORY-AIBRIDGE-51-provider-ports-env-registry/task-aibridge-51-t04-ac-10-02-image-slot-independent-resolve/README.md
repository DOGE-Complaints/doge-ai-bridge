# Task: AC-10-02 image slot independent

**Status:** Done · P3 2026-10-16T10:49:56Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-51-provider-ports-env-registry.md`  
**Parent story:** [`STORY-AIBRIDGE-51-provider-ports-env-registry.md`](../STORY-AIBRIDGE-51-provider-ports-env-registry.md)  
**P1 scaffold:** 2026-10-16T10:46:25Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_51_scaffold_20261016T104516Z.plan.md)  
**Maps:** AC-10-02

## Purpose

Image slot resolves independently of text.

## AC/DoD

- [x] Gate from Purpose satisfied on disk at P3.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved — module path = implement `src/aibridge/providers/`.
- [x] Siblings 52–55 / channel registry / live vendor not claimed.
- [x] No product invent beyond this task DoD.

## Where to change (P3)

- `src/aibridge/config.py` · `src/aibridge/providers/` · `readiness.py` / `app.py` gates · `tests/test_provider_ports_story_51.py`

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-51-t04-ac-10-02-image-slot-independent-resolve.md`
