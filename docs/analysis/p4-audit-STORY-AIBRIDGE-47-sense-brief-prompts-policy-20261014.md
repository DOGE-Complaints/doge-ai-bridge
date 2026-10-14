# P4 Audit — STORY-AIBRIDGE-47-sense-brief-prompts-policy

| Field | Value |
|-------|-------|
| **Date** | 2026-10-14T13:23:18Z |
| **Mode** | `input_mode=backlog_story` / epic_story pipeline |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/run-reports/run-summary-20261014-1314-story-aibridge-47-p3.md` |
| **$story** | `…/STORY-AIBRIDGE-47-sense-brief-prompts-policy/STORY-AIBRIDGE-47-sense-brief-prompts-policy.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-47-sense-brief-prompts-policy.md` |
| **Method** | Read `sense_brief/` + config/app/readiness + fixtures; live pytest 47+46; no product patches; no invent poster/bind/LLM SSOT |
| **Thinking** | `.cursor/rules/analysis.mdc` · aibridge-operator-contract §6 · workflow §P4 |
| **Scope** | L2 brief · dedicated EN prompts · text-brief slot fail-closed · no-invent · fail classes |
| **Out of scope** | Poster/storage (48) · gateway bind (49) · harness (50) · live OpenAI as CI gate |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (AC-09-02 · AC-09-05 · prompts · text-brief fail-closed)** | **PASS** |
| **Bullrun t01–t07 Done** | **Confirmed** vs code + gate + **20 passed** |
| **OPEN gaps** | **0 Crit · 0 High · 0 Med · 1 Low · 2 Info** |
| **Critical / High OPEN** | **0** |
| **Live pytest** | **20 passed** (`test_sense_brief_story_47` + `test_worker_accept_story_46`) @ 2026-10-14T13:23:18Z |

---

## Bullrun touchpoints (актуализация `$bullrun`)

| ID | P3 claim | P4 fact |
|----|----------|---------|
| **STORY-47** | P3 Done · gate PASS · next P4 | **Confirmed** · **this P4** → next **P5** |
| **t01** | Done · L2 model | **Confirmed** `sense_brief/model.py` · `satisfies_l2` · title max_length=80 |
| **t02** | Done · `prompts/system_en.md` | **Confirmed** load + `assert_not_interview_ssot` |
| **t03** | Done · `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` fail-closed | **Confirmed** middleware 503 `worker_text_brief_missing` · readyz |
| **t04** | Done · corpus + no-invent | **Confirmed** `pipeline.generate_sense_brief` · invent-refusal helper + fixtures |
| **t05** | Done · fail classes | **Confirmed** `corpus_insufficient` / `brief_generation_failed` · accept 422 |
| **t06** | Done · golden + invent fixtures | **Confirmed** `tests/fixtures/sense_brief_*.json` · 9 tests in 47 |
| **t07** | PASS · story gate | **Confirmed** acceptance |
| **Backlog Code points** | module path **Open** | **Stale** → **Low G-01** (Verified already Present) |

---

## AC matrix (pipeline / `$storyFile` · arch 02 · REQ-09)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| **AC-09-02** | title ≤80 + summary et/ru/en | **PASS** | `SenseBrief` / `SenseBriefSummary` · `test_t01_golden_l2_*` · accept `brief_ready` |
| **AC-09-05** | EN instructions; no invented civic facts beyond corpus | **PASS** · **Info G-03** | `system_en.md` «Do not invent…» · insufficient → `corpus_insufficient` · `refuse_invented_civic_facts` fixture |
| **Dedicated prompts** | Not interview/content SSOT | **PASS** | `sense_brief/prompts/` · markers forbid InterviewEngine · accept ≠ `InterviewEngine` |
| **text-brief fail-closed** | Unset + worker enabled → no invent brief | **PASS** | `worker_text_brief_fail_closed` · accept/readyz 503 `worker_text_brief_missing` |
| Nested t01–t07 | Done / PASS | **PASS** | README + acceptance + **20 passed** |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| Fail classes surfaced | **PASS** | accept 422 `corpus_insufficient`; enum has `brief_generation_failed` |
| PII-safe logging | **PASS** | `log_brief_job` ids only · `test_t06_pii_safe_*` |
| No entry via InterviewEngine | **PASS** | worker route calls `generate_sense_brief` only |
| No live vendor required in CI | **PASS** · **Info G-02** | corpus-grounded v1; model slot checked, not invoked |
| Poster/bind not invented | **PASS** | out of module scope |
| `.env.example` knob | **PASS** | `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL=` |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Low** | Backlog `$storyFile` «Code points» still claims «New worker brief module path — **Open** (name≠create until implement)» while Verified + P3 shipped `src/aibridge/sense_brief/`. | Sync Code points to Present / remove stale Open line. |
| **G-02** | **Info** | `generate_sense_brief` is **corpus-grounded extraction** only — `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` is required (fail-closed) but **not** used for a live LLM call (documented in `pipeline.py`). AC fixtures OK without live vendor. | Later wave may bind model invoke; not required for this story AC. |
| **G-03** | **Info** | `invent_forbidden` loop inside `generate_sense_brief` is effectively a no-op; `refuse_invented_civic_facts` is fixture/helper-only (not called on accept). L2 model has no address/agency fields, so current path cannot invent them into the brief. | Optional wire helper into future LLM path; residual only. |

### Non-gaps

| Topic | Note |
|-------|------|
| Using interview templates as civic SSOT | Avoided — dedicated `system_en.md` + assert |
| Softening text-brief fail-closed | Avoided — middleware before handler |
| Inventing poster/storage/bind | Avoided |
| Locking model id / JSON keys as cross-repo SSOT | Avoided — implement choice documented |

### Regressions

| Topic | Note |
|-------|------|
| vs P3 gate (20 passed) | **None** — re-run **20 passed** |
| STORY-46 accept suite | Untouched behavior preserved (11) |

---

## Cited paths

- `src/aibridge/sense_brief/model.py`
- `src/aibridge/sense_brief/pipeline.py`
- `src/aibridge/sense_brief/prompts.py` · `prompts/system_en.md`
- `src/aibridge/sense_brief/errors.py` · `logging_safe.py`
- `src/aibridge/config.py` · `readiness.py` · `app.py` (`worker_sense_brief_accept`)
- `tests/test_sense_brief_story_47.py` · `tests/fixtures/sense_brief_*.json`
- `tests/test_worker_accept_story_46.py`
- `.env.example`
- Pipeline / tasks under `…/STORY-AIBRIDGE-47-sense-brief-prompts-policy/`
- P3: `docs/tasks/run-reports/run-summary-20261014-1314-story-aibridge-47-p3.md`
- Arch: `docs/architecture/sense-brief-poster-worker/02-brief-poster-pipeline.md`

---

## Handoff

- **OPEN gaps:** 0 Crit · 0 High · 0 Med · **1 Low** · **2 Info**
- **OPEN IDs:** G-01, G-02, G-03
- **AC vs story:** **PASS**
- **next:** **P5**
