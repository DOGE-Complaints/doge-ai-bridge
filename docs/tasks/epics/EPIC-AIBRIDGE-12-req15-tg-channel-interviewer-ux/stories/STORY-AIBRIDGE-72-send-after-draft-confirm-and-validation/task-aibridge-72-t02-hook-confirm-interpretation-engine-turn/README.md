# Task: Hook CONFIRM_INTERPRETATION → engine turn

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md`  
**Parent story:** [`STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md`](../STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md)  
**P1 scaffold:** 2026-11-10T14:53:18Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_72_scaffold_20261110T144725Z.plan.md) · pkg-000075  
**Maps:** t02 · AC-72-02 · server-owned engine after CONFIRM_INTERPRETATION

## Purpose

After successful CONFIRM_INTERPRETATION consume: server-owned InterviewEngine turn → build_turn_from_engine (no citizen free-text)

## Code Facts (verify exists)

- Arch cite: docs/architecture/req15-tg-channel-interviewer-ux/05 §2
- STORY-71 Done: Confirm/Edit always Present (hard-dep).
- Post-confirm engine → validate → Send on `/actions`: Present (P3 harness).
- Honesty: no invent stash on interpret · no new TokenActionKind · Keep REQ-11 · 56/68/70/71 regression · no invent Railway/live SUCCESS · GPT ROL-07 OOS.

## AC/DoD

- [x] AC-72-02 · server-owned engine after CONFIRM_INTERPRETATION DoD met or Explicit Partial honesty recorded.
- [x] Touch limited to: `confirm.py` · `channel.process_action`
- [x] OOS respected: New TokenActionKind
- [x] Skill python-pro present.
- [x] No invent stash / TokenActionKind / Railway/live SUCCESS.

## Where to change (P3)

- `confirm.py` · `channel.process_action`

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story72 (+56/68/70/71) as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-72-t02-hook-confirm-interpretation-engine-turn.md`](./acceptance-verification-task-aibridge-72-t02-hook-confirm-interpretation-engine-turn.md)

## Implementation (P3)

- **Result:** Done · 2026-11-10T15:01:32Z
- **Evidence:** src/aibridge/confirm.py · src/aibridge/channel.py
- **Note:** confirm post_confirm_engine + channel.run_post_interpretation_confirm_chain
- **Honesty:** no invent stash/TokenActionKind/live SUCCESS · Keep REQ-11 · GPT ROL-07 OOS
