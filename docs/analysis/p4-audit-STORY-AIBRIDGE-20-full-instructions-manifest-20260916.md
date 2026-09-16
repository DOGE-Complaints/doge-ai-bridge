# P4 Audit — STORY-AIBRIDGE-20-full-instructions-manifest

| Field | Value |
|-------|-------|
| **Date** | 2026-09-16T12:37:00Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-03-…/STORY-AIBRIDGE-20-full-instructions-manifest/STORY-AIBRIDGE-20-full-instructions-manifest.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md` |
| **Method** | Read/Glob + dir/manifest set-diff + live pytest story-20; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (REQ-05 §4.2 / R5-A-02)** | **PASS** — full 25-file in-place manifest · §4.2 order · pack JSON in `files[]` · load smoke |
| **Bullrun t01–t05 Done** | **Confirmed** vs artifacts + gate PASS 2026-09-16T12:32:27Z |
| **OPEN gaps** | **1 Medium · 0 Low · 2 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **5 passed** (`tests/test_story_20_full_manifest.py`) @ 2026-09-16T12:37Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-20** | 🟢 Implemented (P3 · next P4) · pkg-000017 | **Confirmed** ADR-2 full manifest; gate PASS; **this P4** → next **P5** |
| **t01** | Done — inventory dir vs REQ | **Confirmed** `…/t01…/INVENTORY.md` · 25 children · layers 1–7 |
| **t02** | Done — write full manifest | **Confirmed** `src/instructions/instructions.manifest.json` · 25 `files[]` · `bundle_version=uus-veerenni-v3-local-1` |
| **t03** | Done — load smoke | **Confirmed** `test_load_content_bundle_full_dump` · hashes non-empty |
| **t04** | Done — completeness assert | **Confirmed** `test_completeness_dir_set_equals_files_set` · `test_omit_would_fail_completeness` |
| **t05** | Done — story gate PASS | **Confirmed** `acceptance-verification-…t05…md` + pytest 5 passed |
| **pkg-000017** | Active (story 20 P3 · next P4) | `--verify` **ok 5 paths** @ audit time |
| **STORY-19** | Done (P8) | Sibling; not re-audited |
| **Siblings 21–22** | Todo (INDEX) | **Out of scope** this story |

---

## AC matrix (`$storyFile` Target · REQ-05 §4.2)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | Completeness: omit любого root-child (кроме manifest) = FAIL | **PASS (CI/assert)** · **PARTIAL (runtime loader)** | Live: `set(files)==set(dir children)` · 25=25 · omit/extra empty. Tests assert equality. Loader `content.py` still loads only `files[]` — **no** dir-vs-manifest fail-closed → **G-02** |
| 2 | Layer order matches §4.2 | **PASS** | Manifest `files` == `REQ_05_42_ORDER` in `tests/test_story_20_full_manifest.py`; matches REQ-05 §4.2 list |
| 3 | Pack JSON в `files[]`; `load_content_bundle` succeeds | **PASS** | pack/payload/taxonomy JSON present; `test_load_content_bundle_full_dump` + `test_pack_json_in_files` |

### Scope extras

| Item | Status | Evidence |
|------|--------|----------|
| ADR-2 in-place; no loader schema change | **PASS** | Manifest replaced; `content.py` unchanged schema |
| Channel OAS not in `files[]` | **PASS** | Asserted absent in completeness test |
| Payload path dual-use (same basename) | **PASS (artifact)** · **PARTIAL (local .env DIR)** | PAYLOAD path in `.env` points at pack payload JSON; **INSTRUCTIONS_DIR** malformed → **G-03** |
| Engine wire / Dockerfile | **Out of scope** | Stories 19 / 21 |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Info** | Backlog `$storyFile` «Verified current state» still claims **6-file subset FAIL**, while Meta/AC/nested T01–T05 say Implemented/Done and on-disk manifest is full (25). Contradicts pipeline post-P3 facts. | Sync backlog verified-state to post-P3 (25 files + order + tests); drop stale subset FAIL claim. |
| **G-02** | **Info** | REQ «omit = FAIL» / Target #1 satisfied by **pytest set equality** only. `load_content_bundle` / `verify_and_register_deployment` do **not** compare dir children to `files[]` (story explicitly keeps loader schema). Incomplete `files[]` still loads silently at runtime. | Keep CI gate (current); or later fail-closed completeness in loader/readyz (would be schema-adjacent — likely STORY-22 / new task); do not invent loader change under STORY-20 DoD. |
| **G-03** | **Medium** | Local `doge-ai-bridge/.env` sets `DOGESTONIA_INSTRUCTIONS_DIR=src/instructions/manifest.json` — path **does not exist** / is not the instructions **directory** (`src/instructions`). `DOGESTONIA_PAYLOAD_SCHEMA_PATH` correctly targets pack payload JSON. Mis-set DIR breaks `content_configured` / load if this env is used. `.env.example` Phase A pins still empty (owned primarily by STORY-21). | Point `DOGESTONIA_INSTRUCTIONS_DIR` at `src/instructions` (or image `/app/…`); document pins in `.env.example` / runbook (STORY-21); verify `content_configured` + load against full manifest. |

### Non-gaps

| Topic | Note |
|-------|------|
| Inventing files outside dump | None; 25 children match §4.2 |
| Loader join / root-child-only | Unchanged; intentional |
| Fixtures `tests/fixtures/content/` 2-file subset | Test harness only — not production dump |
| Channel OAS in instruction `files[]` | Correctly excluded |

---

## Cited paths

- `src/instructions/instructions.manifest.json` (25 `files[]`)
- `src/instructions/` (25 root-children + manifest)
- `src/aibridge/content.py` (`load_manifest` / `load_content_bundle`)
- `tests/test_story_20_full_manifest.py`
- `…/task-aibridge-20-t01-…/INVENTORY.md`
- Gate: `acceptance-verification-task-aibridge-20-t05-story-gate.md`
- REQ-05 §4.2 · R5-A-02 · TECH ADR-2
- Ops residual: `doge-ai-bridge/.env` · `.env.example`

---

## Handoff

- **OPEN:** G-01 (Info), G-02 (Info), G-03 (Medium)
- **Critical:** 0
- **OPEN counts:** Critical **0** · Medium **1** · Low **0** · Info **2**
- **next:** **P5** disposition
