# req15-tg-channel-interviewer-ux — INDEX

> **Пакет:** REQ15 Telegram channel interviewer UX residual (seam/Send CTAs + session language pick + Send-claim control surface)  
> **Parent product:** [`REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md`](../../../../../docs/requirements%20backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md)  
> **Peer Keep pipe:** [`REQ-11`](../../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) · package [`../req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md`](../req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md) **exhausted** (56–58 Done) — this package is **residual**, not reopen  
> **Architecture:** [`../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) (`01` seam/Send · `02` locale · `03` Send-claim)  
> **UX evidence:** [`docs/analysis/req15-tg-interviewer-ux-gap-pille-2026-11-06.md`](../../../../../docs/analysis/req15-tg-interviewer-ux-gap-pille-2026-11-06.md) · [target](../../../../../docs/analysis/req15-tg-interviewer-target-ux-2026-11-06.md) · [triage](../../../../../docs/analysis/req15-tg-interviewer-ux-gap-triage-2026-11-06.md) · transcript [`2026-11-09-pille`](../../../../../docs/analysis/tg-interview-transcripts/req15-tg-interview-dialogue-2026-11-09-pille.md)  
> **Emitted:** 2026-11-06 · **Updated:** 2026-11-09T11:46:08Z — P8 STORY-70 Product/Code Done · package exhausted  
> **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)  
> **Honesty:** 68/69/70 Code Done · H-01 live smoke WAIVE · Code Done ≠ live smoke · no invent live SUCCESS

## Stories

| Status | Key | Title | Depends |
|--------|-----|-------|---------|
| 🟢 **Product Done · Code Done** · pkg-000071 · P8 | STORY-AIBRIDGE-68-channel-seam-send-actions-always | [Seam + Send actions always](STORY-AIBRIDGE-68-channel-seam-send-actions-always.md) · [pipeline](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-68-channel-seam-send-actions-always/STORY-AIBRIDGE-68-channel-seam-send-actions-always.md) | REQ-11 Keep (56–58 Done) |
| 🟢 **Product Done · Code Done** · pkg-000072 · P8 | STORY-AIBRIDGE-69-session-language-pick-actions | [Session language pick actions](STORY-AIBRIDGE-69-session-language-pick-actions.md) · [pipeline](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-69-session-language-pick-actions/STORY-AIBRIDGE-69-session-language-pick-actions.md) | Soft independent of 68 |
| 🟢 **Product Done · Code Done** · pkg-000073 · P8 | STORY-AIBRIDGE-70-send-claim-requires-actions | [Send claim requires actions](STORY-AIBRIDGE-70-send-claim-requires-actions.md) · [pipeline](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-70-send-claim-requires-actions/STORY-AIBRIDGE-70-send-claim-requires-actions.md) | Hard: 68 Done · arch [`03`](../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md) |

## Build order

`68` Done → `69` Done → `70` Done · **package exhausted**.

## Out of package

- GPT invent-named-CTA / ROL-05/06  
- Telegram ops redact LF  
- Model-owned archive stash restore  
- Gateway/SPA redesign  
- Live TG / Railway SUCCESS invent · invent stash · NL rewrite reply_text v1  
