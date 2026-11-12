# Task: Channel meaning-change → invalidate send

**Status:** Done · P3 2026-11-04T13:14:19Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md`  
**Parent story:** [`STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md`](../STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md)  
**P1 scaffold:** 2026-11-04T13:06:36Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_65_scaffold_20261104T130109Z.plan.md) · pkg-000068  
**Maps:** t03 · STORY-65 · Scope-3 · L13-3 A

## Purpose

On channel semantic meaning writes → invalidate_send_permission via guard/callback.

## Code Facts (verify exists)

- Modules Present: `semantic_state/`, `roles/` (62–64 harness Done).
- Channel: `app.py` `/v1/channel/turns` → `channel.process_turn` — G-02 not yet lifted on product path.
- Dual-confirm Keep: `confirm.invalidate_send_permission` Present.

## AC/DoD

- [x] Meaning writes on channel call invalidate_send_permission.
- [x] L13-3 Target A live path evidence.
- [x] Skill declared: python-pro present.

## Where changed (P3)

- confirm_guard invalidate on meaning writes

## Where to change (P3)

- `semantic_state/service.py` · `confirm.invalidate_send_permission` · channel wire

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story65 / keep 62/63 as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-65-t03-channel-meaning-invalidate-send.md`](./acceptance-verification-task-aibridge-65-t03-channel-meaning-invalidate-send.md)
