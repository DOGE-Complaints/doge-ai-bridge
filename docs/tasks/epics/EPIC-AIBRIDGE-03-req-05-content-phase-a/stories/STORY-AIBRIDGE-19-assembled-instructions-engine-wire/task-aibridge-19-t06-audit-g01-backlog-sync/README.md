# Task: docs — sync backlog Status/AC/verified state (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_19_audit_20260916`  
**Gap:** G-01 (Info) — P4 audit 2026-09-16  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-19-assembled-instructions-engine-wire-20260916.md`  
**Parent story:** [`STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`](../STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md)  
**P5 scaffold:** 2026-09-16T12:17:23Z  
**P6 Done:** 2026-09-16T12:19:26Z

## Purpose

Sync backlog `$storyFile` so nested T01–T05 Status, Target AC checkboxes, and «Verified current state» match pipeline Done + ADR-1 wire (helper + tests). Docs-only.

**Out of this task:** product `src/` edits; GPT UI `05` (G-03 WAIVED); inventing new AC.

## Code Facts (verified exists — post P6)

1. Product wire: `_apply_deployment_to_engine` `src/aibridge/app.py:196–230`; call after deploy assign `app.py:429–433`.
2. Pipeline t01–t05 **Done**; gate PASS 2026-09-16T12:10:09Z; pytest 7 passed.
3. Backlog nested T01–T05 **Done**; verified-state post-wire (this task).

## AC/DoD

- [x] Backlog nested T01–T05 Status = Done; Target AC checked where product PASS.
- [x] «Verified current state» describes post-P3 wire (helper + prefix XOR + fail-closed), not pre-wire Gap.
- [x] Cites helper/tests paths; no product `src/` changes in this task.
- [x] `Skill declared: python-pro` present.

## Where to change

- `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`

## Verification commands (P6)

```bash
rg -n 'Todo|Verified current|290–298|_apply_deployment_to_engine' \
  doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md
```
