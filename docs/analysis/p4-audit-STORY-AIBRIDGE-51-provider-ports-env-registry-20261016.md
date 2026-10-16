# P4 Audit — STORY-AIBRIDGE-51-provider-ports-env-registry

| Field | Value |
|-------|-------|
| **Date** | 2026-10-16T10:53:17Z |
| **Mode** | `input_mode=backlog_story` / epic_story pipeline |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/run-reports/run-summary-20261016-1049-story-aibridge-51-p3.md` |
| **$story** | `…/STORY-AIBRIDGE-51-provider-ports-env-registry/STORY-AIBRIDGE-51-provider-ports-env-registry.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-51-provider-ports-env-registry.md` |
| **Method** | Read `providers/` + config/readiness/app middleware + tests; live pytest 46–51; no product patches; no invent accept-wire (52) / live OpenAI (54) |
| **Thinking** | `.cursor/rules/analysis.mdc` · aibridge-operator-contract §6 · workflow §P4 |
| **Scope** | Worker text/image provider ports · env registry · unset→mock · nest · unknown fail-closed |
| **Out of scope** | Mock accept wire (52) · allow-mock (53) · live OpenAI text (54) · docs/verify (55) |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (AC-10-01 · AC-10-02 · AC-10-05 · unset→mock · nest)** | **PASS** |
| **Bullrun t01–t08 Done** | **Confirmed** vs code + gate + **55 passed** |
| **OPEN gaps** | **0 Crit · 0 High · 0 Med · 1 Low · 2 Info** |
| **Critical / High OPEN** | **0** |
| **Live pytest** | **55 passed** (`test_provider_ports_story_51` + 46–50) @ 2026-10-16T10:53:17Z |

---

## Bullrun touchpoints (актуализация `$bullrun`)

| ID | P3 claim | P4 fact |
|----|----------|---------|
| **STORY-51** | P3 Done · t08 PASS · next P4 | **Confirmed** · **this P4** → next **P5** |
| **t01** | Done · selector env | **Confirmed** `AIBRIDGE_WORKER_*_PROVIDER` · nest fail-closed |
| **t02** | Done · registry skeleton | **Confirmed** `src/aibridge/providers/` |
| **t03** | Done · AC-10-01 | **Confirmed** `resolve_text_brief_provider` |
| **t04** | Done · AC-10-02 | **Confirmed** independent registry resolve |
| **t05** | Done · model nest openai-only | **Confirmed** mock+empty model readyz 200; openai+empty 503 |
| **t06** | Done · AC-10-05 | **Confirmed** unknown → `worker_provider_unknown` |
| **t07** | Done · registry tests | **Confirmed** this P4 **55 passed** |
| **t08** | PASS · gate | **Confirmed** |
| **`.env.example`** | — | **Missing provider knobs** → **Low G-01** |

---

## AC matrix (pipeline / `$storyFile` · arch 01–02 · REQ-10)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| **AC-10-01** | Text slot via selectable port | **PASS** · **Info G-02** | `TextBriefProviderPort` · Mock/OpenAI resolve · ports doc: accept wire = 52 |
| **AC-10-02** | Image slot independent | **PASS** | registry text≠image combinations · `test_ac_10_02_*` |
| **AC-10-05** | Unknown/incomplete fail-closed; no silent OpenAI | **PASS** | `anthropic` → 503 `worker_provider_unknown` · `normalize_provider_id` raises · nest via model fail-closed |
| **Unset → mock** | Blank/unset defaults mock | **PASS** | Field default + normalize blank → `ProviderId.MOCK` |
| **Model nest** | Model required only if provider=`openai` | **PASS** | `worker_*_fail_closed` gated on openai |
| **L10-1 channel** | Channel registry unchanged | **PASS** | `test_channel_auth_unchanged_*` · no channel wiring edits |
| Nested t01–t08 | Done / PASS | **PASS** | README + **55 passed** |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| Reason `worker_provider_unknown` | **PASS** | middleware + readyz |
| Sibling 47/48 nest tests | **PASS** | set `*_PROVIDER=openai` for model-empty cases |
| Accept-pipe mock wire | **OOS** · **Info G-02** | accept still `generate_sense_brief` direct |
| Live OpenAI invoke | **OOS** · **Info G-03** | `OpenAI*Provider` → `NotImplementedError` |
| Anthropic/Gemini | **PASS** | not registered; unknown fail-closed |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Low** | `.env.example` documents model/storage worker knobs but **omits** `AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER` / `AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER` while `config.py` Present. | Add selector lines (+ unset→mock note) to `.env.example`. |
| **G-02** | **Info** | Accept handler still calls `generate_sense_brief` / poster pipeline **directly** — does not invoke `resolve_*_provider` (ports.py / adapters explicitly defer wire to STORY-52). Registry resolve AC met in unit tests. | STORY-52 accept wire; not this story AC. |
| **G-03** | **Info** | `OpenAITextBriefProvider` / `OpenAIImagePosterProvider` resolve but raise `NotImplementedError` on invoke (54 / live image deferred). `INCOMPLETE_PROVIDER_CONFIG` enum unused (nest uses middleware reasons instead). | STORY-54 + optional enum hygiene; residual only. |

### Non-gaps

| Topic | Note |
|-------|------|
| Silent OpenAI fallback on unknown id | Avoided — raise / 503 |
| Softening nest for openai empty model | Avoided |
| Altering channel Responses wiring | Avoided |
| Inventing Anthropic/Gemini | Avoided |

### Regressions

| Topic | Note |
|-------|------|
| vs P3 gate (55 passed) | **None** — re-run **55 passed** |
| STORY-46–50 suites | Preserved (47/48 nest env updated) |

---

## Cited paths

- `src/aibridge/providers/` (`ids.py` · `ports.py` · `registry.py` · `adapters.py` · `errors.py`)
- `src/aibridge/config.py` · `readiness.py` · `app.py` (middleware)
- `tests/test_provider_ports_story_51.py`
- `.env.example` (G-01)
- Pipeline / tasks under `…/STORY-AIBRIDGE-51-provider-ports-env-registry/`
- P3: `docs/tasks/run-reports/run-summary-20261016-1049-story-aibridge-51-p3.md`
- Arch: `docs/architecture/ai-provider-selection/01-provider-ports.md` · `02-readyz-env-fail-closed.md`

---

## Handoff

- **OPEN gaps:** 0 Crit · 0 High · 0 Med · **1 Low** · **2 Info**
- **OPEN IDs:** G-01, G-02, G-03
- **AC vs story:** **PASS**
- **next:** **P5**
