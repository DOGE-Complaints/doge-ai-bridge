# Task: Channel wire assemble default cutover

**Status:** Done · P3 2026-11-04T13:51:20Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-66-roles-schema-channel-cutover.md`  
**Parent story:** [`STORY-AIBRIDGE-66-roles-schema-channel-cutover.md`](../STORY-AIBRIDGE-66-roles-schema-channel-cutover.md)  
**P1 scaffold:** 2026-11-04T13:44:52Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_66_scaffold_20261104T134107Z.plan.md) · pkg-000069  
**Maps:** t03 · STORY-66 · Scope-1 · AC-1 · wire residual

## Purpose

Under cutover env, channel turns assemble from roles-schema by default; ADR-1 mega-string = legacy/dev-only when cutover active. No new HTTP. Keep dual-confirm.

## Code Facts (verify exists)

- STORY-65 Present: `channel_wire.apply_before_engine_turn` + optional roles paths; mega-string Keep when unset.
- `assemble_role_prompt` Present.
- Dual-confirm Keep: `confirm.invalidate_send_permission` Present.

## AC/DoD

- [x] Product channel turns use roles-schema assembly when cutover env set.
- [x] ADR-1 mega-string not live SSOT after cutover (legacy/dev-only).
- [x] No invent HTTP · dual-confirm regression Keep.
- [x] Skill declared: python-pro present.

## Where to change (P3)

- `src/aibridge/channel_wire.py` · `app.py` (bind / ADR-1 interaction)

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story66 + keep dual-confirm smoke
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-66-t03-channel-wire-assemble-default-cutover.md`](./acceptance-verification-task-aibridge-66-t03-channel-wire-assemble-default-cutover.md)
