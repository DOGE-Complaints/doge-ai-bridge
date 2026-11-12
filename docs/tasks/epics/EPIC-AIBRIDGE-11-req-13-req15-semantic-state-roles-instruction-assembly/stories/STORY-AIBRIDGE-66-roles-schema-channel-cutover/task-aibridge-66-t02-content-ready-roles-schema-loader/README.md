# Task: Content/ready roles-schema loader

**Status:** Done · P3 2026-11-04T13:51:20Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-66-roles-schema-channel-cutover.md`  
**Parent story:** [`STORY-AIBRIDGE-66-roles-schema-channel-cutover.md`](../STORY-AIBRIDGE-66-roles-schema-channel-cutover.md)  
**P1 scaffold:** 2026-11-04T13:44:52Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_66_scaffold_20261104T134107Z.plan.md) · pkg-000069  
**Maps:** t02 · STORY-66 · Scope-1 · AC-1 · readiness

## Purpose

Adapt content/deployment/ready loader to accept roles-schema live; `files[]` not required for product ready after cutover (Phase-A remains legacy/dev path).

## Code Facts (verify exists)

- `content.py` `load_manifest` requires non-empty `files[]`.
- `deployment.py` / `readiness.py` consume `LoadedContentBundle`.
- Roles-schema loader Present in `roles/assembly.py` (harness/fixture).

## AC/DoD

- [x] Channel/ready can load roles-schema (`bundle_version`/`core`/`roles.*`) as live SSOT.
- [x] Product ready does not require Phase-A `files[]` after cutover.
- [x] Fail-closed on incomplete/mismatched roles-schema (keep spirit AC-AIB-13-06 local).
- [x] Skill declared: python-pro present.

## Where to change (P3)

- `src/aibridge/content.py` · `deployment.py` · `readiness.py` · registry bind as needed

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story66
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-66-t02-content-ready-roles-schema-loader.md`](./acceptance-verification-task-aibridge-66-t02-content-ready-roles-schema-loader.md)
