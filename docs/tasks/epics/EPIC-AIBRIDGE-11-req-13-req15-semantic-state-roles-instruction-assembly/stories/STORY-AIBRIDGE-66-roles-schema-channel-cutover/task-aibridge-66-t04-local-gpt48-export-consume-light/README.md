# Task: Local GPT-48 export consume (light)

**Status:** Done · P3 2026-11-04T13:51:20Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-66-roles-schema-channel-cutover.md`  
**Parent story:** [`STORY-AIBRIDGE-66-roles-schema-channel-cutover.md`](../STORY-AIBRIDGE-66-roles-schema-channel-cutover.md)  
**P1 scaffold:** 2026-11-04T13:44:52Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_66_scaffold_20261104T134107Z.plan.md) · pkg-000069  
**Maps:** t04 · STORY-66 · Scope-2 · AC-2 · V8-light

## Purpose

Local MVP: configure paths to Present GPT UI `instructions-roles/` and prove light consume vs export inventory. **No invent** bodies. **OOS** Railway volume (STORY-67).

## Code Facts (verify exists)

- Export Present: `GPT UI/instructions-roles/roles.manifest.json` + role md files.
- Fixture Present: `tests/fixtures/content/roles.manifest.json` (≠ invent GPT UI checkout).
- AC-05 live/hash SSOT remains Explicit Partial / Open joint GPT-48 (honesty Keep).

## AC/DoD

- [x] Local consume Pass vs Present export inventory (MVP light).
- [x] No invent instruction bodies · no invent Railway SUCCESS.
- [x] Evidence distinguishes fixture vs GPT UI export path.
- [x] Skill declared: python-pro present.

## Where to change (P3)

- tests focused story66 local consume · docs/runtime note · env example pointing at export mount

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story66 local consume
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-66-t04-local-gpt48-export-consume-light.md`](./acceptance-verification-task-aibridge-66-t04-local-gpt48-export-consume-light.md)
