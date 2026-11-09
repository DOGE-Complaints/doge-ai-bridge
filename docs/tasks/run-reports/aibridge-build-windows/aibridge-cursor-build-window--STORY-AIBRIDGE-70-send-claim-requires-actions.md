---
generated_utc: 2026-11-09T11:36:26Z
builder_project: aibridge
aibridge_input_package: doge-ai-bridge/docs/tasks/aibridge-active-packages/pkg-000073-20261109-epic-aibridge-12-story-70-send-claim-requires-actions.yaml
window_mode: story_key
artifact_kind: aibridge_cursor_build_window
pkg_schema_version: 1
---

# AI Bridge Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `aibridge_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --write-build-window --story-key STORY-AIBRIDGE-70-send-claim-requires-actions
```

Исполнение: [`aibridge-story-execution-pipeline.md`](../../aibridge-story-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## STORY-AIBRIDGE-70-send-claim-requires-actions
1. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-70-send-claim-requires-actions/task-aibridge-70-t01-send-claim-marker-lock/README.md`
2. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-70-send-claim-requires-actions/task-aibridge-70-t02-seam-policy-send-claim-gate/README.md`
3. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-70-send-claim-requires-actions/task-aibridge-70-t03-coordinator-remint-interpret-send/README.md`
4. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-70-send-claim-requires-actions/task-aibridge-70-t04-build-turn-ensure-invariant/README.md`
5. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-70-send-claim-requires-actions/task-aibridge-70-t05-harness-send-claim-remint/README.md`
6. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-70-send-claim-requires-actions/task-aibridge-70-t06-regression-story-68-suite/README.md`
7. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-70-send-claim-requires-actions/task-aibridge-70-t07-runtime-docs-send-claim/README.md`
8. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-70-send-claim-requires-actions/task-aibridge-70-t08-story-gate-index-arch/README.md`

## P3 disposition (2026-11-09T11:36:43Z)

| Task | Status | Evidence |
|------|--------|----------|
| t01–t08 | **Done** | task READMEs · harness 14 passed (70+68) |
| Send-claim | Present | `seam_policy.py` · `coordinator._ensure_control_surface` · idempotent `offer_*` |
| Honesty | no invent stash/NL/live SUCCESS · Keep REQ-11 · GPT invent-named-CTA OOS | runtime-docs/17 |

**next=P4** (operator fence).

