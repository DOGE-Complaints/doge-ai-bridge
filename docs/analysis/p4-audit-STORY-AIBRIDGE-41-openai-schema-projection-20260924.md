# P4 Audit — STORY-AIBRIDGE-41-openai-schema-projection

| Field | Value |
|-------|-------|
| **Date** | 2026-09-24T11:02:40Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-05-…/STORY-AIBRIDGE-41-openai-schema-projection/STORY-AIBRIDGE-41-openai-schema-projection.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-41-openai-schema-projection.md` |
| **Method** | Read/Glob + live pytest `tests/test_openai_schema_projection.py` + `tests/test_tool_gen.py` (12) + code paths `tool_gen.py` / `deployment.py` / `readiness.py`; pack disk `uniqueItems`; no product patches; no live OpenAI/TG invent |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway / live Telegram / live OpenAI** | **No** Railway SUCCESS · **No** live Telegram/OpenAI PASS invented |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (projection / no disk rewrite / fail-closed)** | **PASS (core)** — policy + `project_schema_for_openai` + wire in `generate_strict_tool`; pack retains `uniqueItems`; tool strips keyword |
| **Bullrun t01–t04 Done** | **Confirmed** vs code + acceptance + gate PASS 2026-09-24T11:00:27Z |
| **OPEN gaps** | **0 Critical · 0 Medium · 2 Low · 2 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **12 passed** (`test_openai_schema_projection.py` + `test_tool_gen.py`) @ 2026-09-24T11:02:40Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-41** | ✅ P3 Done · next P4 · pkg-000040 | **Confirmed** projection + 12 tests · **this P4** → next **P5** |
| **t01** | Done — policy + strip helper | **Confirmed** `OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS` · `project_schema_for_openai` |
| **t02** | Done — wire generate_strict_tool | **Confirmed** project + `assert_openai_projection_clean` + non-blocking `_emit_projection_ready_event` |
| **t03** | Done — AC/T-COMPAT · 12 passed | **Confirmed** **12 passed** this P4 · residual T-COMPAT-06 soft (**G-02**) |
| **t04** | Done · PASS | **Confirmed** acceptance gate |
| **pkg-000040** | Active · 4 paths | YAML under `aibridge-active-packages/` |
| **active-package.current comment** | «next P2» | **Stale** after P3 → **Info G-04** |

---

## AC matrix (`$storyFile` / pipeline · REQ-07 · TECH-ARCH §2.1–2.2)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| AC-01 | Pack still has `"uniqueItems": true` on houses | **PASS** | `src/instructions/schema-packs.uus_veerenni_civic.v3.payload.schema.json` · test disk bytes + keyword present |
| AC-02 | Story Intake OAS not rewritten | **PASS** | `test_disk_pack_and_oas_unchanged` · generate reads only |
| AC-03 | OpenAI tool: no `uniqueItems`, `strict: true`, name `postStoryDraftStash` | **PASS** | `test_generate_tool_no_unique_items_on_canonical_pack` · live generate probe |
| AC-05 | Projection at deploy/init; reuse; no per-turn disk rewrite | **PASS (code)** · **Info G-03** | `deployment.verify_and_register_deployment` stores `strict_tool`; `generate_strict_tool` only in `deployment.py` + `readiness.py` (not interview path); disk immutability tested; no turn-path regenerate instrumentation |
| AC-06 / fail-closed | Projection error / remaining keyword → `tool_gen_failed:*` | **PASS** | `assert_openai_projection_clean` → `ToolGenError`; deployment/readiness prefix `tool_gen_failed:` · `test_fail_closed_when_projection_leaves_keyword` |
| AC-07 | Deterministic bytes; input object unchanged | **PASS** | `test_deterministic_serialization` · `test_input_python_pack_unchanged_via_project` |
| Policy allow-list | Sole strip = `uniqueItems` | **PASS** | `OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS == frozenset({"uniqueItems"})` |
| Property named `uniqueItems` | Not stripped (AIB-COMPAT-02) | **PASS** | `test_project_preserves_property_named_unique_items` |
| Optional init event | Non-blocking for readiness | **PASS** | `_emit_projection_ready_event` swallows exceptions |
| AC-04 / AC-09 | Gate 2 / live TG | **Out of scope** | STORY-42 / STORY-45 |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| No pack JSON edit / `strict: false` | **PASS** | Tool `strict: True`; pack still has keyword |
| SPA / hasUxPipeline | false | |
| Live OpenAI accept (AC-03 wording) | **Not claimed** | Deferred STORY-45; local shape only |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Low** | Test helper `_keyword_in_schema_tree` in `tests/test_openai_schema_projection.py` special-cases only `properties`, not `$defs`/`definitions`. A `$defs` entry *named* `uniqueItems` makes the helper return True even when production `_PROPERTY_MAP_KEYS` walk + `assert_openai_projection_clean` are clean (verified ad-hoc). | Align helper with production (`_PROPERTY_MAP_KEYS`) or stop using helper as sole AC-03 oracle for `$defs`. |
| **G-02** | **Low** | REQ §11 **T-COMPAT-06** (preserve supported constraints) not named in t03 acceptance (lists 01…05/07/08). Suite does not assert e.g. `minItems` survives on projected houses; ad-hoc P4 probe: houses keeps `minItems: 1`, `uniqueItems` absent. | Add explicit T-COMPAT-06 assert on projected canonical houses (or document waive). |
| **G-03** | **Info** | AC-05 «ordinary turns do not reload/rewrite» proven by call-graph + disk tests; no test/instrumentation that InterviewEngine turn path skips `generate_strict_tool`. | Optional: assert generate not called from turn/engine path (spy) or cite call-sites in gate note. |
| **G-04** | **Info** | `aibridge-active-package.current.yaml` header still «P1.3 APPLY · next P2» though P3 closed 11:00:27Z. | Refresh pointer comment to P3 Done / audit phase. |

### Non-gaps

| Topic | Note |
|-------|------|
| Invent pack strip / Gate 2 uniqueItems / live TG / OpenAI network | Avoided |
| Silent `strict: false` fallback | Avoided — fail-closed `tool_gen_failed:` |
| Disk mutation of pack/OAS | Avoided — bytes equal after generate |
| SPA / hasUxPipeline | false |

### Regressions

| Topic | Note |
|-------|------|
| vs gate t04 (12 passed) | **None** — re-run **12 passed** @ 2026-09-24T11:02:40Z |
| Pack still has uniqueItems | **Confirmed** (`"uniqueItems": true` under houses) |

---

## Cited paths

- `src/aibridge/tool_gen.py` — `OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS`, `project_schema_for_openai`, `assert_openai_projection_clean`, `generate_strict_tool`, `_emit_projection_ready_event`
- `src/aibridge/deployment.py` — `DeploymentBundleState.strict_tool`
- `src/aibridge/readiness.py` — `_strict_tool_ok` / `tool_gen_failed:`
- `src/aibridge/app.py` — engine tools from deployment
- `tests/test_openai_schema_projection.py` · `tests/test_tool_gen.py`
- Pack: `src/instructions/schema-packs.uus_veerenni_civic.v3.payload.schema.json`
- OAS: `docs/openapi/story-intake-actions.openapi.yaml`
- Gate: `…/task-aibridge-41-t04-story-gate/acceptance-verification-….md`
- P3: `docs/tasks/run-reports/run-summary-20260924-1100-story-aibridge-41-p3.md`
- Pkg: `docs/tasks/aibridge-active-packages/pkg-000040-20260924-epic-aibridge-05-story-41-openai-schema-projection.yaml`

---

## Handoff

- **OPEN gaps:** 0 Critical · 0 Medium · **2 Low** · **2 Info**
- **OPEN IDs:** G-01, G-02, G-03, G-04
- **Product Story AC/DoD (core):** **PASS** (docs/test-hygiene residuals only)
- **next:** **P5** (disposition; do not implement in P4)
