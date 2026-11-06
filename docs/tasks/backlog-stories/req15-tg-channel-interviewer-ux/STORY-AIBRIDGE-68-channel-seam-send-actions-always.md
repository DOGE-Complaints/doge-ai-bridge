# STORY-AIBRIDGE-68 — Channel seam + Send actions always

## Meta
- **Key:** `STORY-AIBRIDGE-68-channel-seam-send-actions-always`
- **Status:** 🟢 **Product Done · Code Done** · pkg-000071 · P8 · 2026-11-06T12:23:51Z · next **DONE** · live smoke residual separate · no invent Railway/live SUCCESS
- **Package:** [`INDEX.md`](INDEX.md) · `req15-tg-channel-interviewer-ux`
- **Pipeline:** [`STORY-AIBRIDGE-68-….md`](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-68-channel-seam-send-actions-always/STORY-AIBRIDGE-68-channel-seam-send-actions-always.md) · epic [`EPIC-AIBRIDGE-12`](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux.md)
- **P1 APPLY:** 2026-11-06T12:01:54Z · [p1 APPLIED](../../../../../.cursor/plans/p1_aibridge_68_scaffold_20261106T115910Z.plan.md)
- **Tech-arch:** [`req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md`](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) · [`00-overview`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md)
- **Parent product:** REQ15 channel interview UX · peer Keep [`REQ-11`](../../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md)
- **Evidence:** [`req15-tg-interviewer-ux-gap-pille-2026-11-06.md`](../../../../../docs/analysis/req15-tg-interviewer-ux-gap-pille-2026-11-06.md) Goals 2/4/§4 · [triage](../../../../../docs/analysis/req15-tg-interviewer-ux-gap-triage-2026-11-06.md)
- **Depends:** REQ-11 stories 56–58 **Done** (Keep pipe Present; this story = residual live channel behavior)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)
- **Emitted:** 2026-11-06 · Tech-arch + subtasks: 2026-11-06
- **Product Done honesty:** Code/docs after t01–t07 + t08; live smoke residual separate. Do not invent Railway SUCCESS. Soft peer GPT ROL-05 wording.

## Scope

1. At **non-seamless** interview stages (before validate / send / edit), the channel turn response **MUST** include Telegram-renderable **actions** (continue and/or edit as product needs) so the user is not forced to type «дальше».
2. When the draft is **send-ready**, the system **MUST** mint **Send confirm** actions (Keep dual-confirm) without requiring free-text «отправляй».
3. A bot reply that claims submission must happen «в интерфейсе» **MUST NOT** be returned without either (a) Present in-chat actions that perform the next server step, or (b) after successful stash, a `continuation_url` in the outbound path.
4. Server-owned stash remains the only HTTP submit path (REQ-11 Keep). Model must not own gateway stash.

## Out of scope

- Instruction prose (GPT UI [STORY-GPT-ROL-05](../../../../../GPT%20UI/docs/tasks/backlog-stories/req15-tg-interviewer-roles-ux/STORY-GPT-ROL-05-channel-interview-stage-proactivity.md) / [06](../../../../../GPT%20UI/docs/tasks/backlog-stories/req15-tg-interviewer-roles-ux/STORY-GPT-ROL-06-channel-interview-surface-readability.md)).  
- Language picker (STORY-69).  
- Telegram transport rendering of ChannelAction (Present Keep).  
- Gateway/SPA contract redesign.  
- Runtime implement in this docs wave (other dialog).

## Acceptance (product)

| ID | Criterion |
|----|-----------|
| AC-68-01 | Stage seams that are not seamless expose continue/edit (or equivalent) actions on `/v1/channel/turns` response |
| AC-68-02 | Send-ready draft yields Send confirm actions without user coaching «отправь» |
| AC-68-03 | No send-path user message relies solely on vague «интерфейс» without actions or post-stash URL |
| AC-68-04 | Stash still only via Send consume → gateway (Keep REQ-11) |

## Verified current state (honesty)

| Fact | Status | Cite |
|------|--------|------|
| `ChannelAction` contract + OpenAPI | **Present** | `schemas.py` · channel OpenAPI |
| `offer_interpretation_confirm` / `offer_send_confirm` | **Present** | `confirm.py` · `coordinator.py` |
| Token kinds interpret/send/edit/cancel | **Present** | `action_tokens.py` |
| Generic `CONTINUE` kind | **Present** (P3) | `TokenActionKind.CONTINUE` |
| Stage-invariant CTA on every non-seamless seam | **Present** (P3) | `seam_policy` + coordinator |
| No-vague-«интерфейс» policy | **Present** (P3) | `needs_control_surface` |
| Stash via Send consume → gateway | **Present** Keep | REQ-11 |
| Telegram action render | **Present** Keep | doge-telegram `outbound.py` |

## Code points
- `action_tokens.py` · `confirm.py` · `coordinator.py` · `channel.py` · `schemas.py`
- Keep: `gateway.py` stash · telegram outbound

## Technical subtasks (arch-bound; pre-P1.3)

| ID | Subtask | Arch cite | AC / DoD | Touch (as-is) | OOS | Status |
|----|---------|-----------|----------|---------------|-----|--------|
| **t01** | Lock seam policy invariants: which stages are non-seamless; free-text «дальше» not sole path | [`01` §2](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) | AC-68-01 policy | Thin product/arch matrix at implement | GPT prose rewrite | Done |
| **t02** | Add `TokenActionKind.CONTINUE` + mint/hash store Adapt | [`01` §2](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) · [`01` §6](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) | AC-68-01 | `action_tokens.py` · `confirm.py` | Reuse interpret as continue | Done |
| **t03** | Coordinator emit continue and/or edit on non-seamless seam turns | [`01` §2](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) · [`01` §6](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) | AC-68-01 | `coordinator.py` · channel turn assembly | Telegram keyboard redesign | Done |
| **t04** | CONTINUE consume → resume interview (no stash / no gateway) | [`01` §2](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) · [`01` §5](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) | AC-68-01 · AC-68-04 | `confirm.py` consume path | CONTINUE→stash | Done |
| **t05** | Send-ready after freeze/validate always `offer_send_confirm` | [`01` §3](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) | AC-68-02 | `coordinator.py` · `confirm.py` | Model-owned send | Done |
| **t06** | Ban vague «интерфейс» without actions or post-stash `continuation_url` | [`01` §4](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) | AC-68-03 | coordinator/channel policy | ML text filter invent | Done |
| **t07** | Harness: seam actions Present; send-ready CTAs; stash Keep; label passthrough | [`01` §1](../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) · OpenAPI | AC-68-01…04 tech | `tests/` | Live TG window invent | Done |
| **t08** | Story gate + thin runtime-docs note · package INDEX honesty | [`00`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) | Package gate for 68 | runtime-docs · [`INDEX.md`](INDEX.md) | Parent Phase F | Done |

## Dependencies
- Hard: REQ-11 Keep (56–58 **Done**).
- Soft: GPT ROL-05 wording (proactivity prose).
- Soft peer: [STORY-69](STORY-AIBRIDGE-69-session-language-pick-actions.md) independent for lang.

## Related

- Target UX: [`req15-tg-interviewer-target-ux-2026-11-06.md`](../../../../../docs/analysis/req15-tg-interviewer-target-ux-2026-11-06.md)  
- Sibling: [STORY-AIBRIDGE-69](STORY-AIBRIDGE-69-session-language-pick-actions.md)  
