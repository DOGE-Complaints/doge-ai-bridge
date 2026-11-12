# STORY-AIBRIDGE-19 — Assembled instructions → stable prefix + tools

## Meta
- **Key:** `STORY-AIBRIDGE-19-assembled-instructions-engine-wire`
- **Status:** 🟢 Implemented (P6 audit docs closed · next P7)
- **Parent Epic:** [`EPIC-AIBRIDGE-03-req-05-content-phase-a.md`](../../EPIC-AIBRIDGE-03-req-05-content-phase-a.md)
- **source:** `backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`
- **decision_ref:** [`STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`](../../../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md) · [`REQ-05`](../../../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2.0 §2.1 · §4.1 · R5-A-01 · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/req-05-content-phase-a-flat-launch/TECHNICAL-ARCHITECTURE.md) ADR-1
- **Parent REQ:** [`REQ-05`](../../../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2.0 §2.1 · §4.1 · R5-A-01
- **Package:** [`req-05-content-phase-a-flat-launch/INDEX.md`](../../../../backlog-stories/req-05-content-phase-a-flat-launch/INDEX.md)
- **Siblings:** [20](../../../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md) · [21](../../../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-21-oas-image-env-docs.md) · [22](../../../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-22-content-phase-a-proof.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/req-05-content-phase-a-flat-launch/TECHNICAL-ARCHITECTURE.md) §5 ADR-1 · §4 matrix · §10.1–10.2
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)  
  Composition slice: `fastapi-expert` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/fastapi-expert/SKILL.md)
- **Related gap:** [GPT UI 05 §5](../../../../../../../GPT%20UI/docs/architecture/05-python-bridge-instruction-delivery.md)
- **Active pkg (wave):** `pkg-000016-20260916-epic-aibridge-03-story-19-assembled-instructions-engine-wire.yaml`
- **P1 materialize:** 2026-09-16T12:04:31Z

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-05 §4.1 / R5-A-01 | [`REQ-05`](../../../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) |
| ADR-1 composition | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/req-05-content-phase-a-flat-launch/TECHNICAL-ARCHITECTURE.md) §5 |
| Loader | `src/aibridge/content.py` |
| Deploy / strict_tool | `src/aibridge/deployment.py` |
| Engine / XOR prefix | `src/aibridge/interview.py` · `request_assembly.py` |
| create_app ordering | `src/aibridge/app.py` |

## Scope
- При успешном `verify_and_register_deployment`: non-empty `LoadedContentBundle.assembled_instructions` → `InterviewEngine` через **stable prefix** (`prompt_channel=prefix`).
- Responses **не** дублирует тот же текст в `instructions=`.
- `DeploymentBundleState.strict_tool` (при `SCHEMA_ID`+`SCHEMA_VERSION`) → interview path (`engine.tools` или эквивалент).
- Fail-closed: content_configured + deploy ready при пустом assembled → не silent empty prompt.

## Вне scope
- Полный manifest contents (20); Dockerfile OAS (21); REQ-06; ValidationContext redesign (REQ-04); channel OAS.
- Full reorder of `create_app` (stores before engine) — rejected for Phase A ([TECH §5](../../../../backlog-stories/req-05-content-phase-a-flat-launch/TECHNICAL-ARCHITECTURE.md)).

## Verified current state (post-P3 · ADR-1)
- Loader: `src/aibridge/content.py` (`assembled_instructions`).
- Deploy + optional `strict_tool`: `src/aibridge/deployment.py`.
- Helper: `_apply_deployment_to_engine` `src/aibridge/app.py:196–230`.
- Wire: after `app.state.deployment_bundle = deployment` → helper `app.py:429–433`.
- ADR-1 order: engine constructed **before** `_init_stores` (~327 vs ~420); mutate after deploy — **no** full create_app reorder.
- Fail-closed: empty/whitespace assembled → `error=assembled_instructions_empty`; `/readyz` 503.
- Tests: `tests/test_story_19_engine_wire.py`.

## Target / AC
- [x] REQ-05 §4.1: `prompt_channel=prefix`; assembled в stable prefix; XOR соблюдён.
- [x] Strict tool из deploy на interview path при schema id/version.
- [x] Нет silent empty instructions при content_configured + ready bundle.

## Техническое решение (projected)

- **Approach (ADR-1):** после `_init_stores` / `app.state.deployment_bundle = deployment` — **mutate** тот же `InterviewEngine`: `instructions = loaded.assembled_instructions`; `tools = [strict_tool]` если tool есть; `pack_id` из Settings schema_id/version; `prompt_channel` остаётся `"prefix"`. Helper e.g. `_apply_deployment_to_engine(...)`. Не full reorder create_app.
- **Prefix contract:** `build_stable_prefix` / `<<<INSTRUCTIONS>>>` (`request_assembly.py:74–103`; `interview.py:78–112`).
- **Fail-closed:** content_configured + not ready / empty assembled → readiness error; не silent empty prefix.
- **Skill:** python-pro · fastapi-expert  
- **Arch:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/req-05-content-phase-a-flat-launch/TECHNICAL-ARCHITECTURE.md) ADR-1

## Точки в коде
- `src/aibridge/app.py`, `interview.py`, `deployment.py`, `content.py`, `request_assembly.py`

## Dependencies
- None (∥ 20, 21). Soft: STORY-02 Done (loader/registry).

## Nested tasks (pkg-000016 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-19-t01-apply-deployment-helper](./task-aibridge-19-t01-apply-deployment-helper/README.md) | Scope #1 · ADR-1 helper | Done |
| t02 | [task-aibridge-19-t02-wire-create-app-after-stores](./task-aibridge-19-t02-wire-create-app-after-stores/README.md) | Scope #1 · wire after stores | Done |
| t03 | [task-aibridge-19-t03-tools-pack-id](./task-aibridge-19-t03-tools-pack-id/README.md) | Scope #3 · tools + pack_id | Done |
| t04 | [task-aibridge-19-t04-fail-closed-empty](./task-aibridge-19-t04-fail-closed-empty/README.md) | Scope #4 · Target #3 | Done |
| t05 | [task-aibridge-19-t05-story-gate](./task-aibridge-19-t05-story-gate/README.md) | Target AC gate | Done |
| t06 | [task-aibridge-19-t06-audit-g01-backlog-sync](./task-aibridge-19-t06-audit-g01-backlog-sync/README.md) | P5 G-01 backlog sync | Done |
| t07 | [task-aibridge-19-t07-audit-g02-pipeline-facts-refresh](./task-aibridge-19-t07-audit-g02-pipeline-facts-refresh/README.md) | P5 G-02 facts refresh | Done |
