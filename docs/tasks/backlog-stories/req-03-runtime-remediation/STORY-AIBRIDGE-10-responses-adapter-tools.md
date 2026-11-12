# STORY-AIBRIDGE-10 — Production Responses adapter + flat tools + prompt

## Meta
- **Key:** `STORY-AIBRIDGE-10-responses-adapter-tools`
- **Status:** Done
- **Parent REQ:** [`REQ-03`](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §5.1 (P0-02) · P0-04 · P0-13
- **Package:** [`req-03-runtime-remediation/INDEX.md`](INDEX.md)
- **Siblings:** [09](STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [11](STORY-AIBRIDGE-11-coordinator-pause-resume-send.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)

## Doc pointers

| Topic | Where |
|-------|--------|
| Responses adapter checklist | REQ-03 [§5.1](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| Dual instructions ban | REQ-03 R3-P0-13 |
| Flat tool shape | REQ-03 R3-P0-04 |

## Scope
- Production Responses adapter: `store:false`, `parallel_tool_calls:false`, finite `max_output_tokens`, bounded timeouts, non-blocking ASGI, preserve replay items, parse `function_call`/`call_id`/usage/cache, map 429/5xx/timeouts, never leak API key.
- Tool shape Responses-flat (`type`/`name`/`parameters`/`strict`) — not nested Chat Completions `function`.
- Canonical prompt assembly: stable prefix **or** `instructions=`, not both.

## Вне scope
- Wiring `/turns` to engine (11); gateway HTTPS; inventing numeric budget defaults beyond knobs.

## Verified current state
- `ProductionResponsesClient` + `RecordingResponsesClient` / recorded transports — `src/aibridge/responses_client.py`.
- Responses-flat tools — `generate_strict_tool` (`type`/`name`/`parameters`/`strict`); nested Chat Completions wrap removed; `to_responses_flat_tool` normalizer remains.
- Prompt xor — `InterviewEngine.prompt_channel` (`prefix` \| `instructions`); `assert_prompt_xor` fail-closed.
- ASGI contract — prefer `await InterviewEngine.arun_turn` → `client.acreate` (sync `run_turn` for tests/non-ASGI). `/turns` wire → STORY-11.

## Target / AC
- [x] Every §5.1 bullet satisfied on the live/production client path (tests with fake or recorded transport OK until live smoke policy).
- [x] Emitted tool schema is Responses-flat.
- [x] Prompt assembly never duplicates instructions (prefix xor `instructions=`).
- [x] API key never appears in logs/exceptions.

## Точки в коде
- `src/aibridge/responses_client.py`, `tool_gen.py`, `interview.py`, `request_assembly.py`

## Dependencies
- [STORY-AIBRIDGE-09](STORY-AIBRIDGE-09-postgres-ssot-migrations.md)
