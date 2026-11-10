# Task: Arch 04 policy: state-invariant remint

**Status:** Done · P3 2026-11-10T12:54:14Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-71-awaiting-interpretation-actions-always.md`  
**Parent story:** [`STORY-AIBRIDGE-71-awaiting-interpretation-actions-always.md`](../STORY-AIBRIDGE-71-awaiting-interpretation-actions-always.md)  
**P1 scaffold:** 2026-11-10T12:41:54Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_71_scaffold_20261110T123821Z.plan.md) · pkg-000074  
**Maps:** t01 · AC-71-02 policy · cite claim-gate miss

## Purpose

(see backlog / arch 04)

## Code Facts (verify exists)

- Evidence: docs/architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md
- Honesty: no invent Send/stash · no NL rewrite · Keep REQ-11 · 68/70 regression · no invent Railway/live TG SUCCESS · GPT ROL-07 / invent-named-CTA OOS · STORY-72 OOS.

## AC/DoD

- [x] AC-71-02 policy · cite claim-gate miss DoD met or Explicit Partial honesty recorded.
- [x] Touch limited to: arch `04` · story Implementation
- [x] OOS respected.
- [x] Skill python-pro present.
- [x] No invent Send/stash / NL rewrite / Railway/live TG SUCCESS.

## Where to change (P3)

- arch `04` · story Implementation

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line tests/test_story_71_awaiting_interpretation_actions_always.py tests/test_story_70_send_claim_requires_actions.py tests/test_story_68_channel_seam_send_actions.py
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-71-t01-arch04-policy-state-invariant-remint.md`](./acceptance-verification-task-aibridge-71-t01-arch04-policy-state-invariant-remint.md)

### P3 evidence (2026-11-10T12:54:14Z)

- docs/architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md
- arch 04 Present early remint policy
