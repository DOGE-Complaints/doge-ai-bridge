# STORY-AIBRIDGE-71 — Awaiting interpretation always has Confirm/Edit actions

## Meta
- **Key:** `STORY-AIBRIDGE-71-awaiting-interpretation-actions-always`
- **Status:** 🟢 Product Done · Code Done · pkg-000074 · P8 · 2026-11-10T14:34:54Z · next **DONE** · H-01 WAIVE
- **Parent Epic:** [`EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux.md`](../../EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux.md)
- **source:** `backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-71-awaiting-interpretation-actions-always.md`
- **decision_ref:** backlog STORY-71 · arch [`04`](../../../../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md)
- **Package:** [`req15-tg-channel-interviewer-ux/INDEX.md`](../../../../backlog-stories/req15-tg-channel-interviewer-ux/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000074-20261110-epic-aibridge-12-story-71-awaiting-interpretation-actions-always.yaml`
- **P1 materialize:** 2026-11-10T12:41:54Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_71_scaffold_20261110T123821Z.plan.md)
- **P3 Build:** 2026-11-10T12:54:14Z
- **P5 APPLY:** 2026-11-10T13:40:11Z · [p5 APPLIED](../../../../../../.cursor/plans/p5_aibridge_71_gap_20261110T131453Z.plan.md) · [disposition](../../../../analysis/p5-disposition-STORY-AIBRIDGE-71-awaiting-interpretation-actions-always-20261110.md)
- **P6:** 2026-11-10T13:59:30Z · [run-summary](../../../../run-reports/run-summary-20261110-1359-story-aibridge-71-p6-t09.md) · G-01 CLOSED
- **P7:** 2026-11-10T14:34:54Z · [p7](../../../../analysis/p7-reaudit-STORY-AIBRIDGE-71-awaiting-interpretation-actions-always-20261110.md) · WAVE_COMPLETE
- **P8:** 2026-11-10T14:34:54Z · feat→test→docs · **no push**
- **Depends:** Soft: STORY-68/70 **Done** (Keep mint + claim remint Present)
- **Downstream OOS:** STORY-72 · GPT ROL-07
- **OOS:** invent Send/stash · NL rewrite reply_text · Railway/live TG SUCCESS · invent-named-CTA
- **Honesty:** state-invariant remint Confirm/Edit when `AWAITING_INTERPRETATION_CONFIRM` + empty actions **without** Send-claim markers · Keep REQ-11 · 68/70 regression · no invent live SUCCESS · Code Done ≠ live Pass

## Doc pointers

| Topic | Where |
|-------|--------|
| Arch awaiting-interpret always | [`04-awaiting-interpretation-always-actions.md`](../../../../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md) |
| Runtime note | [`18-awaiting-interpretation-always-actions.md`](../../../../runtime-docs/18-awaiting-interpretation-always-actions.md) |
| Peer Send-claim | [`03`](../../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md) · STORY-70 Done |
| Peer seam/Send | [`01`](../../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) · STORY-68 Done |
| Overview | [`00-overview.md`](../../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) |

## Scope
- FSM `awaiting_interpretation_confirm` + otherwise empty `actions` → always remint Confirm+Edit (Cancel Keep).
- Obligation holds on ordinary free-text turns — **not** only via Send-claim / vague markers (STORY-70 residual).
- **No** invent Send confirm / stash; **no** NL rewrite; Keep REQ-11.

## Nested tasks (pkg-000074)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-71-t01-arch04-policy-state-invariant-remint](./task-aibridge-71-t01-arch04-policy-state-invariant-remint/README.md) | AC-71-02 | Done |
| t02 | [task-aibridge-71-t02-ensure-early-remint-awaiting-interpret](./task-aibridge-71-t02-ensure-early-remint-awaiting-interpret/README.md) | AC-71-01 · AC-71-02 | Done |
| t03 | [task-aibridge-71-t03-flip-awaiting-do-not-remint-comment](./task-aibridge-71-t03-flip-awaiting-do-not-remint-comment/README.md) | AC-71-01 | Done |
| t04 | [task-aibridge-71-t04-build-turn-ensure-coverage](./task-aibridge-71-t04-build-turn-ensure-coverage/README.md) | AC-71-01 | Done |
| t05 | [task-aibridge-71-t05-harness-awaiting-plain-reply-remint](./task-aibridge-71-t05-harness-awaiting-plain-reply-remint/README.md) | AC-71-01…03 | Done |
| t06 | [task-aibridge-71-t06-regression-story-68-70-suites](./task-aibridge-71-t06-regression-story-68-70-suites/README.md) | AC-68/70 Keep | Done |
| t07 | [task-aibridge-71-t07-runtime-docs-awaiting-interpret](./task-aibridge-71-t07-runtime-docs-awaiting-interpret/README.md) | honesty | Done |
| t08 | [task-aibridge-71-t08-story-gate-index-arch](./task-aibridge-71-t08-story-gate-index-arch/README.md) | Package gate for 71 | Done |
| t09 | [task-aibridge-71-t09-audit-g01-backlog-tech-table-sync](./task-aibridge-71-t09-audit-g01-backlog-tech-table-sync/README.md) | G-01 CLOSED | Done |

## Code points
- `coordinator.py` (`_ensure_control_surface` early remint · `build_turn_from_engine` comment) · `confirm.py` Keep `offer_interpretation_confirm` · `seam_policy.py` STORY-71 note
- Tests: `tests/test_story_71_awaiting_interpretation_actions_always.py` + 68/70 regression
