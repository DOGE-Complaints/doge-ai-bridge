# Task: Live volume evidence (ops window)

**Status:** Partial · P3 2026-11-05T12:02:38Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`  
**Parent story:** [`STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`](../STORY-AIBRIDGE-67-consume-parity-volume-evidence.md)  
**P1 scaffold:** 2026-11-05T11:57:24Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_67_scaffold_20261105T115528Z.plan.md) · pkg-000070  
**Maps:** t07 · AC-05 live · G7

## Purpose

Live evidence (ops window): mount · env (no secrets) · export identity · comparator · /readyz · ≥1 role path · UTC artifact. Without window → **Explicit Partial** · **no invent** SUCCESS.

## Code Facts (verify exists)

- Railway volume evidence Absent.
- Ops window soft dependency.

## AC/DoD

- [x] With window: evidence artifact + UTC Present OR Explicit Partial recorded without invent SUCCESS.
- [x] No secrets in evidence.
- [x] Skill python-pro present.

## Where to change (P3)

- docs/analysis/ or docs/tasks/run-reports/ at implement

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story67 as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-67-t07-live-volume-evidence-ops-window.md`](./acceptance-verification-task-aibridge-67-t07-live-volume-evidence-ops-window.md)
