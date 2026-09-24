# P4 Audit — STORY-AIBRIDGE-44-compat-merge-gate-proof

| Field | Value |
|-------|-------|
| **Date** | 2026-09-24T11:56:42Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-05-…/STORY-AIBRIDGE-44-compat-merge-gate-proof/STORY-AIBRIDGE-44-compat-merge-gate-proof.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-44-compat-merge-gate-proof.md` |
| **Method** | Read/Glob + live pytest `tests/test_req07_merge_gate.py` (7) + P3 regression filter (60) + fixture path; no product patches; no live TG/OpenAI invent |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway / live Telegram / live OpenAI** | **No** SUCCESS invent · focus status remains **implemented, live verification pending** (STORY-45) |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (TECH-ARCH §5.1 merge gate + AC-08)** | **PASS (core)** — §5.1 #1–#5 evidenced in `test_req07_merge_gate.py` |
| **Bullrun t01–t05 Done** | **Confirmed** vs suite + acceptance + gate PASS 2026-09-24T11:52:39Z |
| **OPEN gaps** | **0 Critical · 0 Medium · 3 Low · 1 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **7 passed** (merge-gate) · **60 passed** (P3 regression filter) @ 2026-09-24T11:56:42Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-44** | ✅ P3 Done · next P4 · implemented, live verification pending · pkg-000043 | **Confirmed** §5.1 suite · **this P4** → next **P5** · live still pending (45) |
| **t01** | Done — Responses tools / §11.4 | **Confirmed** RecordingResponsesClient · no `uniqueItems` · store/parallel false |
| **t02** | Done — pack unchanged | **Confirmed** disk bytes + in-memory snapshot |
| **t03** | Done — Gate 2 + fixture | **Confirmed** duplicate houses + `invalid_function_parameters_uniqueitems.json` |
| **t04** | Done — readyz VC / T-READY | **Confirmed** `validation_context_not_bound` · no OpenAI from `/readyz` · `schema_validation_complete` |
| **t05** | Done · PASS | **Confirmed** acceptance |
| **suite 7 / regression 60** | claimed | **Confirmed** this P4 |
| **Backlog Verified** | «T-COMPAT/T-UNIQUE not present» | **Stale** → **Low G-01** |
| **active-package.current comment** | «next P2» | **Stale** → **Info G-04** |

---

## AC matrix (`$storyFile` / pipeline · TECH-ARCH §5.1 · REQ §11)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| §5.1 #1 | `uniqueItems` absent from OpenAI-facing `tools` payload | **PASS** · **Low G-02** | `test_merge_gate_responses_tools_payload_no_uniqueitems` · keyword walk on `parameters`; soft `tool == outbound or params` |
| §5.1 #2 | Canonical pack unchanged by projection | **PASS** | disk bytes + deepcopy; houses `uniqueItems: true` retained |
| §5.1 #3 | Gate 2 rejects duplicate `houses` | **PASS** | `validate_gate2_pack_payload` on uus_veerenni pack |
| §5.1 #4 | Missing VC → `/readyz` not_ready | **PASS** | 503 `validation_context_not_bound` · OpenAI call count unchanged |
| §5.1 #5 | Regression fixture `invalid_function_parameters` | **PASS** | `tests/fixtures/openai/invalid_function_parameters_uniqueitems.json` + remediation prove |
| §11.4 | Responses-flat · `store:false` · `parallel_tool_calls:false` · name | **PASS** | payload asserts + `test_merge_gate_assemble_contract_knobs` |
| T-READY w/o OpenAI `/readyz` | Covered locally | **PASS (partial)** · **Low G-03** | VC + `schema_validation_complete`; T-READY-02/04 not named in suite |
| Focus status | **implemented, live verification pending** | **PASS** | Index / pipeline / bullrun · not invent AC-09 |
| Nested tasks Done | t01–t05 | **PASS** | README + acceptance |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| No live TG / live OpenAI as sole proof | **PASS** | Recording transport + fixtures only |
| SPA / hasUxPipeline | false | |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Low** | Backlog `$storyFile` «Verified current state» still says REQ-07 T-COMPAT / T-UNIQUE suite «not present at emit» while 41–44 suites exist post-P3. | Sync Verified to post-P3 merge-gate / sibling suite facts. |
| **G-02** | **Low** | `test_merge_gate_responses_tools_payload_no_uniqueitems` uses `assert tool == outbound or tool["parameters"] == outbound["parameters"]` — OR weakens full-object mutation proof (currently full equal ad-hoc). | Tighten to `tool == outbound` (or drop OR). |
| **G-03** | **Low** | Story AC «T-READY behaviors» — suite covers VC readyz + `schema_validation_complete` (T-READY-03-ish); REQ T-READY-02 (projector broken → projection reason) and T-READY-04 (restart hash stability) not named in merge-gate module. | Add/name remaining T-READY cases or document out-of-DoD for STORY-44 (merge §5.1 only). |
| **G-04** | **Info** | `aibridge-active-package.current.yaml` header still «P1.3 APPLY · next P2» though P3 closed 11:52:39Z. | Refresh pointer comment. |

### Non-gaps

| Topic | Note |
|-------|------|
| Invent live Telegram / live OpenAI SUCCESS (AC-09) | Avoided — deferred STORY-45 |
| Weakening pack / deleting uniqueItems from disk | Avoided |
| Silent claim production verified / Done for REQ-07 | Avoided — **implemented, live verification pending** |
| SPA / hasUxPipeline | false |

### Regressions

| Topic | Note |
|-------|------|
| vs gate t05 (7 + 60) | **None** — re-run **7** / **60** @ 2026-09-24T11:56:42Z |
| STORY-41/42/43 suites in filter | Still green |

---

## Cited paths

- `tests/test_req07_merge_gate.py`
- `tests/fixtures/openai/invalid_function_parameters_uniqueitems.json`
- `src/instructions/schema-packs.uus_veerenni_civic.v3.payload.schema.json`
- `src/aibridge/tool_gen.py` · `request_assembly.py` · `app.py` · `responses_client.py`
- TECH-ARCH: `docs/architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md` §5.1
- Gate: `…/task-aibridge-44-t05-story-gate/acceptance-verification-….md`
- P3: `docs/tasks/run-reports/run-summary-20260924-1152-story-aibridge-44-p3.md`
- Pkg: `docs/tasks/aibridge-active-packages/pkg-000043-20260924-epic-aibridge-05-story-44-compat-merge-gate-proof.yaml`

---

## Handoff

- **OPEN gaps:** 0 Critical · 0 Medium · **3 Low** · **1 Info**
- **OPEN IDs:** G-01, G-02, G-03, G-04
- **Product Story AC/DoD (merge gate):** **PASS** (live verify = STORY-45)
- **next:** **P5** (disposition; do not implement in P4)
