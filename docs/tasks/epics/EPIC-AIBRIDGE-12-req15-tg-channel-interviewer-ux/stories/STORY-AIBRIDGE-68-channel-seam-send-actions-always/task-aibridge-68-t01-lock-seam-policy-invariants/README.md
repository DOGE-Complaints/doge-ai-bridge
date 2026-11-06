# Task: Lock seam policy invariants

**Status:** Done · P3 2026-11-06T12:08:29Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-68-channel-seam-send-actions-always.md`  
**Parent story:** [`STORY-AIBRIDGE-68-channel-seam-send-actions-always.md`](../STORY-AIBRIDGE-68-channel-seam-send-actions-always.md)  
**P1 scaffold:** 2026-11-06T12:01:54Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_68_scaffold_20261106T115910Z.plan.md) · pkg-000071  
**Maps:** t01 · AC-68-01 policy

## Purpose

which stages non-seamless; free-text «дальше» not sole path

## Code Facts (verify exists)

- Arch cite: docs/architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md §2
- ChannelAction / offer_send_confirm / offer_interpretation_confirm Present (REQ-11 Keep).
- Generic CONTINUE kind Absent until t02.
- Honesty: Keep stash · CONTINUE ≠ stash · no invent live SUCCESS.

## AC/DoD

- [x] AC-68-01 policy DoD met or Explicit Partial honesty recorded.
- [x] Touch limited to: Thin product/arch matrix at implement
- [x] OOS respected: GPT prose rewrite
- [x] Skill python-pro present.
- [x] No invent Railway/live TG SUCCESS · no CONTINUE→stash.

## Where to change (P3)

- Thin product/arch matrix at implement

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story68 as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-68-t01-lock-seam-policy-invariants.md`](./acceptance-verification-task-aibridge-68-t01-lock-seam-policy-invariants.md)

### P3 evidence (2026-11-06T12:08:29Z)

- src/aibridge/seam_policy.py · tests/test_story_68_channel_seam_send_actions.py::test_t01_seam_policy_matrix
- NON_SEAMLESS_FCLESS_STATES + classify matrix locked
