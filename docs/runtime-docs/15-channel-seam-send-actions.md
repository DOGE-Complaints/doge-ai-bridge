# Channel seam CTAs + Send actions always (STORY-68 / EPIC-12)

Thin runtime note — **Adapt** on Present REQ-11 Keep pipe. Detail SSOT:

- Arch: [`../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md`](../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md)
- Keep pipe: [`04-confirm-gateway-keep-pipe.md`](./04-confirm-gateway-keep-pipe.md)

## What changed (P3 · 2026-11-06T12:08:29Z)

| Concern | Code | Must |
|---------|------|------|
| Seam policy matrix | `seam_policy.py` | Non-seamless FC-less states → actions; free-text «дальше» not sole path |
| CONTINUE kind | `action_tokens.TokenActionKind.CONTINUE` | Mint/hash store Adapt; ≠ interpret · ≠ send |
| Offer continue | `confirm.offer_continue_seam` | CONTINUE + Edit; no FSM offer transition |
| Consume continue | `confirm.consume_action_token` | Resume interview; **never** stash / gateway |
| Emit on seams | `coordinator.build_turn_from_engine` | INTERVIEWING → interpret; INTERPRETATION_CONFIRMED → continue/edit |
| Send-ready | `offer_send_confirm` after freeze | Always CTAs; no free-text «отправляй» sole path |
| Vague «интерфейс» | `needs_control_surface` | Require actions **or** post-stash `continuation_url` |
| Stash | CONFIRM_SEND → `execute_stash` only | REQ-11 Keep |

## Honesty

- Code/harness Done ≠ live TG / Railway SUCCESS (no invent).
- CONTINUE ≠ stash.
- STORY-69 / GPT ROL-05/06 OOS this wave.

## Verify harness

`tests/test_story_68_channel_seam_send_actions.py` (t01–t07 matrix).
