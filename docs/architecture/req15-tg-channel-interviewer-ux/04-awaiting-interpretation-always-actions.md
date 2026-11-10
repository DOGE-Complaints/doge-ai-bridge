# Awaiting interpretation — always Confirm/Edit actions

**Overview:** [`00-overview.md`](./00-overview.md)  
**Story:** [`STORY-AIBRIDGE-71`](../../tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-71-awaiting-interpretation-actions-always.md)  
**Peer Done:** [`01-channel-seam-send-actions.md`](./01-channel-seam-send-actions.md) (STORY-68) · [`03-send-claim-control-surface.md`](./03-send-claim-control-surface.md) (STORY-70 claim-gated remint)  
**Keep:** [`../req15-dual-confirm-handoff/01-keep-pipe-boundaries.md`](../req15-dual-confirm-handoff/01-keep-pipe-boundaries.md)  
**Evidence:** [`../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-gap-2026-11-10.md`](../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-gap-2026-11-10.md) §4.5 · [north star](../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-north-star-2026-11-10.md) · [handoff log-note](../../../../docs/analysis/req15-tg-interview-2026-11-10-handoff-chain-log-note.md)

---

## 1) Present foundation (cite)

| Piece | Status | Path |
|-------|--------|------|
| `offer_interpretation_confirm` remint without FSM hop when already awaiting | **Present** (STORY-70) | `confirm.offer_interpretation_confirm` |
| Claim/vague remint via `_ensure_control_surface` | **Present** (STORY-70) | fires when `needs_control_surface` |
| **Early** state-invariant remint before marker gate | **Present** (STORY-71 P3) | `_ensure_control_surface` step 0 |
| `SeamKind.AWAITING_ACTION` for `AWAITING_INTERPRETATION_CONFIRM` | **Present** | `seam_policy.classify_fcless_seam` |
| FC-less mint only for `INTERVIEWING` / `INTERPRETATION_CONFIRMED` | **Present** | `requires_fcless_actions` / `NON_SEAMLESS_FCLESS_STATES` |
| Comment honesty for interpret-await remint | **Present** (STORY-71 P3) | `coordinator.build_turn_from_engine` (flipped) |
| Live 2026-11-10: awaiting interpret + empty actions every turn | **Observed residual** (pre-71 deploy) | gap §3.3 / §4.5 · `needs_control=False` |

**Target vs claim-gate:** arch `03` claim remint remains; STORY-71 adds unconditional remint when already awaiting interpret + empty actions.

---

## 2) Policy (target) — state-invariant, not claim-gated

| Rule | Target |
|------|--------|
| When FSM is `AWAITING_INTERPRETATION_CONFIRM` and a success channel turn would otherwise have **empty** `actions` | **MUST** remint `offer_interpretation_confirm` (Confirm / Edit / Cancel Keep) |
| Marker independence | Remint **MUST NOT** depend on Send-claim or vague-«интерфейс» markers (AC-71-02) |
| Same-turn keyboard | Prefer CTAs on **this** turn response (Telegram on latest message) |
| NL rewrite of `reply_text` | **v1 Absent** |

Relation to arch [`03`](./03-send-claim-control-surface.md): claim/vague gate remains for other states and Send-claim prose. For **interpret-await**, STORY-71 is **stricter** — unconditional when actions empty.

---

## 3) Remint placement (FSM)

In `coordinator._ensure_control_surface` (**Present** STORY-71 P3):

| Order | Condition | Action |
|-------|-----------|--------|
| **0 (early, before marker gate)** | `AWAITING_INTERPRETATION_CONFIRM` ∧ `actions` empty | `offer_interpretation_confirm` — **unconditional** |
| Then | existing `needs_control_surface` early-return | Keep STORY-70 claim path for other cases |
| 1…4 | remint order from arch `03` §3 | Keep (send-ready / interpret-under-claim / FC-less / terminal) |

Product comment for interpret-await remint flipped (STORY-71). Do **not** invent Send on this path.

---

## 4) Trust / coexistence

| Must | Must not |
|------|----------|
| Server remint via Present `offer_interpretation_confirm` | Mint `CONFIRM_SEND` / invent stash solely to fill empty actions |
| Keep Cancel in interpret offer bundle | Overload interpret as Send |
| Soft peer ROL-07 (no role-theater prose) | Claim live TG SUCCESS from docs-only |

---

## 5) Touchpoints (implement)

| Concern | Module |
|---------|--------|
| Early unconditional remint | `coordinator._ensure_control_surface` |
| Comment / FC-less path honesty | `coordinator.build_turn_from_engine` |
| Offer Keep | `confirm.offer_interpretation_confirm` |
| Policy docs / optional classify note | `seam_policy.py` (comment or doc only unless code needs classify tweak) |
| Tests | awaiting interpret + plain reply + no markers → Confirm+Edit; no Send; 68/70 regression |

---

## 6) Downstream

Post-confirm validate→Send sequence = [`05-send-after-draft-confirm-validate.md`](./05-send-after-draft-confirm-validate.md) / **STORY-72** (hard-dep this arch).
