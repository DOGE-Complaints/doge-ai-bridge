# STORY-AIBRIDGE-68 — Channel seam + Send actions always

## Meta
- **Key:** `STORY-AIBRIDGE-68-channel-seam-send-actions-always`
- **Status:** 🟢 **Product Done · Code Done** · pkg-000071 · P8 · 2026-11-06T12:23:51Z · next **DONE** · live smoke residual separate · no invent Railway/live SUCCESS
- **P8 SHAs (local, no push):** feat `156f327` · test `292567e` · docs `8ab99e6`
- **Parent Epic:** [`EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux.md`](../../EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux.md)
- **source:** `backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-68-channel-seam-send-actions-always.md`
- **decision_ref:** [`STORY-AIBRIDGE-68-….md`](../../../../backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-68-channel-seam-send-actions-always.md) · arch [`01`](../../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md)
- **Package:** [`req15-tg-channel-interviewer-ux/INDEX.md`](../../../../backlog-stories/req15-tg-channel-interviewer-ux/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000071-20261106-epic-aibridge-12-story-68-channel-seam-send-actions-always.yaml`
- **P1 materialize:** 2026-11-06T12:01:54Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_68_scaffold_20261106T115910Z.plan.md)
- **Depends:** hard REQ-11 Keep (56–58 Done) · soft GPT ROL-05 · soft STORY-69 independent
- **OOS:** GPT ROL-05/06 · STORY-69 · TG keyboard redesign · Gateway/SPA · invent live SUCCESS · CONTINUE→stash
- **Honesty:** Keep REQ-11 stash · **CONTINUE ≠ stash** · no invent Railway/live TG SUCCESS · Code Done ≠ live smoke without window

## Doc pointers

| Topic | Where |
|-------|--------|
| Arch seam/Send | [`01-channel-seam-send-actions.md`](../../../../architecture/req15-tg-channel-interviewer-ux/01-channel-seam-send-actions.md) |
| Overview | [`00-overview.md`](../../../../architecture/req15-tg-channel-interviewer-ux/00-overview.md) |
| Keep dual-confirm | [`REQ-11`](../../../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) |
| Evidence | [`req15-tg-interviewer-ux-gap-pille-2026-11-06.md`](../../../../../../docs/analysis/req15-tg-interviewer-ux-gap-pille-2026-11-06.md) |

## Scope
- Non-seamless stages → Telegram-renderable continue/edit actions on `/v1/channel/turns`.
- Send-ready → Send confirm actions without free-text «отправляй».
- No vague «интерфейс» without actions or post-stash `continuation_url`.
- Stash only via Send consume → gateway (Keep).

## Nested tasks (pkg-000071)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-68-t01-lock-seam-policy-invariants](./task-aibridge-68-t01-lock-seam-policy-invariants/README.md) | seam policy | Done |
| t02 | [task-aibridge-68-t02-continue-token-kind](./task-aibridge-68-t02-continue-token-kind/README.md) | CONTINUE kind | Done |
| t03 | [task-aibridge-68-t03-coordinator-emit-seam-actions](./task-aibridge-68-t03-coordinator-emit-seam-actions/README.md) | emit CTAs | Done |
| t04 | [task-aibridge-68-t04-continue-consume-resume](./task-aibridge-68-t04-continue-consume-resume/README.md) | consume resume | Done |
| t05 | [task-aibridge-68-t05-send-ready-offer-always](./task-aibridge-68-t05-send-ready-offer-always/README.md) | send-ready | Done |
| t06 | [task-aibridge-68-t06-ban-vague-interface-without-control](./task-aibridge-68-t06-ban-vague-interface-without-control/README.md) | no vague UI | Done |
| t07 | [task-aibridge-68-t07-harness-seam-send-stash-keep](./task-aibridge-68-t07-harness-seam-send-stash-keep/README.md) | harness | Done |
| t08 | [task-aibridge-68-t08-story-gate-runtime-docs](./task-aibridge-68-t08-story-gate-runtime-docs/README.md) | gate | Done |
| t09 | [task-aibridge-68-t09-audit-g01-active-package-tip-sync](./task-aibridge-68-t09-audit-g01-active-package-tip-sync/README.md) | G-01 tip sync | Done |

## Code points
- `action_tokens.py` · `confirm.py` · `coordinator.py` · `channel.py` · `schemas.py`
- Keep: `gateway.py` stash · doge-telegram outbound
