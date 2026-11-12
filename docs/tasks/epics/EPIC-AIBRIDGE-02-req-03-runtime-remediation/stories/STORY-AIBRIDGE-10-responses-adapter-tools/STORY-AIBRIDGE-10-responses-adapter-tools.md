# STORY-AIBRIDGE-10 — Production Responses adapter + flat tools + prompt

## Meta
- **Key:** `STORY-AIBRIDGE-10-responses-adapter-tools`
- **Status:** 🟢 Done (P3 gate PASS · awaiting P4)
- **Parent Epic:** [`EPIC-AIBRIDGE-02-req-03-runtime-remediation.md`](../../EPIC-AIBRIDGE-02-req-03-runtime-remediation.md)
- **source:** `backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-10-responses-adapter-tools.md`
- **decision_ref:** [`STORY-AIBRIDGE-10-responses-adapter-tools.md`](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-10-responses-adapter-tools.md) · [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §5.1 (P0-02) · P0-04 · P0-13
- **Parent REQ:** [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §5.1 (P0-02) · P0-04 · P0-13
- **Package:** [`req-03-runtime-remediation/INDEX.md`](../../../../backlog-stories/req-03-runtime-remediation/INDEX.md)
- **Siblings:** [09](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [11](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Active pkg (wave):** `pkg-000008-20260913-epic-aibridge-02-story-10-responses-adapter.yaml`
- **P1 materialize:** 2026-09-13T15:40:24Z
- **P3 Done:** 2026-09-13T15:46:08Z

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Responses adapter checklist | REQ-03 [§5.1](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| Dual instructions ban | REQ-03 R3-P0-13 |
| Flat tool shape | REQ-03 R3-P0-04 |

## Scope
- Production Responses adapter: `store:false`, `parallel_tool_calls:false`, finite `max_output_tokens`, bounded timeouts, non-blocking ASGI, preserve replay items, parse `function_call`/`call_id`/usage/cache, map 429/5xx/timeouts, never leak API key.
- Tool shape Responses-flat (`type`/`name`/`parameters`/`strict`) — not nested Chat Completions `function`.
- Canonical prompt assembly: stable prefix **or** `instructions=`, not both.

## Вне scope
- Wiring `/turns` to engine (11); gateway HTTPS; inventing numeric budget defaults beyond knobs.

## Verified current state (post-P3)
- `ProductionResponsesClient` + recorded transport; `InterviewEngine.prompt_channel` xor; flat `generate_strict_tool`.
- pytest **112 passed, 14 skipped**.

## Verified current state (P1)
- `RecordingResponsesClient` only — `src/aibridge/responses_client.py`; `default_recording_engine` — `interview.py`.
- Nested tool wrap — `src/aibridge/tool_gen.py` (`"function": { ... }`).
- Dual instructions risk: system prefix **and** `instructions=` — `interview.py` (`build_stable_prefix` + `assemble_responses_request`).

## Target / AC
- [x] Every §5.1 bullet satisfied on the live/production client path (tests with fake or recorded transport OK until live smoke policy).
- [x] Emitted tool schema is Responses-flat.
- [x] Prompt assembly never duplicates instructions (prefix xor `instructions=`).
- [x] API key never appears in logs/exceptions.

## Точки в коде
- `src/aibridge/responses_client.py`, `tool_gen.py`, `interview.py`, `request_assembly.py`

## Dependencies
- [STORY-AIBRIDGE-09](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md)

## Nested tasks (pkg-000008 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-02-10-t01-production-responses-client](./task-aibridge-02-10-t01-production-responses-client/README.md) | Scope #1 knobs; AC #1/#4 | Done |
| t02 | [task-aibridge-02-10-t02-parse-replay-items](./task-aibridge-02-10-t02-parse-replay-items/README.md) | Scope #1 parse; AC #1 | Done |
| t03 | [task-aibridge-02-10-t03-responses-flat-tools](./task-aibridge-02-10-t03-responses-flat-tools/README.md) | Scope #2; AC #2 | Done |
| t04 | [task-aibridge-02-10-t04-prompt-assembly-xor](./task-aibridge-02-10-t04-prompt-assembly-xor/README.md) | Scope #3; AC #3 | Done |
| t05 | [task-aibridge-02-10-t05-story-acceptance-verification](./task-aibridge-02-10-t05-story-acceptance-verification/README.md) | AC #1–#4 gate | Done |
| t06 | [task-aibridge-02-10-t06-audit-g01-engine-acreate-asgi](./task-aibridge-02-10-t06-audit-g01-engine-acreate-asgi/README.md) | P4 G-01 | Done |
| t07 | [task-aibridge-02-10-t07-audit-g02-5xx-outcome-test](./task-aibridge-02-10-t07-audit-g02-5xx-outcome-test/README.md) | P4 G-02 | Done |
| t08 | [task-aibridge-02-10-t08-audit-g03-backlog-verified-sync](./task-aibridge-02-10-t08-audit-g03-backlog-verified-sync/README.md) | P4 G-03 | Done |
