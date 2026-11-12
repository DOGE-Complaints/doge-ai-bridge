# STORY-AIBRIDGE-20 — Full flat instructions manifest

## Meta
- **Key:** `STORY-AIBRIDGE-20-full-instructions-manifest`
- **Status:** 🟢 Implemented (P6 · next P7)
- **Parent Epic:** [`EPIC-AIBRIDGE-03-req-05-content-phase-a.md`](../../EPIC-AIBRIDGE-03-req-05-content-phase-a.md)
- **source:** `backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md`
- **decision_ref:** [`STORY-AIBRIDGE-20-full-instructions-manifest.md`](../../../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md) · [`REQ-05`](../../../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2.0 §2.2 · §4.2 · R5-A-02 · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/req-05-content-phase-a-flat-launch/TECHNICAL-ARCHITECTURE.md) ADR-2
- **Parent REQ:** [`REQ-05`](../../../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2.0 §2.2 · §4.2 · R5-A-02
- **Package:** [`req-05-content-phase-a-flat-launch/INDEX.md`](../../../../backlog-stories/req-05-content-phase-a-flat-launch/INDEX.md)
- **Siblings:** [19](../../../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md) · [21](../../../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-21-oas-image-env-docs.md) · [22](../../../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-22-content-phase-a-proof.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/req-05-content-phase-a-flat-launch/TECHNICAL-ARCHITECTURE.md) §6 ADR-2 · §4 matrix
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Active pkg (wave):** `pkg-000017-20260916-epic-aibridge-03-story-20-full-instructions-manifest.yaml`
- **P1 materialize:** 2026-09-16T12:28:09Z

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-05 §4.2 / R5-A-02 | [`REQ-05`](../../../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) |
| ADR-2 content assembly | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/req-05-content-phase-a-flat-launch/TECHNICAL-ARCHITECTURE.md) §6 |
| Manifest | `src/instructions/instructions.manifest.json` |
| Loader (schema unchanged) | `src/aibridge/content.py` |

## Scope
- In-place `src/instructions/instructions.manifest.json`: **полная** комплектация — каждый root-child в `src/instructions/` кроме самого манифеста, ровно один раз.
- Включая все Module-1 `.md` и все `schema-packs.uus_veerenni_civic.v3.*` (md + json) + `schema-packs.README.md`.
- Порядок слоёв — REQ-05 §4.2 (не `ls` наугад).
- `DOGESTONIA_PAYLOAD_SCHEMA_PATH` указывает на тот же `schema-packs.uus_veerenni_civic.v3.payload.schema.json` (текст в assembly + path для tool_gen).

## Вне scope
- Engine wiring (19); Dockerfile (21); урезанные profiles / REQ-06; layered/nested manifest; inventing files вне dump.
- Смена схемы loader (`content.py` root-child rule остаётся).

## Verified current state (post-P3 · ADR-2)
- Dump flat: `src/instructions/` — 25 root-children + manifest.
- Manifest `files[]` = 25 names in REQ-05 §4.2 order: `src/instructions/instructions.manifest.json`.
- Loader schema unchanged: `src/aibridge/content.py`.
- Tests: `tests/test_story_20_full_manifest.py` (5 passed).

## Target / AC
- [x] REQ-05 §4.2 completeness: omit любого root-child (кроме manifest) = FAIL.
- [x] Layer order matches §4.2.
- [x] Pack JSON в `files[]`; `load_content_bundle` succeeds against dir + manifest.

## Техническое решение (projected)

- **Approach (ADR-2):** заменить in-place `instructions.manifest.json`: `bundle_version` + полный `files[]` в порядке слоёв REQ-05 §4.2 / TECH §6. Pack JSON **внутри** `files[]`. Payload path dual-use: basename в assembly + `DOGESTONIA_PAYLOAD_SCHEMA_PATH` на тот же файл.
- **Completeness:** `set(files) == set(dir children) − {instructions.manifest.json}`.
- **Skill:** python-pro  
- **Arch:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/req-05-content-phase-a-flat-launch/TECHNICAL-ARCHITECTURE.md) ADR-2

## Точки в коде / артефакты
- `src/instructions/instructions.manifest.json`
- `src/aibridge/content.py` (формат без смены схемы)

## Dependencies
- None (∥ 19, 21).

## Nested tasks (pkg-000017 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-20-t01-inventory-dir-vs-req](./task-aibridge-20-t01-inventory-dir-vs-req/README.md) | Scope #1 · inventory dir vs REQ §4.2 | Done |
| t02 | [task-aibridge-20-t02-write-full-manifest](./task-aibridge-20-t02-write-full-manifest/README.md) | Scope #1–#2 · full ordered manifest | Done |
| t03 | [task-aibridge-20-t03-load-smoke](./task-aibridge-20-t03-load-smoke/README.md) | Target #3 · load + hashes | Done |
| t04 | [task-aibridge-20-t04-completeness-assert](./task-aibridge-20-t04-completeness-assert/README.md) | Target #1 · dir set == files set | Done |
| t05 | [task-aibridge-20-t05-story-gate](./task-aibridge-20-t05-story-gate/README.md) | All §4.2 AC gate | Done |
| t06 | [task-aibridge-20-t06-audit-g01-backlog-verified-sync](./task-aibridge-20-t06-audit-g01-backlog-verified-sync/README.md) | P5 G-01 · backlog §Verified sync | Done |
| t07 | [task-aibridge-20-t07-audit-g03-instructions-dir-env](./task-aibridge-20-t07-audit-g03-instructions-dir-env/README.md) | P5 G-03 · local INSTRUCTIONS_DIR | Done |
