# STORY-AIBRIDGE-72 — Send after draft confirm and validation

## Meta
- **Key:** `STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation`
- **Status:** 🟢 **Product Done · Code Done** · pkg-000075 · P8 · H-01 WAIVE · next **DONE** · 2026-11-10T16:23:38Z · hard-dep STORY-71 **Done** · [pipeline](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation/STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md)
- **Package:** [`INDEX.md`](INDEX.md) · `req15-tg-channel-interviewer-ux` (residual reopen)
- **Tech-arch:** [`05-send-after-draft-confirm-validate.md`](../../../architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md) · [`00-overview`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) · hard-dep [`04`](../../../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md)
- **Parent product:** REQ15 channel interview UX · peer Keep [`REQ-11`](../../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md)
- **Hard-depends:** [`STORY-AIBRIDGE-71`](STORY-AIBRIDGE-71-awaiting-interpretation-actions-always.md)
- **Peer Done:** [`STORY-AIBRIDGE-68`](STORY-AIBRIDGE-68-channel-seam-send-actions-always.md) (Send mint on send-ready Keep)
- **Evidence:** [north star](../../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-north-star-2026-11-10.md) §3.4–5 · [citizen gap](../../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-gap-2026-11-10.md) §3.4–6 · [handoff log-note](../../../../../docs/analysis/req15-tg-interview-2026-11-10-handoff-chain-log-note.md)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)
- **Emitted:** 2026-11-10 · Tech-arch + subtasks: 2026-11-10
- **Delivery class:** arch + Implementation + technical subtasks Present · **runtime implement out** (after 71 runtime) · no invent live stash SUCCESS

## Scope (requirements)

1. **Send** confirm actions on the channel turn **MUST** appear only after **both**: (a) the citizen has successfully confirmed the draft interpretation (draft-approve CTA consumed / interpretation confirmed), **and** (b) validation for submit readiness has succeeded per the product gate (north star: validation **after** draft approve).
2. The product **MUST NOT** expose Send confirm actions **before** draft-approve CTA success.
3. Free-text «отправляй» **MUST NOT** be treated as Send (Keep REQ-11) — Send remains an in-chat server action after the gate in (1).
4. After Send confirm consume, stash and `continuation_url` remain **server-owned** only (REQ-11 Keep); no model-owned HTTP submit.
5. This story assumes Confirm/Edit availability during `awaiting_interpretation_confirm` from **STORY-AIBRIDGE-71**.

## Out of scope

- Remint Confirm/Edit on empty actions — **STORY-AIBRIDGE-71**.  
- Roles prose / role-theater ban — **STORY-GPT-ROL-07**.  
- Redefining SPA login/OTP (Present after URL).  
- Gateway/SPA redesign; epic/task folders; **runtime code this wave**.  
- Invent live stash SUCCESS.  
- New TokenActionKind invent.

## Acceptance (product)

| ID | Criterion |
|----|-----------|
| AC-72-01 | Send confirm actions are absent until draft interpretation is confirmed |
| AC-72-02 | Send confirm actions appear only after validation success following that confirm (north star order) |
| AC-72-03 | Free-text send verbs do not mint Send or execute stash |
| AC-72-04 | Stash / `continuation_url` only via Send confirm → server path (REQ-11) |

## Verified current state (honesty)

| Fact | Status | Cite |
|------|--------|------|
| Send after validated FC freeze on `/turns` | **Present** | `coordinator.build_turn_from_engine` · STORY-68 Keep |
| FC blocked until `INTERPRETATION_CONFIRMED` | **Present** | `validate_function_calls` |
| `CONFIRM_INTERPRETATION` → state only, `actions=[]`, `post_confirm_engine` | **Present** | `confirm.consume_action_token` |
| Post-confirm auto engine / validate / Send on `/actions` | **Present** (P3 harness) | `channel.run_post_interpretation_confirm_chain` · arch [`05`](../../../architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md) |
| Live handoff-chain window | Never invent live SUCCESS this wave | gap 2026-11-10 residual deploy |
| North-star order approve → validate → Send | **Present** in harness · ≠ live Pass | north star §3 · tests/story_72 |

## Desired

Citizen approves draft with a button, validation runs next, then Send appears — never Send before approve, never command-only send.

## Implementation (target)

Order mirrors arch [`05`](../../../architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md). Hard-dep STORY-71 runtime. **No** invent stash on interpret · **no** new token kinds · **no** soften FC-before-confirm.

1. **Keep gates** — Send absent until interpretation confirmed; FC before confirm still blocked (AC-72-01).
2. **Hook** — after successful `CONFIRM_INTERPRETATION` consume: server-owned InterviewEngine turn (no citizen free-text) → Present `build_turn_from_engine`.
3. **Success path** — FC OK → `validate_function_calls` → `persist_pending_tool` → `offer_send_confirm` on **same** `/actions` success payload (AC-72-02).
4. **Fail / no-FC path** — fail-closed reply + `offer_continue_seam` (CONTINUE/Edit); assert no `CONFIRM_SEND`; `gateway_authorized` stays False.
5. **Keep** — free-text send verbs ≠ Send/stash (AC-72-03); stash only via `CONFIRM_SEND` (AC-72-04).
6. **Tests + docs** — harness for confirm→Send-after-validate; dual-confirm / 56/68/70 regression; thin runtime note; INDEX honesty.

## Code points
- `src/aibridge/confirm.py` (`CONFIRM_INTERPRETATION` consume branch)
- `src/aibridge/channel.py` (`process_action` wire)
- `src/aibridge/coordinator.py` (`build_turn_from_engine` · `validate_function_calls` · `persist_pending_tool`)
- `src/aibridge/confirm.py` (`offer_send_confirm` · `offer_continue_seam` Keep)
- `tests/` — new STORY-72 harness + dual-confirm / story 56/68/70 regression

## Technical subtasks (arch-bound; pre-P1.3)

| ID | Subtask | Arch cite | AC / DoD | Touch (as-is) | OOS | Status |
|----|---------|-----------|----------|---------------|-----|--------|
| **t01** | Arch `05`: post-confirm sequence + fail-closed; cite Present empty `/actions` | [`05` §1–2](../../../architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md) | AC-72-01…02 policy | arch `05` · story Implementation | Soften interpret≠gateway | **Done** |
| **t02** | Hook после `CONFIRM_INTERPRETATION`: server-owned engine turn → `build_turn_from_engine` | [`05` §2](../../../architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md) | AC-72-02 | `confirm.py` · `channel.process_action` | New TokenActionKind | **Done** |
| **t03** | Success path: validate→persist→`offer_send_confirm` в том же actions payload | [`05` §2](../../../architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md) | AC-72-02 | `coordinator.py` · `confirm.offer_send_confirm` | Invent stash on interpret | **Done** |
| **t04** | Fail/no-FC path: CONTINUE/Edit; assert no `CONFIRM_SEND`; no gateway | [`05` §2–3](../../../architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md) | AC-72-01 · AC-72-04 | `offer_continue_seam` | Premature Send invent | **Done** |
| **t05** | Harness: Confirm → Send only after validate; Confirm alone never Send; FC before confirm blocked; free-text send ≠ stash | [`05` §4](../../../architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md) | AC-72-01…04 | `tests/` | Live TG invent | **Done** |
| **t06** | Regression: dual-confirm / STORY-56/68/70/71 Keep | [`01`](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) · Keep dual-confirm | AC Keep | `tests/` | — | **Done** |
| **t07** | Thin runtime-docs note (sequence honesty) | [`05`](../../../architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md) · [`00`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) | honesty | `docs/runtime-docs/19-…` | Invent live SUCCESS | **Done** |
| **t08** | Story gate · package INDEX · hard-dep 71 honesty | [`00`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) | Package gate for 72 | [`INDEX.md`](INDEX.md) · STORY-71 | Code Done invent before 71 | **Done** |

## Dependencies
- **Hard:** STORY-71 **arch+subtasks Present**; **runtime of 71 before runtime of 72**.
- Soft: STORY-68 Send-ready Keep; GPT ROL-07 not required for AC-72 server chain.

## Related

- Package: [`INDEX.md`](INDEX.md)  
- Peer: [STORY-71](STORY-AIBRIDGE-71-awaiting-interpretation-actions-always.md) · [STORY-68](STORY-AIBRIDGE-68-channel-seam-send-actions-always.md)  
- Gap / north star: [citizen gap 2026-11-10](../../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-gap-2026-11-10.md) · [north star](../../../../../docs/analysis/req15-tg-interviewer-citizen-conversation-north-star-2026-11-10.md)  
