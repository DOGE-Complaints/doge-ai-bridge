# P4 Audit — STORY-AIBRIDGE-42-canonical-uniqueitems-validation

| Field | Value |
|-------|-------|
| **Date** | 2026-09-24T11:19:30Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-05-…/STORY-AIBRIDGE-42-canonical-uniqueitems-validation/STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md` |
| **Method** | Read/Glob + live pytest `tests/test_uniqueitems_gate2.py` + `tests/test_request_assembly.py` (16) + `request_assembly.py` / coordinator / readiness / app bind check; pack disk `uniqueItems`; no product patches; no live TG invent |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway / live Telegram** | **No** Railway SUCCESS · **No** live Telegram PASS invented |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (Gate 2 uniqueItems + readiness prove)** | **PASS (core)** — `FULL_SCHEMA_KEYWORDS` + `_assert_unique_items` (structural) + `schema_validation_complete` behavioral prove; T-UNIQUE-01…09 green |
| **Bullrun t01–t04 Done** | **Confirmed** vs code + acceptance + gate PASS 2026-09-24T11:17:36Z |
| **OPEN gaps** | **0 Critical · 0 Medium · 2 Low · 2 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **16 passed** (`test_uniqueitems_gate2.py` + `test_request_assembly.py`) @ 2026-09-24T11:19:30Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-42** | ✅ P3 Done · next P4 · pkg-000041 | **Confirmed** Gate 2 uniqueItems + 16 tests · **this P4** → next **P5** |
| **t01** | Done — Gate 2 enforce | **Confirmed** `uniqueItems` in keywords · `_assert_unique_items` via `_canonical_json_value` |
| **t02** | Done — readiness prove | **Confirmed** `schema_validation_complete()` uniqueItems probe · readiness uses it |
| **t03** | Done — T-UNIQUE · 16 passed | **Confirmed** **16 passed** this P4 |
| **t04** | Done · PASS | **Confirmed** acceptance gate |
| **pkg-000041** | Active · 4 paths | YAML under `aibridge-active-packages/` |
| **AC-04 freeze/Send** | claimed with Gate 2 | **Unit Gate 2 only** · VC bind absent (`app.py`) → **Low G-01** |
| **active-package.current comment** | «next P2» | **Stale** after P3 → **Info G-04** |

---

## AC matrix (`$storyFile` / pipeline · REQ-07 · TECH-ARCH §2.3)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| AC-04 Gate 2 reject | Duplicate houses under one street → Gate 2 error | **PASS** | `test_t_unique_08_…` · live path `gate2: uniqueItems at $.geo.streets[0].houses[1]` |
| AC-04 no freeze/Send/gateway | Stop before freeze/Send/write | **PARTIAL → G-01** | Unit `validate_gate2_pack_payload` only; `validate_function_calls` needs `ValidationContext`; `app.py` has **no** VC bind (STORY-43 OOS) |
| T-UNIQUE-01…09 | Behaviors covered | **PASS** | Dedicated tests in `test_uniqueitems_gate2.py` |
| Structural equality | Key-order independent | **PASS** | `_canonical_json_value` sort_keys · T-UNIQUE-03 |
| `uniqueItems:false` / absent | No uniqueness restriction | **PASS** | T-UNIQUE-05/06 |
| Pack untouched | Disk retains keyword | **PASS** | `test_pack_disk_still_has_uniqueitems` |
| Readiness prove | Not frozenset alone; fail-closed incomplete | **PASS (probe)** · **Low G-02** | `schema_validation_complete` rejects dup probe; readiness → `schema_validation_incomplete`; **no** negative test that broken uniqueItems → False |
| Gate 2 uses canonical pack | Not OpenAI projection | **PASS** | `validate_gate2_pack_payload(payload, pack_schema)` · Uus Veerenni pack JSON |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| OpenAI projection / VC bind / live TG | **Out of scope** | STORY-41 / 43 / 45 |
| `run_three_gates` includes Gate 2 | **PASS (API)** | `request_assembly.run_three_gates` → `validate_gate2_pack_payload` |
| SPA / hasUxPipeline | false | |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Low** | AC-04 wording «no freeze / Send / gateway write» is evidenced only at Gate 2 unit/contract (`validate_gate2_pack_payload`). Coordinator runs `run_three_gates` only when `ValidationContext` is present; `src/aibridge/app.py` has **no** VC bind (owned by STORY-43). Without bind, FC path fails «schemas not configured» before Gate 2 uniqueItems. | Keep residual until STORY-43 bind + optional FC-level duplicate-houses test; or soften story AC wording to unit Gate 2 only (docs). |
| **G-02** | **Low** | Incomplete-uniqueness fail-closed is implemented in `schema_validation_complete()` (dup → False) and readiness maps to `schema_validation_incomplete`, but suite only asserts `schema_validation_complete() is True` — no negative prove (monkeypatch / broken enforce → False / readiness reason). | Add negative test for probe False + readiness reason when uniqueItems capability broken. |
| **G-03** | **Info** | T-UNIQUE-02 «correct path» — Uus Veerenni error path verified ad-hoc (`$.geo.streets[0].houses[1]`) but tests match only `gate2:.*uniqueItems`, not full path. | Optionally assert full path string in T-UNIQUE-08/02. |
| **G-04** | **Info** | `aibridge-active-package.current.yaml` header still «P1.3 APPLY · next P2» though P3 closed 11:17:36Z. | Refresh pointer comment. |

### Non-gaps

| Topic | Note |
|-------|------|
| Invent pack delete uniqueItems / OpenAI projection / live TG | Avoided |
| Trusting model prompt alone for duplicates | Avoided — validator enforce |
| Silent skip of `uniqueItems: true` | Avoided — keyword in FULL_SCHEMA_KEYWORDS + behavioral probe |
| SPA / hasUxPipeline | false |

### Regressions

| Topic | Note |
|-------|------|
| vs gate t04 (16 passed) | **None** — re-run **16 passed** @ 2026-09-24T11:19:30Z |
| Pack still has uniqueItems | **Confirmed** |

---

## Cited paths

- `src/aibridge/request_assembly.py` — `FULL_SCHEMA_KEYWORDS`, `_assert_unique_items`, `_canonical_json_value`, `validate_gate2_pack_payload`, `schema_validation_complete`, `run_three_gates`
- `src/aibridge/coordinator.py` — `validate_function_calls` + `ValidationContext` gate
- `src/aibridge/readiness.py` — `schema_validation_incomplete`
- `src/aibridge/app.py` — **no** VC bind (STORY-43)
- `tests/test_uniqueitems_gate2.py` · `tests/test_request_assembly.py`
- Pack: `src/instructions/schema-packs.uus_veerenni_civic.v3.payload.schema.json`
- Gate: `…/task-aibridge-42-t04-story-gate/acceptance-verification-….md`
- P3: `docs/tasks/run-reports/run-summary-20260924-1117-story-aibridge-42-p3.md`
- Pkg: `docs/tasks/aibridge-active-packages/pkg-000041-20260924-epic-aibridge-05-story-42-canonical-uniqueitems-validation.yaml`

---

## Handoff

- **OPEN gaps:** 0 Critical · 0 Medium · **2 Low** · **2 Info**
- **OPEN IDs:** G-01, G-02, G-03, G-04
- **Product Story AC/DoD (core Gate 2 + prove):** **PASS** (residuals: VC path honesty + negative readiness test)
- **next:** **P5** (disposition; do not implement in P4)
