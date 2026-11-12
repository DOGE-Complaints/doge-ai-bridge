# Task: Readyz parity fail-closed + seam

**Status:** Done · P3 2026-11-05T12:02:38Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`  
**Parent story:** [`STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`](../STORY-AIBRIDGE-67-consume-parity-volume-evidence.md)  
**P1 scaffold:** 2026-11-05T11:57:24Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_67_scaffold_20261105T115528Z.plan.md) · pkg-000070  
**Maps:** t04 · AC-06 · AC-05 gate · L13-2

## Purpose

Wire comparator into deployment/`/readyz` fail-closed; close ROLES_* vs INSTRUCTIONS_* readiness seam.

## Code Facts (verify exists)

- deployment/readiness Present.
- ROLES_* vs INSTRUCTIONS_* seam residual.
- Incomplete fail-closed Present (STORY-64).

## AC/DoD

- [x] Mismatch → fail-closed on ready path.
- [x] Channel content cannot ready-pass without parity when configured.
- [x] No telegram/gateway redesign.
- [x] Skill python-pro present.

## Where to change (P3)

- deployment.py · readiness.py · config.py · app.py

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story67 as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-67-t04-readyz-parity-fail-closed-seam.md`](./acceptance-verification-task-aibridge-67-t04-readyz-parity-fail-closed-seam.md)
