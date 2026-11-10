# STORY-AIBRIDGE-72 — Send after draft confirm and validation

## Meta
- **Key:** `STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation`
- **Status:** 🟢 **Product Done · Code Done** · pkg-000075 · P8 · H-01 WAIVE · next **DONE** · 2026-11-10T16:23:38Z
- **Parent Epic:** [`EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux.md`](../../EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux.md)
- **source:** `backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md`
- **decision_ref:** backlog STORY-72 · arch [`05`](../../../../architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md)
- **Package:** [`req15-tg-channel-interviewer-ux/INDEX.md`](../../../../backlog-stories/req15-tg-channel-interviewer-ux/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000075-20261110-epic-aibridge-12-story-72-send-after-draft-confirm-and-validation.yaml`
- **P1 materialize:** 2026-11-10T14:53:18Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_72_scaffold_20261110T144725Z.plan.md)
- **P3 Build:** 2026-11-10T15:01:32Z · harness `tests/test_story_72_*` · runtime-docs `19`
- **P5 APPLY:** 2026-11-10T16:11:43Z · [p5 APPLIED](../../../../../../.cursor/plans/p5_aibridge_72_gap_20261110T160418Z.plan.md) · [disposition](../../../../analysis/p5-disposition-STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation-20261110.md) · `run_mode=aibridge_72_audit_20261110`
- **P6:** 2026-11-10T16:17:31Z · tip-sync · [p6](../../../run-reports/run-summary-20261110-1617-story-aibridge-72-p6-t09.md) · t09 Done
- **P8:** 2026-11-10T16:23:38Z · local commits feat→test→docs · no push · Code Done ≠ invent live Pass
- **Hard-depends:** STORY-71 **Done** (pkg-000074)
- **Soft peer:** STORY-68 Send-ready Keep · GPT ROL-07 OOS
- **OOS:** invent stash on interpret · new TokenActionKind · soften FC-before-confirm · invent live SUCCESS · remint Confirm/Edit (71)
- **Honesty:** Send only after draft confirm **and** validation · free-text send ≠ Send/stash · Keep REQ-11 · 56/68/70/71 regression · H-01 WAIVE live smoke · no invent live SUCCESS · Code Done ≠ live Pass

## Doc pointers

| Topic | Where |
|-------|--------|
| Arch post-confirm validate→Send | [`05-send-after-draft-confirm-validate.md`](../../../../architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md) |
| Hard-dep awaiting-interpret | [`04`](../../../../architecture/req15-tg-channel-interviewer-ux/04-awaiting-interpretation-always-actions.md) · STORY-71 Done |
| Peer seam/Send | [`01`](../../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) · STORY-68 Done |
| Overview | [`00-overview.md`](../../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) |

## Scope
- Send confirm only after draft interpretation confirmed **and** validation success (north star order).
- Free-text send verbs ≠ mint Send / execute stash.
- Stash / continuation_url only via authorized Send consume (REQ-11).

## Nested tasks (pkg-000075)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-72-t01-arch05-policy-post-confirm-sequence](./task-aibridge-72-t01-arch05-policy-post-confirm-sequence/README.md) | AC-72-01…02 | Done |
| t02 | [task-aibridge-72-t02-hook-confirm-interpretation-engine-turn](./task-aibridge-72-t02-hook-confirm-interpretation-engine-turn/README.md) | AC-72-02 | Done |
| t03 | [task-aibridge-72-t03-success-validate-persist-offer-send](./task-aibridge-72-t03-success-validate-persist-offer-send/README.md) | AC-72-02 | Done |
| t04 | [task-aibridge-72-t04-fail-nofc-continue-seam-no-send](./task-aibridge-72-t04-fail-nofc-continue-seam-no-send/README.md) | AC-72-01 · AC-72-04 | Done |
| t05 | [task-aibridge-72-t05-harness-confirm-then-send-after-validate](./task-aibridge-72-t05-harness-confirm-then-send-after-validate/README.md) | AC-72-01…04 | Done |
| t06 | [task-aibridge-72-t06-regression-story-56-68-70-71](./task-aibridge-72-t06-regression-story-56-68-70-71/README.md) | AC Keep | Done |
| t07 | [task-aibridge-72-t07-runtime-docs-post-confirm-send](./task-aibridge-72-t07-runtime-docs-post-confirm-send/README.md) | honesty | Done |
| t08 | [task-aibridge-72-t08-story-gate-index-arch](./task-aibridge-72-t08-story-gate-index-arch/README.md) | Package gate for 72 | Done |
| t09 | [task-aibridge-72-t09-audit-g01-tip-refresh](./task-aibridge-72-t09-audit-g01-tip-refresh/README.md) | G-01 tip-refresh | Done |

## Code points
- `confirm.py` · `channel.process_action` · `coordinator.build_turn_from_engine` / `validate_function_calls` / `persist_pending_tool` · `offer_send_confirm` · `offer_continue_seam`
- Tests: new STORY-72 + dual-confirm / 56/68/70/71 regression
