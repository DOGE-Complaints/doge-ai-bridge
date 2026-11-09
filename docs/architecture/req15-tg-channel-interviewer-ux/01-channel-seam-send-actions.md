# Channel seam CTAs + Send actions always

**Overview:** [`00-overview.md`](./00-overview.md)  
**Story:** [`STORY-AIBRIDGE-68`](../../tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-68-channel-seam-send-actions-always.md)  
**Keep peers:** [`../runtime/03-confirm-gateway.md`](../runtime/03-confirm-gateway.md) · [`../req15-dual-confirm-handoff/01-keep-pipe-boundaries.md`](../req15-dual-confirm-handoff/01-keep-pipe-boundaries.md)

---

## 1) Present foundation (cite)

| Piece | Path |
|-------|------|
| `ChannelAction` | `schemas.py` — `label` · opaque `token` · `style` |
| OpenAPI | `docs/openapi/aibridge-channel-v1.openapi.yaml` actions |
| Token kinds | `action_tokens.TokenActionKind`: `confirm_interpretation` · `confirm_send` · `edit` · `cancel` · **`continue`** (STORY-68 P3 Present) |
| Interpretation offer | `confirm.offer_interpretation_confirm` · coordinator when FC-less + `INTERVIEWING` |
| Send offer | `confirm.offer_send_confirm` · coordinator after validate/freeze pending call |
| Empty actions | Ordinary replies outside that path; engine errors; post-consume turns — often `actions=[]` |
| Telegram render | doge-telegram `outbound.py` — label→button, token→callback_data **Keep** |

---

## 2) Seam policy (target)

| Rule | Target |
|------|--------|
| Non-seamless stage | Interview stage boundary that cannot join silently (before validate / send / edit / explicit continue) **MUST** return ≥1 Telegram-renderable action |
| Free-text «дальше» | **Not** the sole advance path when a seam is non-seamless |
| Continue | **New** `TokenActionKind.CONTINUE` (literal name at implement) — mint on seam; consume → **resume interview** without stash / without meaning-as-confirm |
| Edit | Keep Present `EDIT` on seams that allow revision |
| Interpretation confirm | Keep Present `Looks right` path — **≠** generic CONTINUE (do not overload) |

Concrete stage→action matrix rows = Open at implement (product thin); this arch locks **invariant**: non-seamless ⇒ actions Present.

---

## 3) Send-ready invariant

| When | Must |
|------|------|
| Draft frozen + validated tool intent (Present coordinator happy path) | Always call `offer_send_confirm` → Send / Edit / Cancel actions |
| User | Must not need free-text coaching «отправь» / «отправляй» to obtain Send CTA |
| Stash | Only after `CONFIRM_SEND` consume → `execute_stash` (REQ-11 Keep) |

---

## 4) No vague «интерфейс» without control

| Forbidden | Required instead |
|-----------|------------------|
| Assistant claims submission happens «в интерфейсе» / vague UI with **no** in-chat actions and **no** post-stash URL | (a) Present seam/Send actions on that turn, **or** (b) after successful stash, outbound includes `continuation_url` |

Enforcement = coordinator/channel policy (stage invariant + post-stash URL Keep), not model-owned HTTP.

**Residual (STORY-70):** named **Send/submit claims** without actions/URL — detection + remint FSM → [`03-send-claim-control-surface.md`](./03-send-claim-control-surface.md) (extends this §4; Keep vague markers).

---

## 5) Trust / coexistence

| Must | Must not |
|------|----------|
| Server mints tokens via Present action-token store | Model invents callback tokens or gateway URLs |
| CONTINUE consume stays off gateway path | CONTINUE triggering stash |
| Keep dual-confirm FSM | Reopen gateway/SPA contracts |

---

## 6) Emission / consume touchpoints (implement)

| Concern | Modules (Present homes) |
|---------|-------------------------|
| Kind registry | `action_tokens.py` Adapt |
| Offer / consume | `confirm.py` Adapt |
| Stage emission | `coordinator.py` Adapt · channel turn assembly |
| Contract tests | channel/coordinator harness; telegram passthrough Keep |
