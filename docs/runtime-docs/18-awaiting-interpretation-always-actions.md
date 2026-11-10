# Awaiting interpretation always actions (STORY-71 / EPIC-12)

Thin runtime note — **Adapt** on Present STORY-70 `_ensure_control_surface`. Detail SSOT:

- Arch: [`../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md`](../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md)
- Peer claim gate: [`17-send-claim-control-surface.md`](./17-send-claim-control-surface.md)

## What landed (P3 · 2026-11-10T12:54:14Z)

| Concern | Code | Must |
|---------|------|------|
| Early remint | `coordinator._ensure_control_surface` step 0 | `AWAITING_INTERPRETATION_CONFIRM` ∧ empty actions → `offer_interpretation_confirm` **before** marker gate |
| Comment honesty | `build_turn_from_engine` FC-less path | interpret await remints via ensure; never invent Send |
| Offer Keep | `confirm.offer_interpretation_confirm` | idempotent when already awaiting |
| Stash | CONFIRM_SEND → gateway only | Keep REQ-11 · **no invent Send/stash** |
| reply_text | unchanged | **no NL rewrite v1** |

## Honesty

- Code/harness Done ≠ invent Railway / live TG SUCCESS.
- STORY-72 (send-after-validate) / GPT ROL-07 OOS this story.
- STORY-68 / STORY-70 regression must stay green.

## Verify harness

`tests/test_story_71_awaiting_interpretation_actions_always.py` + `tests/test_story_70_*` + `tests/test_story_68_*`.
