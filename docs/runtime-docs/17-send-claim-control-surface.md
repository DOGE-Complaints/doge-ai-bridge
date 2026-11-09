# Send-claim control surface (STORY-70 / EPIC-12)

Thin runtime note — **Adapt** on Present STORY-68 ensure path. Detail SSOT:

- Arch: [`../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md`](../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md)
- Peer seam: [`15-channel-seam-send-actions.md`](./15-channel-seam-send-actions.md)

## What landed (P3 · 2026-11-09T11:36:43Z)

| Concern | Code | Must |
|---------|------|------|
| Send-claim markers | `seam_policy.SEND_CLAIM_MARKERS` · `reply_claims_send_control` | Named Send control; **not** bare «отправ» |
| Gate | `needs_control_surface` | (vague ∨ send-claim) ∧ empty actions ∧ no URL |
| Remint | `coordinator._ensure_control_surface` | send-ready → re-offer interpret → FC-less seam → else leave |
| Idempotent offers | `confirm.offer_*` when already awaiting | remint tokens without illegal FSM hop |
| Stash | CONFIRM_SEND → gateway only | Keep REQ-11 · **no invent stash** |
| reply_text | unchanged | **no NL rewrite v1** |

## Honesty

- Code/harness Done ≠ invent Railway / live TG SUCCESS.
- GPT invent-named-CTA instruction package OOS.
- STORY-68 regression must stay green.

## Verify harness

`tests/test_story_70_send_claim_requires_actions.py` + `tests/test_story_68_channel_seam_send_actions.py`.
