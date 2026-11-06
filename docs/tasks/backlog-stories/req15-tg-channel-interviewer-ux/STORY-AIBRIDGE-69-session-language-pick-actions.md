# STORY-AIBRIDGE-69 — Session language pick actions

## Meta
- **Key:** `STORY-AIBRIDGE-69-session-language-pick-actions`
- **Status:** 🟢 **Product Done · Code Done** · pkg-000072 · P8 · 2026-11-06T12:47:50Z · next **DONE** · no invent Railway/live SUCCESS · no invent full i18n
- **Package:** [`INDEX.md`](INDEX.md) · `req15-tg-channel-interviewer-ux`
- **Pipeline:** [`STORY-AIBRIDGE-69-….md`](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-69-session-language-pick-actions/STORY-AIBRIDGE-69-session-language-pick-actions.md) · epic [`EPIC-AIBRIDGE-12`](../../epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux.md)
- **P1 APPLY:** 2026-11-06T12:29:18Z · [p1 APPLIED](../../../../../.cursor/plans/p1_aibridge_69_scaffold_20261106T122734Z.plan.md)
- **Tech-arch:** [`req15-tg-channel-interviewer-ux/02-session-language-locale.md`](../../../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md) · [`00-overview`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md)
- **Parent product:** REQ15 channel interview UX · i18n et/ru/en
- **Evidence:** [`req15-tg-interviewer-target-ux-2026-11-06.md`](../../../../../docs/analysis/req15-tg-interviewer-target-ux-2026-11-06.md) Goal 3 · [triage](../../../../../docs/analysis/req15-tg-interviewer-ux-gap-triage-2026-11-06.md)
- **Depends:** Soft — independent of 68; telegram ChannelAction render **Present**
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)
- **Emitted:** 2026-11-06 · Tech-arch + subtasks: 2026-11-06
- **Product Done honesty:** Code/docs after t01–t08 + t09 tip sync. Locale SSOT=`ConfirmSession`; harness-proven; do not invent full i18n / live TG SUCCESS.

## Scope

1. When the first user message **does not** allow reliable language identification (e.g. opaque tokens like `888`), the channel **MUST** offer **language-pick actions** before continuing the interview in a guessed locale.
2. Each action label **MUST** include the **language name** and a **flag emoji**; English **MUST** use the **US** flag (🇺🇸).
3. Supported picks at minimum: **Eesti**, **Русский**, **English** (aligned with product `{et,ru,en}`).
4. Chosen language **MUST** persist as **session locale** for subsequent interview turns until explicitly changed.
5. Telegram only renders Present `ChannelAction` list — **no** separate telegram STORY required for label strings.

## Out of scope

- Seam/Send confirm residual (STORY-68).  
- Roles prose (GPT UI ROL-05/06).  
- Full i18n of every system string beyond session locale lock.  
- Runtime implement in this docs wave (other dialog).  
- Locale SSOT in semantic_state facts payload (arch lock: ConfirmSession).

## Acceptance (product)

| ID | Criterion |
|----|-----------|
| AC-69-01 | Unclear-language start → language actions Present on turn response |
| AC-69-02 | Labels include name + flag; English uses 🇺🇸 |
| AC-69-03 | Selection binds session locale for following turns |
| AC-69-04 | Clear-language starts (e.g. «историю хочу подать») may skip picker |

## Verified current state (honesty)

| Fact | Status | Cite |
|------|--------|------|
| Inbound `language_code` mapping | **Present** | doge-telegram `mapper.py` · bridge `schemas.py` |
| Bridge engine consumes `language_code` | **Soft-hint only** (P3) | unclear gate ignores silent lock |
| Lang-pick actions | **Present** (P3) | `offer_language_pick` · EN=🇺🇸 |
| `ConfirmSession.locale` / state_json locale | **Present** (P3) | `confirm.py` SSOT |
| Telegram can render arbitrary action labels | **Present** Keep | `outbound.py` |
| Pille session | Clear RU start — Goal 3 **N/A that session**; still Desired product | evidence notes |

## Code points
- `confirm.py` ConfirmSession · `action_tokens.py` · `channel.py` · `schemas.py`
- Peer: doge-telegram `mapper.py` · `outbound.py`

## Technical subtasks (arch-bound; pre-P1.3)

| ID | Subtask | Arch cite | AC / DoD | Touch (as-is) | OOS | Status |
|----|---------|-----------|----------|---------------|-----|--------|
| **t01** | Unclear-language detector policy (opaque/`888`/digits/empty); clear-text skip | [`02` §2](../../../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md) | AC-69-01 · AC-69-04 | Thin policy helper / channel gate | Silent lock from `language_code` alone | Done |
| **t02** | `ConfirmSession.locale ∈ {et,ru,en}` + persist in `state_json` | [`02` §3](../../../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md) | AC-69-03 | `confirm.py` | Semantic-state facts as locale SSOT | Done |
| **t03** | Memory + Postgres session round-trip for locale | [`02` §3](../../../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md) · [`02` §6](../../../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md) | AC-69-03 | confirm store / pg path | New migration invent unless needed | Done |
| **t04** | Lang-pick token kinds + labels Eesti/Русский/English+🇺🇸 | [`02` §4](../../../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md) | AC-69-02 | `action_tokens.py` · confirm/channel mint | Telegram STORY for strings | Done |
| **t05** | First-turn picker gate before interview engine advance | [`02` §2](../../../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md) · [`02` §6](../../../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md) | AC-69-01 | `channel.py` / coordinator gate | Block on STORY-68 CONTINUE | Done |
| **t06** | Bind locale on pick consume; apply to subsequent turns (prompt/context Adapt) | [`02` §3](../../../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md) | AC-69-03 | interview/channel wire | Full UI i18n catalog | Done |
| **t07** | Harness: unclear→actions; clear skip; persist; EN=🇺🇸 | [`02` §1](../../../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md) · [`02` §4](../../../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md) | AC-69-01…04 tech | `tests/` | Live TG window invent | Done |
| **t08** | Story gate + thin runtime-docs note · package INDEX honesty | [`00`](../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) | Package gate for 69 | runtime-docs · [`INDEX.md`](INDEX.md) | Parent Phase F | Done |
| **t09** | Audit G-01 active-package tip sync | tip SSOT | Info tip honesty | `aibridge-active-package.current.yaml` | invent live SUCCESS | Done |

## Dependencies
- Soft: independent of STORY-68.
- Soft: telegram ChannelAction render **Present**.

## Related

- Sibling: [STORY-AIBRIDGE-68](STORY-AIBRIDGE-68-channel-seam-send-actions-always.md)  
- Target UX Goal 3  
