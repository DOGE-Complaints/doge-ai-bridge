# STORY-AIBRIDGE-19 — Assembled instructions → stable prefix + tools

## Meta
- **Key:** `STORY-AIBRIDGE-19-assembled-instructions-engine-wire`
- **Status:** 🟢 Implemented (P6 audit docs closed · next P7)
- **Pipeline:** [`STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`](../../epics/EPIC-AIBRIDGE-03-req-05-content-phase-a/stories/STORY-AIBRIDGE-19-assembled-instructions-engine-wire/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md)
- **Active pkg:** `pkg-000016-20260916-epic-aibridge-03-story-19-assembled-instructions-engine-wire.yaml`
- **P1 materialize:** 2026-09-16T12:04:31Z
- **Parent REQ:** [`REQ-05`](../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2.0 §2.1 · §4.1 · R5-A-01
- **Package:** [`req-05-content-phase-a-flat-launch/INDEX.md`](INDEX.md)
- **Siblings:** [20](STORY-AIBRIDGE-20-full-instructions-manifest.md) · [21](STORY-AIBRIDGE-21-oas-image-env-docs.md) · [22](STORY-AIBRIDGE-22-content-phase-a-proof.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](./TECHNICAL-ARCHITECTURE.md) §5 ADR-1 · §4 matrix · §10.1–10.2
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)  
  Composition slice: `fastapi-expert` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/fastapi-expert/SKILL.md)
- **Related gap:** [GPT UI 05 §5](../../../../../GPT%20UI/docs/architecture/05-python-bridge-instruction-delivery.md) (G-03 WAIVED out-of-DoD this wave)

## Scope
- При успешном `verify_and_register_deployment`: non-empty `LoadedContentBundle.assembled_instructions` → `InterviewEngine` через **stable prefix** (`prompt_channel=prefix`).
- Responses **не** дублирует тот же текст в `instructions=`.
- `DeploymentBundleState.strict_tool` (при `SCHEMA_ID`+`SCHEMA_VERSION`) → interview path (`engine.tools` или эквивалент).
- Fail-closed: content_configured + deploy ready при пустом assembled → не silent empty prompt.

## Вне scope
- Полный manifest contents (20); Dockerfile OAS (21); REQ-06; ValidationContext redesign (REQ-04); channel OAS.
- Full reorder of `create_app` (stores before engine) — rejected for Phase A ([TECH §5](./TECHNICAL-ARCHITECTURE.md)).

## Verified current state
- Loader: `src/aibridge/content.py` (`assembled_instructions`).
- Deploy + optional `strict_tool`: `src/aibridge/deployment.py`.
- ADR-1 helper: `_apply_deployment_to_engine` `src/aibridge/app.py:196–230`.
- Wire after `app.state.deployment_bundle = deployment`: `app.py:429–433` (engine still constructed earlier ~327; **no** full create_app reorder).
- Prefix XOR: `interview.py` `prompt_channel=prefix` ⇒ `"instructions" not in request.payload`.
- Fail-closed empty assembled → `deployment.error=assembled_instructions_empty` → `/readyz` 503.
- Tests: `tests/test_story_19_engine_wire.py` (7 passed @ P3/P4).
- Gate: `acceptance-verification-task-aibridge-19-t05-story-gate.md` PASS 2026-09-16T12:10:09Z.

## Target / AC
- [x] REQ-05 §4.1: `prompt_channel=prefix`; assembled в stable prefix; XOR соблюдён.
- [x] Strict tool из deploy на interview path при schema id/version.
- [x] Нет silent empty instructions при content_configured + ready bundle.

## Техническое решение (landed)

- **Approach (ADR-1):** после `_init_stores` / `app.state.deployment_bundle = deployment` — **mutate** тот же `InterviewEngine`: `instructions = loaded.assembled_instructions`; `tools = [strict_tool]` если tool есть; `pack_id` из Settings schema_id/version; `prompt_channel` остаётся `"prefix"`. Helper `_apply_deployment_to_engine(...)`. Не full reorder create_app.
- **Prefix contract:** `build_stable_prefix` / `<<<INSTRUCTIONS>>>` (`request_assembly.py`; `interview.py`).
- **Fail-closed:** content_configured + not ready / empty assembled → readiness error; не silent empty prefix.
- **Skill:** python-pro · fastapi-expert  
- **Arch:** [TECHNICAL-ARCHITECTURE.md](./TECHNICAL-ARCHITECTURE.md) ADR-1

## Nested tasks (materialized under pipeline)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-19-t01-apply-deployment-helper` | Done | `_apply_deployment_to_engine` helper |
| **T02** | `task-aibridge-19-t02-wire-create-app-after-stores` | Done | Wire after `deployment_bundle` assign |
| **T03** | `task-aibridge-19-t03-tools-pack-id` | Done | `strict_tool` → tools; `pack_id` |
| **T04** | `task-aibridge-19-t04-fail-closed-empty` | Done | Fail-closed empty/not-ready |
| **T05** | `task-aibridge-19-t05-story-gate` | Done | §4.1 AC + XOR gate |
| **T06** | `task-aibridge-19-t06-audit-g01-backlog-sync` | Done | P6 G-01 backlog sync |
| **T07** | `task-aibridge-19-t07-audit-g02-pipeline-facts-refresh` | Done | P6 G-02 facts refresh |

## Точки в коде
- `src/aibridge/app.py`, `interview.py`, `deployment.py`, `content.py`, `request_assembly.py`

## Dependencies
- None (∥ 20, 21). Soft: STORY-02 Done (loader/registry).
