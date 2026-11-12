# Task: Hybrid-C volume runbook

**Status:** Done · P3 2026-11-05T12:02:38Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`  
**Parent story:** [`STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`](../STORY-AIBRIDGE-67-consume-parity-volume-evidence.md)  
**P1 scaffold:** 2026-11-05T11:57:24Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_67_scaffold_20261105T115528Z.plan.md) · pkg-000070  
**Maps:** t06 · AC-AIB-13-04 docs

## Purpose

Hybrid-C runbook: volume path/env · manual publish · reconcile arch 03 with runtime/02; image-baked = fixture/dev (L13-2).

## Code Facts (verify exists)

- runtime 11/13 Present.
- L13-2 volume/fixture lock.
- Automatic CI sync OOS (V3 rejected).

## AC/DoD

- [x] Runbook/runtime note documents volume/env + image-baked honesty.
- [x] No invent Railway SUCCESS.
- [x] Skill python-pro present.

## Where to change (P3)

- docs/runtime-docs/ (+ thin ops note as needed)

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story67 as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-67-t06-hybrid-c-volume-runbook.md`](./acceptance-verification-task-aibridge-67-t06-hybrid-c-volume-runbook.md)
