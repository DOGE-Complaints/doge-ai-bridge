# Send after draft confirm + validation (STORY-72 / EPIC-12)

Thin runtime note — **Adapt** on Present STORY-68/71 dual-confirm. Detail SSOT:

- Arch: [`../architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md`](../architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md)
- Hard-dep: [`18-awaiting-interpretation-always-actions.md`](./18-awaiting-interpretation-always-actions.md) (STORY-71)

## What landed (P3 · 2026-11-10T15:01:32Z)

| Concern | Code | Must |
|---------|------|------|
| Hook flag | `confirm.consume_action_token` CONFIRM_INTERPRETATION | `post_confirm_engine=True`; `actions=[]`; **never** gateway |
| Chain | `channel.run_post_interpretation_confirm_chain` · `process_action` | Outside turn_lock; server-owned prompt; → `build_turn_from_engine` |
| Success | Present validate → persist → `offer_send_confirm` | Send CTAs on **same** `/actions` payload |
| Fail / no-FC / no engine | `offer_continue_seam` | CONTINUE/Edit · **no** CONFIRM_SEND · no gateway |
| Free-text | Keep REQ-11 | «отправляй» ≠ mint Send / stash |
| Stash | CONFIRM_SEND consume only | Keep · no invent on interpret |

## Honesty

- Code/harness Done ≠ invent Railway / live TG SUCCESS.
- No new TokenActionKind · no invent stash on interpret.
- GPT ROL-07 OOS. Regression 56/68/70/71 must stay green.

## Verify harness

`tests/test_story_72_send_after_draft_confirm_and_validation.py` + `tests/test_story_56_*` + `68` + `70` + `71`.
