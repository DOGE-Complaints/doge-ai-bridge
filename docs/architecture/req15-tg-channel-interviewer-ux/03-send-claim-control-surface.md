# Send-claim control surface (residual after STORY-68)

**Overview:** [`00-overview.md`](./00-overview.md)  
**Story:** [`STORY-AIBRIDGE-70`](../../tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-70-send-claim-requires-actions.md)  
**Peer Done:** [`01-channel-seam-send-actions.md`](./01-channel-seam-send-actions.md) (STORY-68) · Keep [`../req15-dual-confirm-handoff/01-keep-pipe-boundaries.md`](../req15-dual-confirm-handoff/01-keep-pipe-boundaries.md)  
**Evidence:** [`../../../../docs/analysis/tg-interview-transcripts/req15-tg-interview-dialogue-2026-11-09-pille.md`](../../../../docs/analysis/tg-interview-transcripts/req15-tg-interview-dialogue-2026-11-09-pille.md)

---

## 1) Present foundation after STORY-68 (cite)

| Piece | Status | Path |
|-------|--------|------|
| Seam mint FC-less | **Present** | `coordinator._mint_fcless_seam_actions` · `seam_policy.classify_fcless_seam` |
| Send after FC freeze | **Present** | `offer_send_confirm` in `build_turn_from_engine` |
| Vague «интерфейс» gate | **Present** | `VAGUE_INTERFACE_MARKERS` · `needs_control_surface` · `_ensure_control_surface` |
| Send-claim markers («действие **Send**») | **Present** (STORY-70 P3) | `seam_policy.SEND_CLAIM_MARKERS` · `reply_claims_send_control` |
| Re-offer on `AWAITING_INTERPRETATION_CONFIRM` when new turn has empty actions | **Present** (STORY-70 P3) | `_ensure_control_surface` remint order |
| NL rewrite of reply | **Absent** (v1 Keep Absent) | — |

---

## 2) Detection policy (target)

| Class | Markers (casefold; literal list locked at implement — not invent overbroad «отправ») | Gate |
|-------|----------------------------------------------------------------------------------------|------|
| Vague UI (Keep 68) | `интерфейс`, `in the interface`, `in the ui` | ∪ |
| **Send-claim (70)** | Phrases that assert an **in-chat Send/submit control is available**, e.g. `действие send`, `действию send`, `действие **send**`, `через … send`, `action send`, `send button` | ∪ |

`needs_control_surface(reply, actions, continuation_url)` → **True** when (vague ∨ send-claim) ∧ `actions` empty ∧ no `continuation_url`.

Do **not** treat ordinary interview words about «отправка» without naming an in-chat **Send** control as a claim (avoid false remint).

---

## 3) Remint order (FSM)

When gate fires:

| Priority | Session condition | Remint |
|----------|-------------------|--------|
| 1 | `AWAITING_SEND_CONFIRM` + frozen intent + not send-blocked | `offer_send_confirm` |
| 2 | `AWAITING_INTERPRETATION_CONFIRM` | **Re-offer** `offer_interpretation_confirm` (same-turn keyboard) |
| 3 | FC-less non-seamless (`INTERVIEWING` / `INTERPRETATION_CONFIRMED`) | `_mint_fcless_seam_actions` (interpret or CONTINUE/Edit) |
| 4 | Terminal / cannot mint | **No** invent stash / **no** invent Send tokens |

Prefer remint CTAs on **this** turn response (Telegram keyboard on latest message). Prose rewrite of `reply_text` = **v1 Absent**.

---

## 4) Trust / coexistence

| Must | Must not |
|------|----------|
| Server mints via Present action-token store | Model-owned gateway stash |
| Send buttons only when Keep send-ready path allows | Mint `CONFIRM_SEND` without freeze/validate |
| CONTINUE / interpret remint when Send not legal | Overload interpret as Send |
| Soft peer: GPT invent-named-CTA ban | Claim instruction rewrite Done in this residual |

---

## 5) Touchpoints (implement)

| Concern | Module |
|---------|--------|
| Markers + `needs_control_surface` | `seam_policy.py` Adapt |
| Remint order + wire all engine exits | `coordinator._ensure_control_surface` · `build_turn_from_engine` |
| Offers | `confirm.py` Keep (`offer_send_confirm` · `offer_interpretation_confirm` · `offer_continue_seam`) |
| Tests | Send-claim empty → remint; vague Keep; 68 regression; no stash invent |
