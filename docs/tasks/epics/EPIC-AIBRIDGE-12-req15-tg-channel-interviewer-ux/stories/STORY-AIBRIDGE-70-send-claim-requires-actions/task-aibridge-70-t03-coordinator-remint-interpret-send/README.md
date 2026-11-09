# Task: Coordinator remint interpret/send

**Status:** Done · P3 2026-11-09T11:36:43Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-70-send-claim-requires-actions.md`  
**Parent story:** [`STORY-AIBRIDGE-70-send-claim-requires-actions.md`](../STORY-AIBRIDGE-70-send-claim-requires-actions.md)  
**P1 scaffold:** 2026-11-09T11:33:00Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_70_scaffold_20261109T113113Z.plan.md) · pkg-000073  
**Maps:** t03 · AC-70-03 · remint order send-ready / re-offer interpret / FC-less seam

## Purpose

Remint: AWAITING_SEND_CONFIRM→offer_send_confirm; AWAITING_INTERPRETATION_CONFIRM→re-offer interpret; FC-less→seam; else leave

## Code Facts (verify exists)

- Arch cite: docs/architecture/req15-tg-channel-interviewer-ux/03 §3
- STORY-68 Present: vague «интерфейс» · `_ensure_control_surface` · send after FC freeze.
- Send-claim markers / remint on AWAITING_INTERPRETATION_CONFIRM: Absent until implement.
- Honesty: no invent stash · no NL rewrite v1 · Keep REQ-11 · STORY-68 regression · no invent Railway/live TG SUCCESS · GPT invent-named-CTA OOS.

## AC/DoD

- [x] AC-70-03 · remint order send-ready / re-offer interpret / FC-less seam DoD met or Explicit Partial honesty recorded.
- [x] Touch limited to: coordinator._ensure_control_surface
- [x] OOS respected: Invent CONFIRM_SEND without freeze
- [x] Skill python-pro present.
- [x] No invent stash / NL rewrite / Railway/live TG SUCCESS.

## Where to change (P3)

- coordinator._ensure_control_surface

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story70 (+68) as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-70-t03-coordinator-remint-interpret-send.md`](./acceptance-verification-task-aibridge-70-t03-coordinator-remint-interpret-send.md)

### P3 evidence (2026-11-09T11:36:43Z)

- src/aibridge/coordinator.py · confirm.py idempotent offers
- test_t03_awaiting_interpret_send_claim_remints_interpretation · test_t03_awaiting_send_claim_remints_send_confirm
