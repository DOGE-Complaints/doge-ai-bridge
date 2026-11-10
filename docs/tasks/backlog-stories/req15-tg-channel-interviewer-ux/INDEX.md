# req15-tg-channel-interviewer-ux — INDEX

> **Пакет:** REQ15 Telegram channel interviewer UX residual (seam/Send CTAs + session language pick + Send-claim + north-star CTA sequence)  
> **Parent product:** [`REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md`](../../../../../docs/requirements%20backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md)  
> **Peer Keep pipe:** [`REQ-11`](../../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) · package [`../req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md`](../req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md) **exhausted** (56–58 Done) — this package is **residual**, not reopen Keep  
> **Architecture:** [`../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) (`01` seam/Send · `02` locale · `03` Send-claim · `04` awaiting-interpret always · `05` post-confirm validate→Send)  
> **UX evidence:** [citizen gap](../../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-gap-2026-11-10.md) · [north star](../../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-north-star-2026-11-10.md) · [handoff-chain](../../../../../docs/analysis/req15-tg-interview-2026-11-10-handoff-chain-log-note.md) · prior [Pille gap](../../../../../docs/analysis/req15-tg-interviewer-ux-gap-pille-2026-11-06.md) · [triage](../../../../../docs/analysis/req15-tg-interviewer-ux-gap-triage-2026-11-06.md)  
> **Emitted:** 2026-11-06 · **Updated:** 2026-11-10T16:23:38Z — STORY-72 **Product/Code Done** pkg-000075 · P8 · H-01 WAIVE · next DONE  
> **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)  
> **Honesty:** 68–72 Code Done · tip honest · no invent stash/TokenActionKind/live SUCCESS · Code Done ≠ live Pass · H-01 WAIVE

## Stories

| Status | Key | Title | Depends |
|--------|-----|-------|---------|
| 🟢 **Product Done · Code Done** · pkg-000071 · P8 | STORY-AIBRIDGE-68-channel-seam-send-actions-always | [Seam + Send actions always](STORY-AIBRIDGE-68-channel-seam-send-actions-always.md) · [pipeline](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-68-channel-seam-send-actions-always/STORY-AIBRIDGE-68-channel-seam-send-actions-always.md) | REQ-11 Keep (56–58 Done) |
| 🟢 **Product Done · Code Done** · pkg-000072 · P8 | STORY-AIBRIDGE-69-session-language-pick-actions | [Session language pick actions](STORY-AIBRIDGE-69-session-language-pick-actions.md) · [pipeline](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-69-session-language-pick-actions/STORY-AIBRIDGE-69-session-language-pick-actions.md) | Soft independent of 68 |
| 🟢 **Product Done · Code Done** · pkg-000073 · P8 | STORY-AIBRIDGE-70-send-claim-requires-actions | [Send claim requires actions](STORY-AIBRIDGE-70-send-claim-requires-actions.md) · [pipeline](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-70-send-claim-requires-actions/STORY-AIBRIDGE-70-send-claim-requires-actions.md) | Hard: 68 Done · arch [`03`](../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md) |
| 🟢 **Product Done · Code Done** · pkg-000074 · P8 · H-01 WAIVE | STORY-AIBRIDGE-71-awaiting-interpretation-actions-always | [Awaiting interpretation always has Confirm/Edit](STORY-AIBRIDGE-71-awaiting-interpretation-actions-always.md) · [pipeline](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-71-awaiting-interpretation-actions-always/STORY-AIBRIDGE-71-awaiting-interpretation-actions-always.md) · arch [`04`](../../../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md) | Soft: 68/70 Done · live residual |
| 🟢 **Product Done · Code Done** · pkg-000075 · P8 · H-01 WAIVE | STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation | [Send after draft confirm + validation](STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md) · [pipeline](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation/STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md) · arch [`05`](../../../architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md) | Hard: **71** Done |

## Build order

`68` → `69` → `70` → `71` → `72` **Done** (pkg-000075 · P8). Soft peer GPT [`ROL-07`](../../../../../GPT-UI/docs/tasks/backlog-stories/req15-tg-interviewer-roles-ux/STORY-GPT-ROL-07-citizen-surface-no-role-theater.md) OOS · H-01 live smoke WAIVE.

## Out of package

- GPT ROL-05/06/07 (roles package)  
- Telegram ops redact LF  
- Model-owned archive stash restore  
- Gateway/SPA redesign  
- Live TG / Railway SUCCESS invent · invent Send/stash · NL rewrite reply_text v1  
- GPT ROL-07 (roles package)  
