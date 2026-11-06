# STORY-AIBRIDGE-69 — Session language pick actions

## Meta
- **Key:** `STORY-AIBRIDGE-69-session-language-pick-actions`
- **Status:** 🟢 Product Done · Code Done · pkg-000072 · P8 · 2026-11-06T12:47:50Z · next **DONE**
- **Parent Epic:** [`EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux.md`](../../EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux.md)
- **source:** `backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-69-session-language-pick-actions.md`
- **decision_ref:** backlog STORY-69 · arch [`02`](../../../../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md)
- **Package:** [`req15-tg-channel-interviewer-ux/INDEX.md`](../../../../backlog-stories/req15-tg-channel-interviewer-ux/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000072-20261106-epic-aibridge-12-story-69-session-language-pick-actions.yaml`
- **P1 materialize:** 2026-11-06T12:29:18Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_69_scaffold_20261106T122734Z.plan.md)
- **Depends:** soft independent of 68 · telegram ChannelAction render Present
- **OOS:** STORY-68 seam/Send · GPT ROL-05/06 · full i18n · invent live TG SUCCESS · locale in semantic_state facts
- **Honesty:** locale SSOT=`ConfirmSession` · EN=🇺🇸 · unclear→lang-pick · clear-text skip · no invent full i18n / live SUCCESS

## Doc pointers

| Topic | Where |
|-------|--------|
| Arch locale | [`02-session-language-locale.md`](../../../../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md) |
| Overview | [`00-overview.md`](../../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) |
| Peer 68 Done | [`STORY-AIBRIDGE-68`](../STORY-AIBRIDGE-68-channel-seam-send-actions-always/STORY-AIBRIDGE-68-channel-seam-send-actions-always.md) OOS this story |

## Scope
- Unclear first message → language-pick ChannelActions before interview advance.
- Labels: Eesti / Русский / English+🇺🇸; bind `ConfirmSession.locale ∈ {et,ru,en}`.
- Clear-text starts may skip picker.

## Nested tasks (pkg-000072)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-69-t01-unclear-language-detector-policy](./task-aibridge-69-t01-unclear-language-detector-policy/README.md) | unclear/888/digits/empty | Done |
| t02 | [task-aibridge-69-t02-confirm-session-locale-field](./task-aibridge-69-t02-confirm-session-locale-field/README.md) | locale ∈ {et,ru,en} + state_json persist | Done |
| t03 | [task-aibridge-69-t03-locale-memory-postgres-roundtrip](./task-aibridge-69-t03-locale-memory-postgres-roundtrip/README.md) | memory + PG session round-trip for local | Done |
| t04 | [task-aibridge-69-t04-lang-pick-token-kinds-labels](./task-aibridge-69-t04-lang-pick-token-kinds-labels/README.md) | Eesti/Русский/English+🇺🇸 | Done |
| t05 | [task-aibridge-69-t05-first-turn-picker-gate](./task-aibridge-69-t05-first-turn-picker-gate/README.md) | gate before interview engine advance | Done |
| t06 | [task-aibridge-69-t06-bind-locale-on-consume](./task-aibridge-69-t06-bind-locale-on-consume/README.md) | bind + apply subsequent turns | Done |
| t07 | [task-aibridge-69-t07-harness-lang-pick-persist](./task-aibridge-69-t07-harness-lang-pick-persist/README.md) | unclear→actions | Done |
| t08 | [task-aibridge-69-t08-story-gate-runtime-docs](./task-aibridge-69-t08-story-gate-runtime-docs/README.md) | gate + thin runtime note · INDEX honesty | Done |
| t09 | [task-aibridge-69-t09-audit-g01-active-package-tip-sync](./task-aibridge-69-t09-audit-g01-active-package-tip-sync/README.md) | G-01 tip sync (P5 audit) | Done |

## Code points
- `confirm.py` ConfirmSession · `action_tokens.py` · `channel.py` · `schemas.py`
- Peer Keep: doge-telegram `mapper.py` · `outbound.py`
