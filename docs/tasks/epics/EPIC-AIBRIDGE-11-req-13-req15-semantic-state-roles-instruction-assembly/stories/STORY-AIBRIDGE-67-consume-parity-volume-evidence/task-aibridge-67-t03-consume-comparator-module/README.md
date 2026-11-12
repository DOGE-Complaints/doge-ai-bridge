# Task: Consume comparator module

**Status:** Done · P3 2026-11-05T12:02:38Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`  
**Parent story:** [`STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`](../STORY-AIBRIDGE-67-consume-parity-volume-evidence.md)  
**P1 scaffold:** 2026-11-05T11:57:24Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_67_scaffold_20261105T115528Z.plan.md) · pkg-000070  
**Maps:** t03 · AC-AIB-13-05 code

## Purpose

Comparator: mounted inventory/hashes vs locked export artifact; diagnose missing / changed / unexpected.

## Code Facts (verify exists)

- Local hashes Present in content.py.
- Consume comparator Absent.
- E1 lock via t02.

## AC/DoD

- [x] Comparator module Present (path at implement).
- [x] Diagnoses missing/changed/unexpected vs export artifact.
- [x] No invent format · no live Railway run required.
- [x] Skill python-pro present.

## Where to change (P3)

- src/aibridge/content.py (+ new compare helper path at implement)

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story67 as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-67-t03-consume-comparator-module.md`](./acceptance-verification-task-aibridge-67-t03-consume-comparator-module.md)
