# REQ15 TG channel interviewer UX — target technical architecture (overview)

| Field | Value |
|-------|--------|
| **Focus** | Channel turn CTAs at non-seamless stages + Send confirm when send-ready; session language-pick; Send-claim remint; state-invariant interpret-await CTAs; post-confirm validate→Send — residual UX on Keep dual-confirm pipe |
| **Parent product** | [`REQ15`](../../../../docs/requirements%20backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md) · package [`../../tasks/backlog-stories/req15-tg-channel-interviewer-ux/INDEX.md`](../../tasks/backlog-stories/req15-tg-channel-interviewer-ux/INDEX.md) |
| **Peers Keep** | [`../req15-dual-confirm-handoff/00-overview.md`](../req15-dual-confirm-handoff/00-overview.md) · [`../runtime/03-confirm-gateway.md`](../runtime/03-confirm-gateway.md) · [`../runtime/01-channel-facade.md`](../runtime/01-channel-facade.md) |
| **Soft peers** | GPT UI ROL-05/06/07 (instruction prose) · doge-telegram ChannelAction render Keep |
| **UX evidence** | [`../../../../docs/analysis/req15-tg-interviewer-target-ux-2026-11-06.md`](../../../../docs/analysis/req15-tg-interviewer-target-ux-2026-11-06.md) · [triage](../../../../docs/analysis/req15-tg-interviewer-ux-gap-triage-2026-11-06.md) · [north star 2026-11-10](../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-north-star-2026-11-10.md) · [citizen gap](../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-gap-2026-11-10.md) |
| **Story scope** | [`STORY-AIBRIDGE-68…72`](../../tasks/backlog-stories/req15-tg-channel-interviewer-ux/INDEX.md) |
| **Recorded** | 2026-11-06 · residual Send-claim: 2026-11-09 · residual north-star CTA: 2026-11-10 |
| **Mode** | Target technical architecture — not implementation tasks |
| **Slug** | `req15-tg-channel-interviewer-ux` |
| **Layout** | system (`00` + concern docs) |

**Levels:** product AC in STORYs 68–72 · this folder = how coordinator/tokens/session locale coexist with Keep pipe · work items = backlog tech subtasks (not invent code here).

**Siblings:** [`01-channel-seam-send-actions.md`](./01-channel-seam-send-actions.md) · [`02-session-language-locale.md`](./02-session-language-locale.md) · [`03-send-claim-control-surface.md`](./03-send-claim-control-surface.md) · [`04-awaiting-interpretation-always-actions.md`](./04-awaiting-interpretation-always-actions.md) · [`05-send-after-draft-confirm-validate.md`](./05-send-after-draft-confirm-validate.md)

---

## 1) Context & functional vs tech split

| Layer | Lives in | Content |
|-------|----------|---------|
| Product / AC | STORY-68…72 · parent REQ15 UX notes · north star | Goals · AC-68…AC-72 |
| Keep pilot tech | `runtime/03-confirm-gateway` · `req15-dual-confirm-handoff` | Dual-confirm · stash · SPA URL |
| Channel contract | OpenAPI channel v1 · `schemas.ChannelAction` | label · opaque token · style |
| Target tech (this package) | `docs/architecture/req15-tg-channel-interviewer-ux/` | Seam CONTINUE · send-ready CTA · locale · Send-claim · interpret-await always · post-confirm validate→Send |
| Work items | backlog STORY tech subtasks | **Not here** |

**Use case:** Telegram user advances interview via **buttons** at seams and send; language is locked for the session when start text is opaque — without model-owned gateway HTTP.

**Packaging:** same aibridge image. Telegram only renders Present `ChannelAction` list (no new telegram STORY for labels).

---

## 2) Target technical architecture (summary)

```text
/v1/channel/turns
  → [69] locale gate (unclear text → lang-pick actions; else continue)
  → coordinator / interview engine
  → [68] seam: non-seamless → CONTINUE and/or EDIT actions
  → send-ready freeze → offer_send_confirm (Keep)
  → [70] if reply claims Send/интерфейс and actions empty → remint by FSM
  → [71] if AWAITING_INTERPRETATION_CONFIRM and actions empty → always remint Confirm/Edit
  → CONFIRM_SEND consume → execute_stash → continuation_url (Keep)

/v1/channel/actions  (CONFIRM_INTERPRETATION)
  → consume → interpretation_confirmed (Keep · no gateway)
  → [72] server-owned engine → build_turn_from_engine
       FC OK → validate → freeze → offer_send_confirm
       else → CONTINUE/Edit (no Send)
```

| Concern | Doc |
|---------|-----|
| Seam + Send CTAs | [`01`](./01-channel-seam-send-actions.md) |
| Language pick + session locale | [`02`](./02-session-language-locale.md) |
| Send-claim control surface | [`03`](./03-send-claim-control-surface.md) |
| Awaiting interpretation always actions | [`04`](./04-awaiting-interpretation-always-actions.md) |
| Send after draft confirm + validate | [`05`](./05-send-after-draft-confirm-validate.md) |

---

## 3) Coexistence / honesty

| Must Keep | Must not |
|-----------|----------|
| REQ-11 Send consume → gateway stash only | Model-owned stash / invent gateway URL in prose |
| Present ChannelAction contract | Redesign OpenAPI token fields for this residual |
| Telegram label→keyboard passthrough | Separate telegram STORY for flag strings |
| Interpretation / Send / Edit / Cancel offers Present | Claim stage-invariant CTAs / post-confirm Send already Code Done |
| STORY-71 early remint Present · STORY-72 post-confirm chain Present (P3 harness) | Invent live TG SUCCESS / Railway Pass |

**Verified (2026-11-10):** STORY-68/69/70/71 Code Done · STORY-72 P3 post-confirm validate→Send Present (harness). Residual deploy/live smoke. Soft peer GPT ROL-07 OOS.

---

## 4) Story map

| Story | Arch | AC |
|-------|------|-----|
| STORY-68 | [`01`](./01-channel-seam-send-actions.md) | AC-68-01…04 |
| STORY-69 | [`02`](./02-session-language-locale.md) | AC-69-01…04 |
| STORY-70 | [`03`](./03-send-claim-control-surface.md) | AC-70-01…04 |
| STORY-71 | [`04`](./04-awaiting-interpretation-always-actions.md) | AC-71-01…04 |
| STORY-72 | [`05`](./05-send-after-draft-confirm-validate.md) | AC-72-01…04 |
