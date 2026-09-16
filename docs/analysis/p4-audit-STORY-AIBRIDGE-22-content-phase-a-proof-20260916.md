# P4 Audit — STORY-AIBRIDGE-22-content-phase-a-proof

| Field | Value |
|-------|-------|
| **Date** | 2026-09-16T13:44:09Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-03-…/STORY-AIBRIDGE-22-content-phase-a-proof/STORY-AIBRIDGE-22-content-phase-a-proof.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-22-content-phase-a-proof.md` |
| **Method** | Read/Glob + live pytest story-22; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway** | **No** live Railway SUCCESS invented or claimed |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (REQ-05 §4.5 / R5-A-05 · §4.6)** | **PASS** — automated proof tests + smoke checklist file; Phase B not required |
| **Bullrun t01–t05 Done** | **Confirmed** vs tests + ops file + gate PASS 2026-09-16T13:41:13Z |
| **OPEN gaps** | **1 Medium · 0 Low · 1 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **6 passed** (`tests/test_story_22_phase_a_proof.py`) @ 2026-09-16T13:44Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-22** | 🟢 Implemented (P3 · next P4) · pkg-000019 | **Confirmed** ADR-4; gate PASS; **this P4** → next **P5** |
| **t01** | Done — engine wired + prefix | **Confirmed** `test_full_dump_create_app_wires_nonempty_prefix_instructions` |
| **t02** | Done — readyz fail-closed | **Confirmed** missing dir + broken OAS → `/readyz` 503 |
| **t03** | Done — completeness | **Confirmed** `test_proof_completeness_dir_set_equals_files_set` |
| **t04** | Done — smoke checklist | **Confirmed** `docs/ops/req-05-phase-a-smoke.md` present; checkboxes **unchecked** (ops residual → **G-02**) |
| **t05** | Done — story gate PASS | **Confirmed** `acceptance-verification-…t05…md` · no Railway SUCCESS |
| **pkg-000019** | Active (story 22 P3 · next P4) | `--verify` **ok 5 paths** |
| **Depends 19–21** | Done | Satisfied (siblings Done this wave) |

---

## AC matrix (`$storyFile` Target · REQ-05 §4.5 / §4.6)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | §4.5 automated: content_configured + full dump → non-empty prefix / XOR | **PASS** | `create_app` + full `src/instructions` → `prompt_channel=="prefix"` · non-empty `instructions` · system prefix in `run_turn`; `"instructions" not in` payload |
| 2 | §4.5 missing/broken → fail-closed (no silent empty) | **PASS** | missing instructions dir / broken OAS → `deployment.ready is False` · engine `instructions==""` · `/readyz` 503 · `/healthz` 200 |
| 3 | §4.5 completeness dir vs `files[]` | **PASS (CI)** | set equality + omit inequality tests (same pattern as STORY-20) |
| 4 | §4.5 smoke checklist at `docs/ops/req-05-phase-a-smoke.md` | **PASS (artifact)** · **PARTIAL (ops executed)** | File exists; healthz/readyz/content wording present; checklist `[ ]` not filled; **no** Railway SUCCESS — correct |
| 5 | §4.6 Phase B not required | **PASS** | Explicit in smoke §Explicit non-claims + gate |

### Scope extras

| Item | Status | Evidence |
|------|--------|----------|
| ASGI readyz content reason absent on happy path | **PASS** | `test_full_dump_readyz_not_content_bundle_not_ready` |
| Live Railway SUCCESS | **Not claimed** | Gate + smoke explicit non-claims |
| Assembled covers all §4.2 basenames in text | **Soft** | Hashes include `root.md`/pack payload; full text length large; no per-basename substring matrix — acceptable under «при необходимости» |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | `_full_dump_settings` in `tests/test_story_22_phase_a_proof.py` sets dead `DOGESTONIA_API_BASE_URL=…` (alias **removed** in `config.py`). Settings still load `env_file=".env"`, so local/CI hermeticity depends on ambient `DOGESTONIA_INTAKE_BASE_URL`. With `_env_file=None` and no INTAKE kwarg, intake is `""` / `intake_base_url_https_ok() False`. Same dead alias pattern in `test_story_19_engine_wire.py`. Proof tests can pass while not pinning intake in-code. | Pass `DOGESTONIA_INTAKE_BASE_URL=https://gateway.example.invalid` (and prefer `_env_file=None` / isolate ambient `.env`) in story-22 (and sibling) settings helpers; assert hermetic readyz without relying on local `.env`. |
| **G-02** | **Info** | Ops smoke checklist items remain `[ ]` unchecked — artifact DoD met; **live** local/Railway observation not recorded. Correctly forbids inventing Railway SUCCESS. | Ops fill checklist with observed results when executed; or WAIVE as docs-only residual until operator smoke. |

### Non-gaps

| Topic | Note |
|-------|------|
| Inventing Railway SUCCESS | Avoided in gate + smoke |
| Loader runtime completeness fail-closed | Out of STORY-22 DoD (STORY-20 WAIVED → STORY-22 optional); CI assert present |
| Phase B / n8n / Telegram | Explicitly out of Phase A Done |
| Depends 19–21 | Done |

---

## Cited paths

- `tests/test_story_22_phase_a_proof.py`
- `docs/ops/req-05-phase-a-smoke.md`
- `src/aibridge/app.py`, `readiness.py`, `interview.py`, `content.py`, `config.py` (INTAKE alias; no API_BASE)
- Gate: `acceptance-verification-task-aibridge-22-t05-story-gate.md`
- REQ-05 §4.5 · §4.6 · R5-A-05 · TECH ADR-4

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Info)
- **Critical:** 0
- **OPEN counts:** Critical **0** · Medium **1** · Low **0** · Info **1**
- **next:** **P5** disposition
