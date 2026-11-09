# Task: seam_policy Send-claim gate

**Status:** Done · P3 2026-11-09T11:36:43Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-70-send-claim-requires-actions.md`  
**Parent story:** [`STORY-AIBRIDGE-70-send-claim-requires-actions.md`](../STORY-AIBRIDGE-70-send-claim-requires-actions.md)  
**P1 scaffold:** 2026-11-09T11:33:00Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_70_scaffold_20261109T113113Z.plan.md) · pkg-000073  
**Maps:** t02 · AC-70-01 · AC-70-02 · reply_claims_send_control + needs_control_surface

## Purpose

Detect Send-claim; expand needs_control_surface = (vague ∨ send-claim) ∧ empty actions ∧ no URL

## Code Facts (verify exists)

- Arch cite: docs/architecture/req15-tg-channel-interviewer-ux/03 §2
- STORY-68 Present: vague «интерфейс» · `_ensure_control_surface` · send after FC freeze.
- Send-claim markers / remint on AWAITING_INTERPRETATION_CONFIRM: Absent until implement.
- Honesty: no invent stash · no NL rewrite v1 · Keep REQ-11 · STORY-68 regression · no invent Railway/live TG SUCCESS · GPT invent-named-CTA OOS.

## AC/DoD

- [x] AC-70-01 · AC-70-02 · reply_claims_send_control + needs_control_surface DoD met or Explicit Partial honesty recorded.
- [x] Touch limited to: seam_policy.py
- [x] OOS respected: NL rewrite
- [x] Skill python-pro present.
- [x] No invent stash / NL rewrite / Railway/live TG SUCCESS.

## Where to change (P3)

- seam_policy.py

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story70 (+68) as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-70-t02-seam-policy-send-claim-gate.md`](./acceptance-verification-task-aibridge-70-t02-seam-policy-send-claim-gate.md)

### P3 evidence (2026-11-09T11:36:43Z)

- src/aibridge/seam_policy.py · needs_control_surface
- test_t02_needs_control_surface_send_claim_and_url_exempt
