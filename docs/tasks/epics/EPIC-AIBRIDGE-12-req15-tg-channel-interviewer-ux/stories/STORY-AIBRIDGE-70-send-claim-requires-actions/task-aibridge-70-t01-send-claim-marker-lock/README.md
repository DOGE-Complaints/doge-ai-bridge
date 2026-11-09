# Task: Send-claim marker lock

**Status:** Done · P3 2026-11-09T11:36:43Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-70-send-claim-requires-actions.md`  
**Parent story:** [`STORY-AIBRIDGE-70-send-claim-requires-actions.md`](../STORY-AIBRIDGE-70-send-claim-requires-actions.md)  
**P1 scaffold:** 2026-11-09T11:33:00Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_70_scaffold_20261109T113113Z.plan.md) · pkg-000073  
**Maps:** t01 · AC-70-02 · RU/EN Send-claim list · false-positive fence

## Purpose

Lock Send-claim marker list (RU/EN); document false-positive fence

## Code Facts (verify exists)

- Arch cite: docs/architecture/req15-tg-channel-interviewer-ux/03 §2
- STORY-68 Present: vague «интерфейс» · `_ensure_control_surface` · send after FC freeze.
- Send-claim markers / remint on AWAITING_INTERPRETATION_CONFIRM: Absent until implement.
- Honesty: no invent stash · no NL rewrite v1 · Keep REQ-11 · STORY-68 regression · no invent Railway/live TG SUCCESS · GPT invent-named-CTA OOS.

## AC/DoD

- [x] AC-70-02 · RU/EN Send-claim list · false-positive fence DoD met or Explicit Partial honesty recorded.
- [x] Touch limited to: arch `03` · story Implementation
- [x] OOS respected: Overbroad «отправ» invent
- [x] Skill python-pro present.
- [x] No invent stash / NL rewrite / Railway/live TG SUCCESS.

## Where to change (P3)

- arch `03` · story Implementation

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story70 (+68) as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-70-t01-send-claim-marker-lock.md`](./acceptance-verification-task-aibridge-70-t01-send-claim-marker-lock.md)

### P3 evidence (2026-11-09T11:36:43Z)

- src/aibridge/seam_policy.py · SEND_CLAIM_MARKERS
- test_t01_send_claim_markers_lock_and_false_positive_fence
