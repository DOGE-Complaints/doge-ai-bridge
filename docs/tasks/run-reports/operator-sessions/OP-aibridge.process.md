# OP-aibridge.process.md

**Working plan:** [`.cursor/plans/OP-aibridge-req15-71-72-20261110.plan.md`](../../../../../.cursor/plans/OP-aibridge-req15-71-72-20261110.plan.md)  
**NO agent ids in this file** (live ids only in `OP-aibridge.session.yaml`).

## Delivery model

- OP orchestrate only — no product code, no invent AC, no push unless operator ordered
- Claims: Read/Glob only; else Unknown
- `delivery=subagent` — exactly two agents: BLD-aibridge + VAL-aibridge
- Verbatim fences; no operator paste
- Overnight: stop only `стоп|stop|pause|halt`; auto-approve P1.3b/P5b; no pause after story; P8 local no-push

## Constants

| Variable | Value |
|----------|-------|
| `$builderProject` | `aibridge` |
| `$tasksRoot` | `doge-ai-bridge/docs/tasks` |
| `$planFile` | `.cursor/plans/aibridge_builder.plan.md` |
| `focus_folder` | `doge-ai-bridge` |
| `pipeline_doc` | `doge-ai-bridge/docs/tasks/aibridge-story-execution-pipeline.md` |
| `$verifyCmd` | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify` |
| contract | `docs/methodology/Zeya888-builder-queue/contracts/aibridge-operator-contract.md` |
| dashboard | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| skill | `python-pro` |
| hasUxPipeline | **false** |
| Pkg | after `pkg-000073` → **pkg-000074+** |
| Epic | **REUSE** `EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux` |

## Queue

| # | story | intake |
|---|-------|--------|
| 1 | `…/STORY-AIBRIDGE-71-awaiting-interpretation-actions-always.md` | Todo · arch+subtasks |
| 2 | `…/STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md` | Todo · hard-dep 71 |

**mode:** sequential · count=2

## Plan-sim + ROLE_LOCK

P1.3/P5 = PLAN_DRAFT → auto GATE → PLAN_APPLY.  
Each Task prepend: `ROLE_LOCK: Execute ONLY the fence below. RETURN_TO_ROOT…`

## Phase script

P1.3a → P1.3b → P2 (OP shell) → P3 → P4 → P5a/b → P6? → P7 → P8 → next story
