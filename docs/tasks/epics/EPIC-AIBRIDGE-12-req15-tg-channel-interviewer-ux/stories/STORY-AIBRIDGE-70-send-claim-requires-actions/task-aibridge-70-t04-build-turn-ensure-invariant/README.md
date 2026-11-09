# Task: build_turn ensure invariant

**Status:** Done · P3 2026-11-09T11:36:43Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-70-send-claim-requires-actions.md`  
**Parent story:** [`STORY-AIBRIDGE-70-send-claim-requires-actions.md`](../STORY-AIBRIDGE-70-send-claim-requires-actions.md)  
**P1 scaffold:** 2026-11-09T11:33:00Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_70_scaffold_20261109T113113Z.plan.md) · pkg-000073  
**Maps:** t04 · AC-70-01 · all build_turn_from_engine exits still call ensure

## Purpose

Confirm all build_turn_from_engine exits still run expanded ensure

## Code Facts (verify exists)

- Arch cite: docs/architecture/req15-tg-channel-interviewer-ux/03 §5
- STORY-68 Present: vague «интерфейс» · `_ensure_control_surface` · send after FC freeze.
- Send-claim markers / remint on AWAITING_INTERPRETATION_CONFIRM: Absent until implement.
- Honesty: no invent stash · no NL rewrite v1 · Keep REQ-11 · STORY-68 regression · no invent Railway/live TG SUCCESS · GPT invent-named-CTA OOS.

## AC/DoD

- [x] AC-70-01 · all build_turn_from_engine exits still call ensure DoD met or Explicit Partial honesty recorded.
- [x] Touch limited to: coordinator.py
- [x] OOS respected: Channel OpenAPI redesign
- [x] Skill python-pro present.
- [x] No invent stash / NL rewrite / Railway/live TG SUCCESS.

## Where to change (P3)

- coordinator.py

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story70 (+68) as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-70-t04-build-turn-ensure-invariant.md`](./acceptance-verification-task-aibridge-70-t04-build-turn-ensure-invariant.md)

### P3 evidence (2026-11-09T11:36:43Z)

- coordinator.build_turn_from_engine all exits call _ensure_control_surface
- t03/t05 harness covers ensure on FC-less + awaiting
