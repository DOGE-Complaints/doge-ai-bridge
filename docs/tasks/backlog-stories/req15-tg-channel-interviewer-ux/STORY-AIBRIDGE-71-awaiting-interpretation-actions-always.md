# STORY-AIBRIDGE-71 — Awaiting interpretation always has Confirm/Edit actions

## Meta
- **Key:** `STORY-AIBRIDGE-71-awaiting-interpretation-actions-always`
- **Status:** 🟢 **Product Done · Code Done** · pkg-000074 · P8 · 2026-11-10T14:34:54Z · next **DONE** · H-01 WAIVE · [pipeline](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-71-awaiting-interpretation-actions-always/STORY-AIBRIDGE-71-awaiting-interpretation-actions-always.md)
- **Package:** [`INDEX.md`](INDEX.md) · `req15-tg-channel-interviewer-ux` (residual reopen)
- **Tech-arch:** [`04-awaiting-interpretation-always-actions.md`](../../../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md) · [`00-overview`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) · peer [`03`](../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md)
- **Parent product:** REQ15 channel interview UX · peer Keep [`REQ-11`](../../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md)
- **Peer Done:** [`STORY-AIBRIDGE-68`](STORY-AIBRIDGE-68-channel-seam-send-actions-always.md) · [`STORY-AIBRIDGE-70`](STORY-AIBRIDGE-70-send-claim-requires-actions.md)
- **Evidence:** [`req15-tg-interviewer-citizen-conversation-gap-2026-11-10.md`](../../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-gap-2026-11-10.md) §3.3 / §4.5 · [north star](../../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-north-star-2026-11-10.md) · [handoff log-note](../../../../../docs/analysis/req15-tg-interview-2026-11-10-handoff-chain-log-note.md) · transcript [`2026-11-10-pille-handoff-chain`](../../../../../docs/analysis/tg-interview-transcripts/req15-tg-interview-dialogue-2026-11-10-pille-handoff-chain.md)
- **Depends:** Soft: 68/70 Done (Keep mint paths Present; this story = live residual)
- **Downstream:** [`STORY-AIBRIDGE-72`](STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md) hard-deps this story
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)
- **Emitted:** 2026-11-10 · Tech-arch + subtasks: 2026-11-10
- **Delivery class:** arch + Implementation + technical subtasks Present · **P3 runtime Present** (harness) · Code Done ≠ invent live Pass · no invent live TG / Railway SUCCESS

## Scope (requirements)

1. When the confirm FSM state is `awaiting_interpretation_confirm` and a channel turn response would otherwise have **empty** `actions`, the `/v1/channel/turns` success payload **MUST** include Telegram-renderable **Confirm** and **Edit** actions for draft approval (Cancel Keep if already part of that offer bundle).
2. That obligation **MUST** hold on ordinary free-text turns — remint **MUST NOT** depend only on Send-claim or vague-«интерфейс» markers (STORY-70 residual miss Observed 2026-11-10: `needs_control=False` · `actions_count=0`).
3. The story **MUST NOT** authorize minting **Send** confirm or inventing stash without the Keep freeze / REQ-11 send-ready path.
4. Server remains the only owner of action mint; model prose must not substitute for missing CTAs (peer ROL-07).

## Out of scope

- Send-after-validate sequencing — **STORY-AIBRIDGE-72**.  
- GPT roles instruction rewrite / role-theater ban — **STORY-GPT-ROL-07**.  
- Telegram keyboard rendering Keep (Present).  
- Language picker (STORY-69 Done).  
- Gateway/SPA redesign; invent live TG / Railway SUCCESS (H-01 WAIVE).  
- NL rewrite of `reply_text`.  
- Invent live TG / Railway SUCCESS.

## Acceptance (product)

| ID | Criterion |
|----|-----------|
| AC-71-01 | Any success channel turn while FSM is `awaiting_interpretation_confirm` with otherwise empty `actions` returns nonempty Confirm+Edit (Cancel Keep) actions |
| AC-71-02 | AC-71-01 holds without requiring Send-claim or vague-interface markers in `reply_text` |
| AC-71-03 | No Send confirm / stash invent solely to satisfy empty-actions remint |
| AC-71-04 | REQ-11 Keep: stash still only via authorized Send consume path |

## Verified current state (honesty)

| Fact | Status | Cite |
|------|--------|------|
| STORY-68/70 Code Done | **Present** | package INDEX |
| `offer_interpretation_confirm` remint without FSM hop | **Present** | `confirm.offer_interpretation_confirm` |
| Claim/vague remint via `_ensure_control_surface` when `needs_control` | **Present** (STORY-70 Keep) | `coordinator._ensure_control_surface` · arch `03` |
| Early state-invariant remint before marker gate | **Present** (P3 · harness) | `_ensure_control_surface` step 0 · arch [`04`](../../../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md) |
| Comment honesty for interpret-await remint | **Present** (P3 flipped) | `coordinator.build_turn_from_engine` |
| Live 13:37–13:45 same session (pre-71 deploy) | `state=awaiting_interpretation_confirm` · `actions_count=0` · TG `has_actions=False` | gap 2026-11-10 · H-01 WAIVE ≠ invent Pass |
| North-star draft approve CTA in live Observed | **Absent** until redeploy/smoke | H-01 WAIVE |

## Desired

Citizen stuck in draft-approval FSM always sees Confirm/Edit in chat — without coaching free-text or waiting for Send-claim prose.

## Implementation (target)

Order mirrors arch [`04`](../../../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md). **No** invent Send/stash · **no** NL rewrite v1.

1. **Policy lock** — empty `actions` + `AWAITING_INTERPRETATION_CONFIRM` → always remint Confirm/Edit; marker-independence = AC-71-02.
2. **`coordinator._ensure_control_surface`** — **early** branch (before `needs_control_surface` return): if awaiting interpret ∧ actions empty → `offer_interpretation_confirm`.
3. **Flip comment** — remove/rewrite «AWAITING_* — do not re-mint» for interpretation await; Keep FC-less mint for `INTERVIEWING` / `INTERPRETATION_CONFIRMED`.
4. **Wire** — all `build_turn_from_engine` exits still hit ensure (or early path); Keep STORY-70 claim remint for other states.
5. **Tests** — awaiting interpret + plain reply + no markers → Confirm+Edit; no `CONFIRM_SEND`; 68/70 regression green.
6. **Docs** — thin runtime note; INDEX/arch honesty; no claim live Pass without smoke.

## Code points
- `src/aibridge/coordinator.py` (`_ensure_control_surface` · `build_turn_from_engine`)
- `src/aibridge/confirm.py` (Keep `offer_interpretation_confirm`)
- `src/aibridge/seam_policy.py` (policy comment / classify note if needed)
- `tests/test_story_68_*` · `tests/test_story_70_*` · new STORY-71 harness

## Technical subtasks (arch-bound; pre-P1.3)

| ID | Subtask | Arch cite | AC / DoD | Touch (as-is) | OOS | Status |
|----|---------|-----------|----------|---------------|-----|--------|
| **t01** | Arch `04` policy: state-invariant remint; cite claim-gate miss | [`04` §1–2](../../../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md) | AC-71-02 policy | arch `04` · story Implementation | Overbroad remint invent | **Done** (docs) |
| **t02** | `_ensure_control_surface`: early remint awaiting interpret when actions empty (до marker gate) | [`04` §3](../../../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md) | AC-71-01 · AC-71-02 | `coordinator._ensure_control_surface` | Invent CONFIRM_SEND | **Done** (P3) |
| **t03** | Flip/remove «AWAITING_* do not re-mint» для interpret; Keep FC-less mint paths | [`04` §3](../../../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md) | AC-71-01 | `coordinator.build_turn_from_engine` | Change send-await policy invent | **Done** (P3) |
| **t04** | Wire: все exits `build_turn_from_engine` покрыты ensure/early path | [`04` §5](../../../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md) | AC-71-01 | `coordinator.py` | Channel OpenAPI redesign | **Done** (P3) |
| **t05** | Harness: awaiting interpret + plain reply + empty + **no** markers → Confirm+Edit; no Send | [`04` §4](../../../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md) | AC-71-01…03 | `tests/` | Live TG invent | **Done** (P3 harness) |
| **t06** | Regression: STORY-68/70 suites green | [`01`](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) · [`03`](../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md) | AC-68/70 Keep | `tests/test_story_68_*` · `test_story_70_*` | — | **Done** (P3) |
| **t07** | Thin runtime-docs note (stub ≠ live Pass) | [`04`](../../../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md) · [`00`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) | honesty | `docs/runtime-docs/18-awaiting-interpretation-always-actions.md` | Invent live SUCCESS | **Done** (P3) |
| **t08** | Story gate · package INDEX · arch `00`/`03` cross-link | [`00`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) | Package gate for 71 | [`INDEX.md`](INDEX.md) | Parent Phase F · Code Done invent | **Done** (docs) |

## Dependencies
- Soft: STORY-68 / STORY-70 **Done** (Keep mint + claim remint Present).
- Soft peer: GPT ROL-07 — not required to close AC-71 remint.
- Hard for downstream: STORY-72 waits on this story.

## Related

- Package: [`INDEX.md`](INDEX.md)  
- Peer: [STORY-68](STORY-AIBRIDGE-68-channel-seam-send-actions-always.md) · [STORY-70](STORY-AIBRIDGE-70-send-claim-requires-actions.md) · [STORY-72](STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md)  
- Gap / north star: [citizen gap 2026-11-10](../../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-gap-2026-11-10.md) · [north star](../../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-north-star-2026-11-10.md)  
