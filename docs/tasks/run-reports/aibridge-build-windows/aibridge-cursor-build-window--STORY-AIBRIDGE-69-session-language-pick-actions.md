---
generated_utc: 2026-11-06T12:32:01Z
builder_project: aibridge
aibridge_input_package: doge-ai-bridge/docs/tasks/aibridge-active-packages/pkg-000072-20261106-epic-aibridge-12-story-69-session-language-pick-actions.yaml
window_mode: story_key
artifact_kind: aibridge_cursor_build_window
pkg_schema_version: 1
---

# AI Bridge Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `aibridge_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --write-build-window --story-key STORY-AIBRIDGE-69-session-language-pick-actions
```

Исполнение: [`aibridge-story-execution-pipeline.md`](../../aibridge-story-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## STORY-AIBRIDGE-69-session-language-pick-actions
1. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-69-session-language-pick-actions/task-aibridge-69-t01-unclear-language-detector-policy/README.md`
2. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-69-session-language-pick-actions/task-aibridge-69-t02-confirm-session-locale-field/README.md`
3. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-69-session-language-pick-actions/task-aibridge-69-t03-locale-memory-postgres-roundtrip/README.md`
4. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-69-session-language-pick-actions/task-aibridge-69-t04-lang-pick-token-kinds-labels/README.md`
5. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-69-session-language-pick-actions/task-aibridge-69-t05-first-turn-picker-gate/README.md`
6. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-69-session-language-pick-actions/task-aibridge-69-t06-bind-locale-on-consume/README.md`
7. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-69-session-language-pick-actions/task-aibridge-69-t07-harness-lang-pick-persist/README.md`
8. `@doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-12-req15-tg-channel-interviewer-ux/stories/STORY-AIBRIDGE-69-session-language-pick-actions/task-aibridge-69-t08-story-gate-runtime-docs/README.md`

## P3 disposition (2026-11-06T12:32:14Z)

| Task | Status | Evidence |
|------|--------|----------|
| t01–t08 | **Done** | task READMEs · `tests/test_story_69_session_language_pick.py` (6) + with 68 = 14 passed |
| locale SSOT | ConfirmSession.locale ∈ {et,ru,en} + state_json | `confirm.py` · `locale_policy.py` |
| EN label | English 🇺🇸 | `LANG_PICK_LABELS` |
| Honesty | no invent i18n / live SUCCESS · 68 OOS | runtime-docs/16 |

**next=P4** (operator fence).

