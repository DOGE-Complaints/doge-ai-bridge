# P4 Audit — STORY-AIBRIDGE-53-readyz-allow-mock-refuse

| Field | Value |
|-------|-------|
| **Date** | 2026-10-16T11:26:35Z |
| **Mode** | `input_mode=backlog_story` / epic_story pipeline |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/run-reports/run-summary-20261016-1123-story-aibridge-53-p3.md` |
| **$story** | `…/STORY-AIBRIDGE-53-readyz-allow-mock-refuse/STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md` |
| **Method** | Read config/readiness/app middleware + tests + `.env.example`; live pytest story-53 + 50–52; no product patches; no invent live OpenAI (54) |
| **Thinking** | `.cursor/rules/analysis.mdc` · aibridge-operator-contract §6 · workflow §P4 |
| **Scope** | `AIBRIDGE_ALLOW_MOCK_PROVIDERS` · refuse mock at readyz+accept · slot-gated OpenAI presence |
| **Out of scope** | Channel registry · live OpenAI text (54) · docs/verify (55) |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (AC-10-08 · AC-10-09 · nested Done)** | **PASS** |
| **Bullrun t01–t08 Done** | **Confirmed** vs code + gate + focused **27 passed** |
| **OPEN gaps** | **0 Crit · 0 High · 0 Med · 0 Low · 2 Info** |
| **Critical / High OPEN** | **0** |
| **Live pytest** | **27 passed** (`test_readyz_allow_mock_story_53` + 50–52) @ 2026-10-16T11:26:35Z · P3 claimed full suite 559 (not re-run whole tree this P4) |

---

## Bullrun touchpoints (актуализация `$bullrun`)

| ID | P3 claim | P4 fact |
|----|----------|---------|
| **STORY-53** | P3 Done · t08 PASS · next P4 | **Confirmed** · **this P4** → next **P5** |
| **t01** | Done · allow-mock env | **Confirmed** `AIBRIDGE_ALLOW_MOCK_PROVIDERS` · `.env.example` |
| **t02** | Done · slot-gated presence | **Confirmed** `worker_openai_presence_required` |
| **t03** | Done · AC-10-08 | **Confirmed** mock+mock `/readyz` 200 w/o key |
| **t04** | Done · AC-10-09 readyz | **Confirmed** `worker_mock_not_allowed` |
| **t05** | Done · AC-10-09 accept | **Confirmed** accept 503 same code |
| **t06** | Done · reason string | **Confirmed** wire `worker_mock_not_allowed` |
| **t07** | Done · tests | **Confirmed** this P4 focused green |
| **t08** | PASS · gate | **Confirmed** |

---

## AC matrix (pipeline / `$storyFile` · arch 02 · REQ-10)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| **AC-10-08** | mock+mock → `/ready` without `OPENAI_API_KEY` (worker gate) | **PASS** · **Info G-01** | `worker_openai_presence_required()==False` · `evaluate_readiness` ready · `/readyz` 200 |
| **AC-10-09** | Refuse mock unless explicit allow (readyz + accept) | **PASS** | allow=false → readyz 503 + accept 503 `worker_mock_not_allowed` |
| **Slot-gated OpenAI** | Any worker openai slot → key still required | **PASS** | text=openai empty key → `openai_config_missing` |
| **Both openai** | No mock → allow flag irrelevant | **PASS** | `test_both_openai_slots_skip_allow_mock_gate` |
| **Worker off** | Channel presence still required | **PASS** | `test_channel_readyz_still_requires_openai_when_worker_off` |
| Nested t01–t08 | Done / PASS | **PASS** | README + tests |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| Middleware before compute | **PASS** | `worker_s2s_middleware` after unknown, before model nest |
| `.env.example` knob | **PASS** | `AIBRIDGE_ALLOW_MOCK_PROVIDERS=false` + comment |
| Sibling worker tests allow=true | **PASS** | 46–52 helpers updated |
| Channel registry unchanged | **PASS** | L10-1 |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Info** | AC-10-08 is a **worker gate**: mock+mock + allow can make `/readyz` ready with empty `OPENAI_API_KEY`. Channel `InterviewEngine` turns may still need OpenAI at runtime — not contradicted by story AC («worker gate»). | Ops/docs residual; optional channel-gate note in 55. |
| **G-02** | **Info** | Config Field defaults for providers remain `mock`; without `AIBRIDGE_ALLOW_MOCK_PROVIDERS` production fail-closes (by design). Ops must set allow **or** switch slots to `openai`. | Documented in `.env.example`; residual only. |

### Non-gaps

| Topic | Note |
|-------|------|
| Softening refuse when allow false | Avoided — readyz + accept |
| Silent OpenAI skip when any openai slot | Avoided — presence still required |
| Inventing live OpenAI text (54) | Avoided |
| Changing channel bearer registry | Avoided |

### Regressions

| Topic | Note |
|-------|------|
| vs P3 focused story tests | **None** — story-53 + 50–52 **27 passed** |
| Sibling accept suites | Preserved via `ALLOW_MOCK=true` in helpers |

---

## Cited paths

- `src/aibridge/config.py` (`allow_mock_providers` · `worker_mock_not_allowed_fail_closed` · `worker_openai_presence_required`)
- `src/aibridge/readiness.py`
- `src/aibridge/app.py` (worker middleware)
- `.env.example`
- `tests/test_readyz_allow_mock_story_53.py`
- Pipeline / tasks under `…/STORY-AIBRIDGE-53-readyz-allow-mock-refuse/`
- P3: `docs/tasks/run-reports/run-summary-20261016-1123-story-aibridge-53-p3.md`
- Arch: `docs/architecture/ai-provider-selection/02-readyz-env-fail-closed.md`

---

## Handoff

- **OPEN gaps:** 0 Crit · 0 High · 0 Med · **0 Low** · **2 Info**
- **OPEN IDs:** G-01, G-02
- **AC vs story:** **PASS**
- **next:** **P5**
