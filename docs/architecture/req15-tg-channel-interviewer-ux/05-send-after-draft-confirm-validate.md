# Send after draft confirm + validation

**Overview:** [`00-overview.md`](./00-overview.md)  
**Story:** [`STORY-AIBRIDGE-72`](../../tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md)  
**Hard-dep arch:** [`04-awaiting-interpretation-always-actions.md`](./04-awaiting-interpretation-always-actions.md) (STORY-71)  
**Peer Done:** [`01-channel-seam-send-actions.md`](./01-channel-seam-send-actions.md) (Send mint on send-ready) · Keep [`../req15-dual-confirm-handoff/01-keep-pipe-boundaries.md`](../req15-dual-confirm-handoff/01-keep-pipe-boundaries.md) · [`../runtime/03-confirm-gateway.md`](../runtime/03-confirm-gateway.md)  
**Evidence:** [north star](../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-north-star-2026-11-10.md) §3.4–5 · [citizen gap](../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-gap-2026-11-10.md) §3.4–6

---

## 1) Present foundation (cite)

| Piece | Status | Path |
|-------|--------|------|
| `CONFIRM_INTERPRETATION` consume → `interpretation_confirmed`, `actions=[]` | **Present** | `confirm.consume_action_token` |
| No engine / validate / Send on interpret consume | **Present** (gap vs north star) | `channel.process_action` → consume only |
| FC blocked until `INTERPRETATION_CONFIRMED` (or awaiting send) | **Present** | `coordinator.validate_function_calls` |
| Send after FC validate + freeze | **Present** | `build_turn_from_engine` → `persist_pending_tool` → `offer_send_confirm` |
| FSM `OFFER_SEND` only from `INTERPRETATION_CONFIRMED` | **Present** | `confirm_fsm.py` |
| FC-less after confirm → CONTINUE/Edit (not Send) | **Present** | `seam_policy` · `offer_continue_seam` |
| Premature Send CTA before interpret confirm | **Blocked** Keep | FC gate + FSM |

**Missing for north star:** approve → validate → Send on one control surface after Confirm — citizen must wait for a later `/turns` that happens to carry a validated FC.

---

## 2) Target sequence (post-confirm server chain)

```text
POST /v1/channel/actions  (Looks right / CONFIRM_INTERPRETATION)
  → consume: state = interpretation_confirmed · gateway_authorized = False  (Keep)
  → [72] server-owned InterviewEngine turn (no citizen free-text)
  → build_turn_from_engine (Present)
       FC OK  → validate_function_calls → persist_pending_tool → offer_send_confirm
                → actions = Send / Edit / Cancel on same actions response
       no FC / validate fail → fail-closed reply + offer_continue_seam
                → actions = CONTINUE / Edit · no CONFIRM_SEND · no gateway
  → response to channel client
```

| Rule | Target |
|------|--------|
| Send CTA absent until draft interpretation confirmed | Keep (AC-72-01) |
| Send CTA only after validation success **following** that confirm | Post-confirm chain (AC-72-02) |
| Free-text «отправляй» never mints Send / stash | Keep REQ-11 (AC-72-03) |
| Stash / `continuation_url` only via `CONFIRM_SEND` consume | Keep (AC-72-04) |
| New TokenActionKind | **Do not invent** |
| Interpret confirm authorizes gateway | **Forbidden** Keep |

Hard-dep: STORY-71 must land first so the citizen can reach Confirm without empty-actions trap.

---

## 3) Trust / coexistence

| Must | Must not |
|------|----------|
| Reuse Present validate / freeze / `offer_send_confirm` | Invent parallel validate schema |
| Interpret consume stays off gateway path | Soften FC-before-confirm gate |
| Fail-closed → CONTINUE/Edit | Invent Send without freeze |
| Same ChannelAction contract | OpenAPI redesign for this residual |

---

## 4) Touchpoints (implement)

| Concern | Module |
|---------|--------|
| Interpret consume Keep + hook point | `confirm.consume_action_token` (`CONFIRM_INTERPRETATION` branch) |
| Wire post-confirm engine → map | `channel.process_action` (or thin helper called from there) |
| Validate + Send mint | `coordinator.build_turn_from_engine` · `validate_function_calls` · `persist_pending_tool` · `offer_send_confirm` |
| Fail path seam | `confirm.offer_continue_seam` |
| Tests | Confirm → Send only after validate; Confirm alone never Send; FC before confirm blocked; free-text send ≠ stash; dual-confirm / 56/68/70 regression |

---

## 5) Honesty

Docs/arch Present ≠ Code Done ≠ live TG SUCCESS. Implement = separate dialog after STORY-71 runtime.
