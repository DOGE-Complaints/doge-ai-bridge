# STORY-AIBRIDGE-20 — Full flat instructions manifest

## Meta
- **Key:** `STORY-AIBRIDGE-20-full-instructions-manifest`
- **Status:** 🟢 Implemented (P6 · next P7)
- **Pipeline:** [`STORY-AIBRIDGE-20-full-instructions-manifest.md`](../../epics/EPIC-AIBRIDGE-03-req-05-content-phase-a/stories/STORY-AIBRIDGE-20-full-instructions-manifest/STORY-AIBRIDGE-20-full-instructions-manifest.md)
- **Active pkg:** `pkg-000017-20260916-epic-aibridge-03-story-20-full-instructions-manifest.yaml`
- **P1 materialize:** 2026-09-16T12:28:09Z
- **Parent REQ:** [`REQ-05`](../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2.0 §2.2 · §4.2 · R5-A-02
- **Package:** [`req-05-content-phase-a-flat-launch/INDEX.md`](INDEX.md)
- **Siblings:** [19](STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md) · [21](STORY-AIBRIDGE-21-oas-image-env-docs.md) · [22](STORY-AIBRIDGE-22-content-phase-a-proof.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](./TECHNICAL-ARCHITECTURE.md) §6 ADR-2 · §4 matrix
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)

## Scope
- In-place `src/instructions/instructions.manifest.json`: **полная** комплектация — каждый root-child в `src/instructions/` кроме самого манифеста, ровно один раз.
- Включая все Module-1 `.md` и все `schema-packs.uus_veerenni_civic.v3.*` (md + json) + `schema-packs.README.md`.
- Порядок слоёв — REQ-05 §4.2 (не `ls` наугад).
- `DOGESTONIA_PAYLOAD_SCHEMA_PATH` указывает на тот же `schema-packs.uus_veerenni_civic.v3.payload.schema.json` (текст в assembly + path для tool_gen).

## Вне scope
- Engine wiring (19); Dockerfile (21); урезанные profiles / REQ-06; layered/nested manifest; inventing files вне dump.
- Смена схемы loader (`content.py` root-child rule остаётся).

## Verified current state (post-P3 · ADR-2)
- Dump flat: `src/instructions/` — **25** root-children + `instructions.manifest.json`.
- Manifest `files[]` = **25** names in REQ-05 §4.2 order: `src/instructions/instructions.manifest.json` (full dump; not a 6-file subset).
- Completeness: `set(files) == set(dir children) − {instructions.manifest.json}` — asserted in `tests/test_story_20_full_manifest.py` (5 passed @ P3/P4).
- Loader schema unchanged (root-child-only): `src/aibridge/content.py`.
- Gate PASS 2026-09-16T12:32:27Z · nested t01–t05 Done.

## Target / AC
- [x] REQ-05 §4.2 completeness: omit любого root-child (кроме manifest) = FAIL.
- [x] Layer order matches §4.2.
- [x] Pack JSON в `files[]`; `load_content_bundle` succeeds against dir + manifest.

## Техническое решение (projected)

- **Approach (ADR-2):** заменить in-place `instructions.manifest.json`: `bundle_version` + полный `files[]` в порядке слоёв REQ-05 §4.2 / TECH §6. Pack JSON **внутри** `files[]`. Payload path dual-use: basename в assembly + `DOGESTONIA_PAYLOAD_SCHEMA_PATH` на тот же файл.
- **Completeness:** `set(files) == set(dir children) − {instructions.manifest.json}`.
- **Skill:** python-pro  
- **Arch:** [TECHNICAL-ARCHITECTURE.md](./TECHNICAL-ARCHITECTURE.md) ADR-2

## Nested tasks (materialized — pkg-000017)

> Pipeline: [`STORY-AIBRIDGE-20-full-instructions-manifest.md`](../../epics/EPIC-AIBRIDGE-03-req-05-content-phase-a/stories/STORY-AIBRIDGE-20-full-instructions-manifest/STORY-AIBRIDGE-20-full-instructions-manifest.md)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-20-t01-inventory-dir-vs-req` | Done | Inventory `src/instructions/` vs REQ §4.2 layer list |
| **T02** | `task-aibridge-20-t02-write-full-manifest` | Done | Write full ordered `instructions.manifest.json` in-place |
| **T03** | `task-aibridge-20-t03-load-smoke` | Done | `load_content_bundle` succeeds; hashes non-empty |
| **T04** | `task-aibridge-20-t04-completeness-assert` | Done | Assert no omit (dir set == files set) |
| **T05** | `task-aibridge-20-t05-story-gate` | Done | All §4.2 AC checked |
| **T06** | `task-aibridge-20-t06-audit-g01-backlog-verified-sync` | Done | P5 G-01 · sync §Verified (drop 6-file FAIL) |
| **T07** | `task-aibridge-20-t07-audit-g03-instructions-dir-env` | Done | P5 G-03 · local INSTRUCTIONS_DIR directory |

## Точки в коде / артефакты
- `src/instructions/instructions.manifest.json`
- `src/aibridge/content.py` (формат без смены схемы)

## Dependencies
- None (∥ 19, 21).
