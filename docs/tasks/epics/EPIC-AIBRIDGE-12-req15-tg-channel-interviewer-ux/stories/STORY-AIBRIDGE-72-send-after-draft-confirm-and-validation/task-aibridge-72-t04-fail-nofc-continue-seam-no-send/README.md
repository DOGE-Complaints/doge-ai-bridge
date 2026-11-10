# Task: Fail/no-FC CONTINUE seam · no Send

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md`  
**Parent story:** [`STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md`](../STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md)  
**P1 scaffold:** 2026-11-10T14:53:18Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_72_scaffold_20261110T144725Z.plan.md) · pkg-000075  
**Maps:** t04 · AC-72-01 · AC-72-04 · CONTINUE/Edit · no CONFIRM_SEND

## Purpose

Fail/no-FC path: fail-closed reply + offer_continue_seam; assert no CONFIRM_SEND; gateway_authorized stays False

## Code Facts (verify exists)

- Arch cite: docs/architecture/req15-tg-channel-interviewer-ux/05 §2–3
- STORY-71 Done: Confirm/Edit always Present (hard-dep).
- Post-confirm engine → validate → Send on `/actions`: Present (P3 harness).
- Honesty: no invent stash on interpret · no new TokenActionKind · Keep REQ-11 · 56/68/70/71 regression · no invent Railway/live SUCCESS · GPT ROL-07 OOS.

## AC/DoD

- [x] AC-72-01 · AC-72-04 · CONTINUE/Edit · no CONFIRM_SEND DoD met or Explicit Partial honesty recorded.
- [x] Touch limited to: `offer_continue_seam`
- [x] OOS respected: Premature Send invent
- [x] Skill python-pro present.
- [x] No invent stash / TokenActionKind / Railway/live SUCCESS.

## Where to change (P3)

- `offer_continue_seam`

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story72 (+56/68/70/71) as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-72-t04-fail-nofc-continue-seam-no-send.md`](./acceptance-verification-task-aibridge-72-t04-fail-nofc-continue-seam-no-send.md)

## Implementation (P3)

- **Result:** Done · 2026-11-10T15:01:32Z
- **Evidence:** confirm.offer_continue_seam · channel.run_post_interpretation_confirm_chain
- **Note:** fail/no-FC/no-engine → offer_continue_seam · no CONFIRM_SEND
- **Honesty:** no invent stash/TokenActionKind/live SUCCESS · Keep REQ-11 · GPT ROL-07 OOS
