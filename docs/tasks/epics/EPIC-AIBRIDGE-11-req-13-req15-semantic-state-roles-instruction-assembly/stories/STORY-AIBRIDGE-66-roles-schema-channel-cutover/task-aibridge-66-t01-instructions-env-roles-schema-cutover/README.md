# Task: Instructions env → roles-schema cutover

**Status:** Done · P3 2026-11-04T13:51:20Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-66-roles-schema-channel-cutover.md`  
**Parent story:** [`STORY-AIBRIDGE-66-roles-schema-channel-cutover.md`](../STORY-AIBRIDGE-66-roles-schema-channel-cutover.md)  
**P1 scaffold:** 2026-11-04T13:44:52Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_66_scaffold_20261104T134107Z.plan.md) · pkg-000069  
**Maps:** t01 · STORY-66 · Scope-1 · AC-1 · REQ-13 §3b env

## Purpose

Cutover env SSOT: `DOGESTONIA_INSTRUCTIONS_DIR` / `_MANIFEST` (and align/unify `DOGESTONIA_ROLES_*` residual) → roles-schema manifest; product path ≠ Phase-A-only.

## Code Facts (verify exists)

- Config Present: `config.py` `DOGESTONIA_INSTRUCTIONS_*` + optional `DOGESTONIA_ROLES_*` (STORY-65).
- Roles assembly Present: `roles/assembly.py` validates `bundle_version`/`core`/`roles.*`.
- Export Present: `GPT UI/instructions-roles/roles.manifest.json`.
- Phase-A residual: `content.py` still requires `files[]`.

## AC/DoD

- [x] Product env points at roles-schema as live SSOT (REQ-13 §3b).
- [x] Dual env ambiguity on channel path reduced/aligned (ROLES_* residual documented or unified).
- [x] No invent instruction bodies · OOS Railway-67.
- [x] Skill declared: python-pro present.

## Where to change (P3)

- `src/aibridge/config.py` · `.env.example` · app bind of instructions/roles paths

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story66
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-66-t01-instructions-env-roles-schema-cutover.md`](./acceptance-verification-task-aibridge-66-t01-instructions-env-roles-schema-cutover.md)
