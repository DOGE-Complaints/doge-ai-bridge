# Task: G-02 WAIVER lift or re-scope note

**Status:** Done · P3 2026-11-04T13:14:19Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md`  
**Parent story:** [`STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md`](../STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md)  
**P1 scaffold:** 2026-11-04T13:06:36Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_65_scaffold_20261104T130109Z.plan.md) · pkg-000068  
**Maps:** t05 · STORY-65 · AC-3

## Purpose

Lift G-02 WAIVER with wire evidence or operator re-scope note + thin runtime honesty.

## Code Facts (verify exists)

- Modules Present: `semantic_state/`, `roles/` (62–64 harness Done).
- Channel: `app.py` `/v1/channel/turns` → `channel.process_turn` — G-02 not yet lifted on product path.
- Dual-confirm Keep: `confirm.invalidate_send_permission` Present.

## AC/DoD

- [x] G-02 WAIVER lifted or explicitly re-scoped with operator note.
- [x] Runtime/docs honesty Present.
- [x] Skill declared: python-pro present.
- [x] OOS 66/67/GPT-48 preserved.

## Where changed (P3)

- runtime 12 + REQ-13 G-02 Lifted

## Where to change (P3)

- `docs/runtime-docs/` · REQ-13 Status note · wire evidence cites

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story65 / keep 62/63 as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-65-t05-g02-waiver-lift-or-rescope-note.md`](./acceptance-verification-task-aibridge-65-t05-g02-waiver-lift-or-rescope-note.md)
