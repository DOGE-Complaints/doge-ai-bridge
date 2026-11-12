# Task: Channel select_next_role + assemble_role_prompt wire

**Status:** Done · P3 2026-11-04T13:14:19Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md`  
**Parent story:** [`STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md`](../STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md)  
**P1 scaffold:** 2026-11-04T13:06:36Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_65_scaffold_20261104T130109Z.plan.md) · pkg-000068  
**Maps:** t02 · STORY-65 · Scope-1 · AC-1

## Purpose

Invoke select_next_role + assemble_role_prompt on /v1/channel/turns product path (not harness-only); Keep InterviewEngine port.

## Code Facts (verify exists)

- Modules Present: `semantic_state/`, `roles/` (62–64 harness Done).
- Channel: `app.py` `/v1/channel/turns` → `channel.process_turn` — G-02 not yet lifted on product path.
- Dual-confirm Keep: `confirm.invalidate_send_permission` Present.

## AC/DoD

- [x] Channel turn invokes role selection + assembly.
- [x] Product path ≠ harness-only.
- [x] InterviewEngine / interview port Keep.
- [x] Skill declared: python-pro present.

## Where changed (P3)

- select_next_role + assemble_role_prompt on turns

## Where to change (P3)

- `src/aibridge/channel.py` · `roles/policy.py` · `roles/assembly.py` · `coordinator.py`

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story65 / keep 62/63 as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-65-t02-channel-select-assemble-role-wire.md`](./acceptance-verification-task-aibridge-65-t02-channel-select-assemble-role-wire.md)
