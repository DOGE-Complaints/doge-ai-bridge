# STORY-AIBRIDGE-03 — Responses loop, strict tool, LLM budgets

## Meta
- **Key:** `STORY-AIBRIDGE-03-responses-tool-budgets`
- **Status:** Done
- **Parent REQ:** [`REQ-01`](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §9–§12, §10 `store:false`, §17 budgets
- **Package:** [`req-01-runtime/INDEX.md`](INDEX.md)
- **Siblings:** [02](STORY-AIBRIDGE-02-content-bundle-registry.md) · [04](STORY-AIBRIDGE-04-dual-confirm-tokens.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **P3 Done:** 2026-09-12T21:23:18Z · gate PASS · pytest 50 passed, 1 skipped

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Seams: aibridge owns Responses/tools | [00-overview.md §9](../../../architecture/runtime/00-overview.md) |
| Pre-send safe failure (budget/timeout) — no gateway side effect | [03-confirm-gateway.md §4](../../../architecture/runtime/03-confirm-gateway.md) |
| Budget env knobs (numeric defaults Unknown) | [04-ops-security.md §2](../../../architecture/runtime/04-ops-security.md); REQ-01 [§17](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| OpenAPI reuse + strict tool + pack projection + server-owned fields | REQ-01 [§9 AIB-OAS / AIB-GEN](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Responses: `store:false`, serialization, tool lifecycle, constraints | REQ-01 [§10 AIB-RSP-01…05](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Prompt caching stable prefix + observability hooks | REQ-01 [§11 AIB-CACHE-01…03](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Request assembly + three validation gates + draft hash | REQ-01 [§12 AIB-REQ-01…03](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Wire OAS for tool/wire shape | [`story-intake-actions.openapi.yaml`](../../../openapi/story-intake-actions.openapi.yaml) |
| Metrics for cache/budget (implement full series in 06) | [04-ops-security.md §3](../../../architecture/runtime/04-ops-security.md) |

## Scope
- Responses API with `store: false`; local replayable history in Postgres (bundle-pinned session).
- Deterministic **strict** tool from wire OAS + pack projection (`strict: true`); server-owned fields never model-overridable.
- Turn serialization per session; `parallel_tool_calls: false` where supported.
- Enforce budget / rate / timeout env knobs; bounded fail; **no gateway side effect**; last confirmed state kept.
- Prompt stable-prefix ordering; cache telemetry hooks (full `/metrics` exposure in 06).

## Вне scope
- Dual-confirm Send execution (04/05); inventing numeric budget defaults (placeholders required; measure later — [00-overview §13](../../../architecture/runtime/00-overview.md)).

## Verified current state
- Responses assemble always `store: false` — `src/aibridge/responses_client.py` + `InterviewEngine`.
- Strict tool OAS+pack — `tool_gen.py`; deploy fail-fast `tool_gen_failed` when schema_id/version set.
- Turn lock, budgets (incl. timeout elapsed check), three gates, cache hooks — on disk; unit tests green.
- Live OpenAI HTTP client: **Absent** (RecordingResponsesClient only); channel HTTP turns still façade stub.
- Replayable history Postgres: **deferred** → [STORY-AIBRIDGE-07](STORY-AIBRIDGE-07-replayable-history-postgres.md) (P4 G-01 WAIVED out-of-DoD).
- `OPENAI_STORE_RESPONSES=true` rejected at settings load (forces store:false).

## Target / AC
- [x] Every Responses request has `store: false`.
- [x] Tool schema deterministic; unsupported OpenAPI constructs fail startup (no silent non-strict).
- [x] Budget breach → resident-safe error, no gateway call, redacted metric reason.
- [x] Model cannot override pack / origin / URL / auth.
- [x] Three validation gates per AIB-REQ-02 before any Send-authorized path.

## Точки в коде
- `src/aibridge/responses_client.py`, `history.py`, `interview.py`
- `src/aibridge/tool_gen.py`, `request_assembly.py`, `budgets.py`, `turn_lock.py`
- Deploy fail-fast: `deployment.py` + `DOGESTONIA_SCHEMA_ID`/`VERSION`

## Dependencies
- [STORY-AIBRIDGE-02](STORY-AIBRIDGE-02-content-bundle-registry.md).
