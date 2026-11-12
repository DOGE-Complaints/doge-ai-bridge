# Task: docs — refresh pipeline + task README Code Facts (G-02)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_19_audit_20260916`  
**Gap:** G-02 (Info) — P4 audit 2026-09-16  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-19-assembled-instructions-engine-wire-20260916.md`  
**Parent story:** [`STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`](../STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md)  
**P5 scaffold:** 2026-09-16T12:17:23Z  
**P6 Done:** 2026-09-16T12:19:26Z

## Purpose

Refresh materialized pipeline §«Verified current state» and t01–t04 README «Code Facts» from pre-wire Gap / old line refs to post-P3 facts (`196–230` / `429–433`). Keep ADR-1 order note. Docs-only.

**Out of this task:** product `src/` edits; GPT UI `05` (G-03 WAIVED); inventing new AC.

## Code Facts (verified exists — post P6)

1. Helper + wire: `src/aibridge/app.py:196–230`, `429–433`.
2. Engine still constructed before `_init_stores` (ADR-1 — no full reorder).
3. Pipeline §Verified + t01–t04 Code Facts refreshed (this task).

## AC/DoD

- [x] Pipeline §Verified current state reflects post-P3 wire; ADR-1 order retained.
- [x] t01–t04 README Code Facts line refs updated (no stale `290–298` as current Gap).
- [x] No product `src/` changes in this task.
- [x] `Skill declared: python-pro` present.

## Where to change

- pipeline story §Verified
- t01–t04 README Code Facts

## Verification commands (P6)

```bash
rg -n '290–298|196–230|429–433|_apply_deployment_to_engine|Verified current' \
  doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-03-req-05-content-phase-a/stories/STORY-AIBRIDGE-19-assembled-instructions-engine-wire/
```
