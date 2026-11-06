# Task: Ban vague «интерфейс» without control

**Status:** Done · P3 2026-11-06T12:08:29Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-68-channel-seam-send-actions-always.md`  
**Parent story:** [`STORY-AIBRIDGE-68-channel-seam-send-actions-always.md`](../STORY-AIBRIDGE-68-channel-seam-send-actions-always.md)  
**P1 scaffold:** 2026-11-06T12:01:54Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_68_scaffold_20261106T115910Z.plan.md) · pkg-000071  
**Maps:** t06 · AC-68-03

## Purpose

no vague UI claim without actions or post-stash continuation_url

## Code Facts (verify exists)

- Arch cite: 01 §4
- ChannelAction / offer_send_confirm / offer_interpretation_confirm Present (REQ-11 Keep).
- Generic CONTINUE kind Absent until t02.
- Honesty: Keep stash · CONTINUE ≠ stash · no invent live SUCCESS.

## AC/DoD

- [x] AC-68-03 DoD met or Explicit Partial honesty recorded.
- [x] Touch limited to: coordinator/channel policy
- [x] OOS respected: ML text filter invent
- [x] Skill python-pro present.
- [x] No invent Railway/live TG SUCCESS · no CONTINUE→stash.

## Where to change (P3)

- coordinator/channel policy

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story68 as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-68-t06-ban-vague-interface-without-control.md`](./acceptance-verification-task-aibridge-68-t06-ban-vague-interface-without-control.md)

### P3 evidence (2026-11-06T12:08:29Z)

- seam_policy.needs_control_surface · coordinator _ensure_control_surface · test_t06
- vague «интерфейс» without actions/URL → mint CTAs
