# Task: Harness parity matrix

**Status:** Done · P3 2026-11-05T12:02:38Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`  
**Parent story:** [`STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`](../STORY-AIBRIDGE-67-consume-parity-volume-evidence.md)  
**P1 scaffold:** 2026-11-05T11:57:24Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_67_scaffold_20261105T115528Z.plan.md) · pkg-000070  
**Maps:** t05 · tech accept AC-05/06

## Purpose

Harness: pass · missing · changed hash · bad inventory · manifest drift (after t02).

## Code Facts (verify exists)

- Fixture patterns from STORY-64 Present.
- E1 lock via t02.

## AC/DoD

- [x] Focused tests cover pass/missing/changed/bad/drift.
- [x] Fixtures ≠ invent GPT UI checkout bodies.
- [x] No live volume mount required.
- [x] Skill python-pro present.

## Where to change (P3)

- tests/ + tests/fixtures/…

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story67 as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-67-t05-harness-parity-matrix.md`](./acceptance-verification-task-aibridge-67-t05-harness-parity-matrix.md)
