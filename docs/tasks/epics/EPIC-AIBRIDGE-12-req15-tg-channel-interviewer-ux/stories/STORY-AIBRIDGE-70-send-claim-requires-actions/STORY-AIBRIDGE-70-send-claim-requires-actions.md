# STORY-AIBRIDGE-70 — Send claim requires in-chat actions

## Meta
- **Key:** `STORY-AIBRIDGE-70-send-claim-requires-actions`
- **Status:** 🟢 Product Done · Code Done · pkg-000073 · P8 · 2026-11-09T11:46:08Z · next **DONE** · H-01 WAIVE
- **Parent Epic:** [`EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux.md`](../../EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux.md)
- **source:** `backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-70-send-claim-requires-actions.md`
- **decision_ref:** backlog STORY-70 · arch [`03`](../../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md)
- **Package:** [`req15-tg-channel-interviewer-ux/INDEX.md`](../../../../backlog-stories/req15-tg-channel-interviewer-ux/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000073-20261109-epic-aibridge-12-story-70-send-claim-requires-actions.yaml`
- **P1 materialize:** 2026-11-09T11:33:00Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_70_scaffold_20261109T113113Z.plan.md)
- **Depends:** STORY-68 **Done** (Keep mint path)
- **OOS:** invent stash · NL rewrite reply_text v1 · Railway/live TG SUCCESS · GPT invent-named-CTA · STORY-69 reopen
- **Honesty:** Send-claim remint CTAs · Keep REQ-11 · STORY-68 regression · no invent stash/NL/live SUCCESS

## Doc pointers

| Topic | Where |
|-------|--------|
| Arch Send-claim | [`03-send-claim-control-surface.md`](../../../../architecture/req15-tg-channel-interviewer-ux/03-send-claim-control-surface.md) |
| Peer seam/Send | [`01`](../../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) · STORY-68 Done |
| Overview | [`00-overview.md`](../../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) |

## Scope
- Named Send/submit claims without actions/URL → remint control surface (or must not claim Send).
- Expand beyond STORY-68 «интерфейс» markers; remint Keep order; no invent stash; no NL rewrite v1.

## Nested tasks (pkg-000073)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-70-t01-send-claim-marker-lock](./task-aibridge-70-t01-send-claim-marker-lock/README.md) | AC-70-02 | Done |
| t02 | [task-aibridge-70-t02-seam-policy-send-claim-gate](./task-aibridge-70-t02-seam-policy-send-claim-gate/README.md) | AC-70-01 | Done |
| t03 | [task-aibridge-70-t03-coordinator-remint-interpret-send](./task-aibridge-70-t03-coordinator-remint-interpret-send/README.md) | AC-70-03 | Done |
| t04 | [task-aibridge-70-t04-build-turn-ensure-invariant](./task-aibridge-70-t04-build-turn-ensure-invariant/README.md) | AC-70-01 | Done |
| t05 | [task-aibridge-70-t05-harness-send-claim-remint](./task-aibridge-70-t05-harness-send-claim-remint/README.md) | AC-70-01…04 tech | Done |
| t06 | [task-aibridge-70-t06-regression-story-68-suite](./task-aibridge-70-t06-regression-story-68-suite/README.md) | AC-68 Keep | Done |
| t07 | [task-aibridge-70-t07-runtime-docs-send-claim](./task-aibridge-70-t07-runtime-docs-send-claim/README.md) | honesty | Done |
| t08 | [task-aibridge-70-t08-story-gate-index-arch](./task-aibridge-70-t08-story-gate-index-arch/README.md) | Package gate for 70 | Done |

## Code points
- `seam_policy.py` · `coordinator.py` (`_ensure_control_surface` / `build_turn_from_engine`) · `confirm.py` Keep offers
- Tests: new STORY-70 + `tests/test_story_68_*` regression
