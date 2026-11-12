# STORY-AIBRIDGE-21 — OpenAPI in image + Phase A env docs

## Meta
- **Key:** `STORY-AIBRIDGE-21-oas-image-env-docs`
- **Status:** 🟢 Implemented (P3 · next P4)
- **Pipeline:** [`STORY-AIBRIDGE-21-oas-image-env-docs.md`](../../epics/EPIC-AIBRIDGE-03-req-05-content-phase-a/stories/STORY-AIBRIDGE-21-oas-image-env-docs/STORY-AIBRIDGE-21-oas-image-env-docs.md)
- **Active pkg:** `pkg-000018-20260916-epic-aibridge-03-story-21-oas-image-env-docs.yaml`
- **P1 materialize:** 2026-09-16T12:52:52Z
- **Parent REQ:** [`REQ-05`](../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2.0 §2.3–2.4 · §4.3–4.4 · R5-A-03 · R5-A-04
- **Package:** [`req-05-content-phase-a-flat-launch/INDEX.md`](INDEX.md)
- **Siblings:** [19](STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md) · [20](STORY-AIBRIDGE-20-full-instructions-manifest.md) · [22](STORY-AIBRIDGE-22-content-phase-a-proof.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](./TECHNICAL-ARCHITECTURE.md) §7 ADR-3 · §9 env map
- **Skill declared:** `devops-engineer` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/devops-engineer/SKILL.md)

## Scope
- Runtime image содержит `docs/openapi/` (оба YAML) без manual mount.
- `DOGESTONIA_OPENAPI_PATH` → Story Intake wire (`story-intake-actions.openapi.yaml`), не channel façade.
- Channel OAS копируется с каталогом, но **не** в instruction `files[]`.
- Документировать Phase A pins в `.env.example` и `docs/runbooks/aibridge-web-service-local-railway.md` (REQ-05 §4.3); без новых alias.

## Вне scope
- Multi-repo CI (REQ-06); inventing secrets; redesign channel OAS; Railpack spaceship.
- Putting OAS under `src/instructions/` (rejected ADR-3).

## Verified current state (post-P3 · ADR-3)
- Dockerfile: `COPY docs/openapi ./docs/openapi` (both YAML in image).
- Phase A pins: `.env.example` §8 + runbook §1.1b (local + `/app`).
- OPENAPI_PATH = Story Intake wire; channel not in instruction `files[]`.
- Tests: `tests/test_story_21_oas_path_contract.py` (3 passed).

## Target / AC
- [x] REQ-05 §4.4: openapi dir in image; OPENAPI_PATH = Story Intake.
- [x] REQ-05 §4.3: documented pins (incl. SCHEMA_ID/VERSION uus_veerenni_civic/v3).

## Техническое решение (projected)

- **Approach (ADR-3):** `COPY docs/openapi ./docs/openapi` in root `Dockerfile` (WORKDIR `/app`). Env pins: local relative vs image `/app/...` per TECH §9. OPENAPI_PATH = story-intake only; channel YAML rides along in dir.
- **Docs:** Phase A block in `.env.example` + `aibridge-web-service-local-railway.md` (no new aliases).
- **Skill:** devops-engineer (+ docs)  
- **Arch:** [TECHNICAL-ARCHITECTURE.md](./TECHNICAL-ARCHITECTURE.md) ADR-3 · §9

## Nested tasks (materialized — pkg-000018)

> Pipeline: [`STORY-AIBRIDGE-21-oas-image-env-docs.md`](../../epics/EPIC-AIBRIDGE-03-req-05-content-phase-a/stories/STORY-AIBRIDGE-21-oas-image-env-docs/STORY-AIBRIDGE-21-oas-image-env-docs.md)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-21-t01-dockerfile-copy-openapi` | Done | `COPY docs/openapi` (both YAMLs) into image |
| **T02** | `task-aibridge-21-t02-env-example-phase-a` | Done | Document Phase A pins in `.env.example` (local + `/app` note) |
| **T03** | `task-aibridge-21-t03-web-runbook-pins` | Done | Same pins in web-service local/Railway runbook |
| **T04** | `task-aibridge-21-t04-path-contract` | Done | Assert OPENAPI_PATH = story-intake; channel not in manifest `files[]` |
| **T05** | `task-aibridge-21-t05-story-gate` | Done | §4.3–4.4 AC checked |

## Точки в коде / артефакты
- `Dockerfile`, `docs/openapi/*`, `.env.example`, `docs/runbooks/aibridge-web-service-local-railway.md`, `src/aibridge/config.py` (names)

## Dependencies
- None (∥ 19, 20). Soft: 20 for MANIFEST path example consistency.
