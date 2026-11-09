# STORY-AIBRIDGE-70 — Send claim requires in-chat actions

## Meta
- **Key:** `STORY-AIBRIDGE-70-send-claim-requires-actions`
- **Status:** 🟢 **Product Done · Code Done** · pkg-000073 · P8 · 2026-11-09T11:46:08Z · next **DONE** · H-01 live smoke WAIVE · no invent Railway/live SUCCESS · [pipeline](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-70-send-claim-requires-actions/STORY-AIBRIDGE-70-send-claim-requires-actions.md)
- **Package:** [`INDEX.md`](INDEX.md) · `req15-tg-channel-interviewer-ux`
- **Tech-arch:** [`req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md`](../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md) · [`00-overview`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) · peer [`01`](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md)
- **Parent product:** REQ15 channel interview UX · peer Keep [`REQ-11`](../../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md)
- **Peer Done:** [`STORY-AIBRIDGE-68`](STORY-AIBRIDGE-68-channel-seam-send-actions-always.md) (seam/Send on FC freeze · ban «интерфейс» only)
- **Evidence:** transcript [`req15-tg-interview-dialogue-2026-11-09-pille.md`](../../../../../docs/analysis/tg-interview-transcripts/req15-tg-interview-dialogue-2026-11-09-pille.md) · operator screenshot (draft + «действие **Send**», no inline keyboard) · [triage](../../../../../docs/analysis/req15-tg-interviewer-ux-gap-triage-2026-11-06.md)
- **Depends:** STORY-68 **Done** (Keep mint path); this story = residual control-surface gap
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)
- **Emitted:** 2026-11-09 · Tech-arch + subtasks: 2026-11-09
- **Product Done honesty:** Code/docs after t01–t07 + t08; live smoke residual separate. Do not invent Railway / live TG SUCCESS. Soft peer GPT invent-named-CTA = OOS.

## Scope

1. When a channel `reply_text` asserts that an in-chat **Send** / submit control is available (or equivalent draft-ready «переходите к отправке через действие Send»), the `/v1/channel/turns` response **MUST** include Telegram-renderable **actions** appropriate to the confirm FSM — **or** the reply **MUST NOT** claim Send is Present.
2. Expand control-surface policy beyond STORY-68 «интерфейс» markers so **named Send/submit claims** without nonempty `actions` (and without post-stash `continuation_url`) are treated as needing a control surface.
3. Prefer Keep path: Send confirm actions when send-ready (validated FC → freeze → `offer_send_confirm`); otherwise mint interpretation/continue seam CTAs rather than empty actions with Send prose.
4. Server-owned stash remains the only HTTP submit path (REQ-11 Keep). Model must not own gateway stash.

## Out of scope

- Telegram rendering of nonempty `ChannelAction` (Present Keep).  
- GPT UI instruction rewrite / invent-named-CTA ban (soft peer; separate package).  
- Language picker (STORY-69 Done).  
- Gateway/SPA redesign; epic pipeline folders.  
- Runtime implement in this docs wave (other dialog).  
- NL rewrite of `reply_text` (v1 Absent — remint CTAs only).

## Acceptance (product)

| ID | Criterion |
|----|-----------|
| AC-70-01 | No channel turn may claim in-chat Send/submit is available while `actions` is empty and `continuation_url` is absent |
| AC-70-02 | Control-surface policy covers Send/submit **claim** markers (not only «интерфейс») |
| AC-70-03 | When remint is required and FSM allows send-ready Keep path → Send confirm actions; else interpretation/continue seam — never invent stash |
| AC-70-04 | Stash still only via Send consume → gateway (Keep REQ-11) |

## Verified current state (honesty)

| Fact | Status | Cite |
|------|--------|------|
| Send buttons after validated FC freeze | **Present** | `coordinator.build_turn_from_engine` → `offer_send_confirm` |
| Ban vague «интерфейс» without actions/URL | **Present** | `seam_policy.VAGUE_INTERFACE_MARKERS` · `needs_control_surface` · `_ensure_control_surface` |
| Prose «действие Send» without FC / empty keyboard | **Observed gap** | 2026-11-09 transcript |
| Remint on Send-claim markers | **Present** (P3) | `SEND_CLAIM_MARKERS` · `needs_control_surface` |
| Re-offer on `AWAITING_INTERPRETATION_CONFIRM` when new turn has empty actions | **Present** (P3) | `_ensure_control_surface` remint order |
| Telegram append of nonempty actions | **Present** Keep | `doge-telegram` `outbound.inline_keyboard_from_actions` |

## Desired

Draft-ready / send-cue turns either expose real Send (or prior seam) CTAs in the **same** outbound message, or do not name Send as available.

## Implementation (target)

Order mirrors arch [`03`](../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md). **No** invent stash · **no** NL rewrite v1.

1. **Lock markers** — Send-claim set (RU/EN casefold): phrases that assert in-chat **Send** control is available; Keep vague markers; avoid overbroad «отправ» alone.
2. **`seam_policy.py`** — `reply_claims_send_control` (or equivalent); expand `needs_control_surface` = (vague ∨ send-claim) ∧ empty actions ∧ no URL.
3. **`coordinator._ensure_control_surface`** — remint order:
   - `AWAITING_SEND_CONFIRM` + frozen + not blocked → `offer_send_confirm`
   - `AWAITING_INTERPRETATION_CONFIRM` → re-offer `offer_interpretation_confirm`
   - FC-less non-seamless → `_mint_fcless_seam_actions`
   - else → leave (no invent Send/stash)
4. **Wire** — all `build_turn_from_engine` exits already call ensure; keep that invariant after expand.
5. **Tests** — Send-claim + empty actions → remint Send or seam; vague Keep; STORY-68 regression green.
6. **Docs** — thin runtime note; INDEX/arch honesty; no claim live Pass without smoke evidence.

## Code points
- `src/aibridge/seam_policy.py`
- `src/aibridge/coordinator.py` (`_ensure_control_surface` / `build_turn_from_engine`)
- `src/aibridge/confirm.py` (Keep offers)
- `tests/test_story_68_channel_seam_send_actions.py` + new STORY-70 harness

## Technical subtasks (arch-bound; pre-P1.3)

| ID | Subtask | Arch cite | AC / DoD | Touch (as-is) | OOS | Status |
|----|---------|-----------|----------|---------------|-----|--------|
| **t01** | Lock Send-claim marker list (RU/EN); document false-positive fence | [`03` §2](../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md) | AC-70-02 policy | arch `03` · story Implementation | Overbroad «отправ» invent | Done |
| **t02** | `seam_policy`: detect Send-claim; expand `needs_control_surface` | [`03` §2](../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md) | AC-70-01 · AC-70-02 | `seam_policy.py` | NL rewrite | Done |
| **t03** | Coordinator remint: re-offer interpret on `AWAITING_INTERPRETATION_CONFIRM`; Keep send-ready path | [`03` §3](../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md) | AC-70-03 | `coordinator._ensure_control_surface` | Invent CONFIRM_SEND without freeze | Done |
| **t04** | Confirm all `build_turn_from_engine` exits still run expanded ensure | [`03` §5](../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md) | AC-70-01 | `coordinator.py` | Channel OpenAPI redesign | Done |
| **t05** | Harness: Send-claim empty → remint Send or seam; URL exempt; no stash invent | [`03` §3](../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md) | AC-70-01…04 tech | `tests/` | Live TG window invent | Done |
| **t06** | Regression: STORY-68 suite green (vague + FC freeze + CONTINUE) | [`01`](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) | AC-68 Keep | `tests/test_story_68_*` | — | Done |
| **t07** | Thin runtime-docs note (stub ≠ live Pass) | [`03`](../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md) · [`00`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) | honesty | `docs/runtime-docs/` path at implement | Invent live SUCCESS | Done |
| **t08** | Story gate · package INDEX · arch 00/01 cross-link | [`00`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) | Package gate for 70 | [`INDEX.md`](INDEX.md) | Parent Phase F | Done |

## Dependencies
- Hard: STORY-68 **Done**.
- Soft: GPT invent-named-CTA (instruction package) — not required to close AC-70 remint.

## Related

- Package: [`INDEX.md`](INDEX.md)  
- Peer: [STORY-68](STORY-AIBRIDGE-68-channel-seam-send-actions-always.md) · [STORY-69](STORY-AIBRIDGE-69-session-language-pick-actions.md)  
- Transcript: [`2026-11-09-pille`](../../../../../docs/analysis/tg-interview-transcripts/req15-tg-interview-dialogue-2026-11-09-pille.md)  
- Triage: [`req15-tg-interviewer-ux-gap-triage-2026-11-06.md`](../../../../../docs/analysis/req15-tg-interviewer-ux-gap-triage-2026-11-06.md)  
