# STORY-AIBRIDGE-03 — Responses loop, strict tool, LLM budgets

## Meta
- **Key:** `STORY-AIBRIDGE-03-responses-tool-budgets`
- **Status:** 🟢 Done
- **Parent Epic:** [`EPIC-AIBRIDGE-01-req-01-runtime.md`](../../EPIC-AIBRIDGE-01-req-01-runtime.md)
- **source:** `backlog-stories/req-01-runtime/STORY-AIBRIDGE-03-responses-tool-budgets.md`
- **decision_ref:** [`STORY-AIBRIDGE-03-responses-tool-budgets.md`](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-03-responses-tool-budgets.md) · [`REQ-01`](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §9–§12, §10, §17 · [`00-overview.md`](../../../../../architecture/runtime/00-overview.md) · [`03-confirm-gateway.md`](../../../../../architecture/runtime/03-confirm-gateway.md) · [`04-ops-security.md`](../../../../../architecture/runtime/04-ops-security.md)
- **Parent REQ:** [`REQ-01`](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §9–§12, §10 `store:false`, §17 budgets
- **Package:** [`req-01-runtime/INDEX.md`](../../../../backlog-stories/req-01-runtime/INDEX.md)
- **Siblings:** [02](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-02-content-bundle-registry.md) · [04](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-04-dual-confirm-tokens.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Wire OAS:** [`story-intake-actions.openapi.yaml`](../../../../../openapi/story-intake-actions.openapi.yaml)
- **Active pkg (wave):** `pkg-000003-20260912-epic-aibridge-01-story-03-responses-tool.yaml`
- **P1 materialize:** 2026-09-12T21:16:48Z
- **P3 Done:** 2026-09-12T21:23:18Z
- **Gate:** [acceptance-verification … t06](acceptance-verification-task-aibridge-01-03-t06-story-acceptance-verification.md) PASS
- **Run summary:** [run-summary-20260912-2123-story-aibridge-03-p3.md](../../../../run-reports/run-summary-20260912-2123-story-aibridge-03-p3.md)
## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Seams: aibridge owns Responses/tools | [00-overview.md §9](../../../../../architecture/runtime/00-overview.md) |
| Pre-send safe failure (budget/timeout) — no gateway side effect | [03-confirm-gateway.md §4](../../../../../architecture/runtime/03-confirm-gateway.md) |
| Budget env knobs (numeric defaults Unknown) | [04-ops-security.md §2](../../../../../architecture/runtime/04-ops-security.md); REQ-01 [§17](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| OpenAPI reuse + strict tool + pack projection + server-owned fields | REQ-01 [§9 AIB-OAS / AIB-GEN](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Responses: `store:false`, serialization, tool lifecycle, constraints | REQ-01 [§10 AIB-RSP-01…05](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Prompt caching stable prefix + observability hooks | REQ-01 [§11 AIB-CACHE-01…03](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Request assembly + three validation gates + draft hash | REQ-01 [§12 AIB-REQ-01…03](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Wire OAS for tool/wire shape | [`story-intake-actions.openapi.yaml`](../../../../../openapi/story-intake-actions.openapi.yaml) |
| Metrics for cache/budget (implement full series in 06) | [04-ops-security.md §3](../../../../../architecture/runtime/04-ops-security.md) |

## Scope
- Responses API with `store: false`; local replayable history in Postgres (bundle-pinned session).
- Deterministic **strict** tool from wire OAS + pack projection (`strict: true`); server-owned fields never model-overridable.
- Turn serialization per session; `parallel_tool_calls: false` where supported.
- Enforce budget / rate / timeout env knobs; bounded fail; **no gateway side effect**; last confirmed state kept.
- Prompt stable-prefix ordering; cache telemetry hooks (full `/metrics` exposure in 06).

## Вне scope
- Dual-confirm Send execution (04/05); inventing numeric budget defaults (placeholders required; measure later — [00-overview §13](../../../../../architecture/runtime/00-overview.md)).

## Verified current state
- Responses assemble always `store:false` — `responses_client.py` + `InterviewEngine` (Recording client; live OpenAI HTTP out of scope).
- Strict tool from wire OAS + pack — `tool_gen.py`; unsupported `oneOf`/… → `ToolGenError` / deploy `tool_gen_failed`.
- Turn lock + budgets + three gates + cache hooks — see modules under `src/aibridge/`.
- Channel HTTP turns still façade stub (`channel.py`); wiring live model loop deferred to later stories.
- Budget numeric defaults: **None/unset** (Unknown until measured).

## Target / AC
- [x] Every Responses request has `store: false`.
- [x] Tool schema deterministic; unsupported OpenAPI constructs fail startup (no silent non-strict).
- [x] Budget breach → resident-safe error, no gateway call, redacted metric reason.
- [x] Model cannot override pack / origin / URL / auth.
- [x] Three validation gates per AIB-REQ-02 before any Send-authorized path.

## Точки в коде
- `src/aibridge/{responses_client,history,interview,tool_gen,request_assembly,budgets,turn_lock}.py`
- `config.py` OPENAI_* + budget env; `deployment.py` strict tool verify when schema_id/version set.

## Dependencies
- [STORY-AIBRIDGE-02](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-02-content-bundle-registry.md).

## Nested tasks (pkg-000003 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-01-03-t01-responses-store-false-history](./task-aibridge-01-03-t01-responses-store-false-history/README.md) | Scope #1; AC #1 | Done |
| t02 | [task-aibridge-01-03-t02-strict-tool-oas-pack](./task-aibridge-01-03-t02-strict-tool-oas-pack/README.md) | Scope #2; AC #2,#4 | Done |
| t03 | [task-aibridge-01-03-t03-turn-serialization](./task-aibridge-01-03-t03-turn-serialization/README.md) | Scope #3 | Done |
| t04 | [task-aibridge-01-03-t04-llm-budgets-no-gateway](./task-aibridge-01-03-t04-llm-budgets-no-gateway/README.md) | Scope #4; AC #3 | Done |
| t05 | [task-aibridge-01-03-t05-validation-gates-cache-hooks](./task-aibridge-01-03-t05-validation-gates-cache-hooks/README.md) | Scope #5; AC #5 | Done |
| t06 | [task-aibridge-01-03-t06-story-acceptance-verification](./task-aibridge-01-03-t06-story-acceptance-verification/README.md) | AC #1–#5 gate | Done |
| t07 | [task-aibridge-01-03-t07-audit-g02-openai-timeout](./task-aibridge-01-03-t07-audit-g02-openai-timeout/README.md) | P5 G-02 | Done (P6) |
| t08 | [task-aibridge-01-03-t08-audit-g03-backlog-verified-store](./task-aibridge-01-03-t08-audit-g03-backlog-verified-store/README.md) | P5 G-03 | Done (P6) |
