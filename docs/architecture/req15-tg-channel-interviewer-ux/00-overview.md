# REQ15 TG channel interviewer UX — target technical architecture (overview)

| Field | Value |
|-------|--------|
| **Focus** | Channel turn CTAs at non-seamless stages + Send confirm always when send-ready; session language-pick actions + locale persist — residual UX on Keep dual-confirm pipe |
| **Parent product** | [`REQ15`](../../../../docs/requirements%20backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md) · package [`../../tasks/backlog-stories/req15-tg-channel-interviewer-ux/INDEX.md`](../../tasks/backlog-stories/req15-tg-channel-interviewer-ux/INDEX.md) |
| **Peers Keep** | [`../req15-dual-confirm-handoff/00-overview.md`](../req15-dual-confirm-handoff/00-overview.md) · [`../runtime/03-confirm-gateway.md`](../runtime/03-confirm-gateway.md) · [`../runtime/01-channel-facade.md`](../runtime/01-channel-facade.md) |
| **Soft peers** | GPT UI ROL-05/06 (instruction prose) · doge-telegram ChannelAction render Keep |
| **UX evidence** | [`../../../../docs/analysis/req15-tg-interviewer-target-ux-2026-11-06.md`](../../../../docs/analysis/req15-tg-interviewer-target-ux-2026-11-06.md) · [triage](../../../../docs/analysis/req15-tg-interviewer-ux-gap-triage-2026-11-06.md) |
| **Story scope** | [`STORY-AIBRIDGE-68…69`](../../tasks/backlog-stories/req15-tg-channel-interviewer-ux/INDEX.md) |
| **Recorded** | 2026-11-06 |
| **Mode** | Target technical architecture — not implementation tasks |
| **Slug** | `req15-tg-channel-interviewer-ux` |
| **Layout** | system (`00` + concern docs) |

**Levels:** product AC in STORYs 68/69 · this folder = how coordinator/tokens/session locale coexist with Keep pipe · work items = backlog tech subtasks (not invent code here).

**Siblings:** [`01-channel-seam-send-actions.md`](./01-channel-seam-send-actions.md) · [`02-session-language-locale.md`](./02-session-language-locale.md)

---

## 1) Context & functional vs tech split

| Layer | Lives in | Content |
|-------|----------|---------|
| Product / AC | STORY-68 · STORY-69 · parent REQ15 UX notes | Goals 2/3/4 · AC-68-* · AC-69-* |
| Keep pilot tech | `runtime/03-confirm-gateway` · `req15-dual-confirm-handoff` | Dual-confirm · stash · SPA URL |
| Channel contract | OpenAPI channel v1 · `schemas.ChannelAction` | label · opaque token · style |
| Target tech (this package) | `docs/architecture/req15-tg-channel-interviewer-ux/` | Seam CONTINUE · send-ready CTA invariant · locale picker + ConfirmSession locale |
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
  → CONFIRM_SEND consume → execute_stash → continuation_url (Keep)
```

| Concern | Doc |
|---------|-----|
| Seam + Send CTAs | [`01`](./01-channel-seam-send-actions.md) |
| Language pick + session locale | [`02`](./02-session-language-locale.md) |

---

## 3) Coexistence / honesty

| Must Keep | Must not |
|-----------|----------|
| REQ-11 Send consume → gateway stash only | Model-owned stash / invent gateway URL in prose |
| Present ChannelAction contract | Redesign OpenAPI token fields for this residual |
| Telegram label→keyboard passthrough | Separate telegram STORY for flag strings |
| Interpretation / Send / Edit / Cancel offers Present | Claim stage-invariant CTAs already Done |

**Verified gap (analysis.mdc):** generic CONTINUE kind **Absent**; late turns may return `actions=[]` while prose coaches «дальше» / «интерфейс»; session locale picker **Absent** (`language_code` mapped inbound, unused in engine).

---

## 4) Story map

| Story | Arch | AC |
|-------|------|-----|
| STORY-68 | [`01`](./01-channel-seam-send-actions.md) | AC-68-01…04 |
| STORY-69 | [`02`](./02-session-language-locale.md) | AC-69-01…04 |
