# P4 Audit — STORY-AIBRIDGE-21-oas-image-env-docs

| Field | Value |
|-------|-------|
| **Date** | 2026-09-16T12:58:58Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-03-…/STORY-AIBRIDGE-21-oas-image-env-docs/STORY-AIBRIDGE-21-oas-image-env-docs.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-21-oas-image-env-docs.md` |
| **Method** | Read/Glob + live pytest story-21; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (REQ-05 §4.3–4.4 / R5-A-03 · R5-A-04)** | **PASS** — Dockerfile `COPY docs/openapi` · Phase A pins · Story Intake OPENAPI_PATH · channel not in `files[]` |
| **Bullrun t01–t05 Done** | **Confirmed** vs artifacts + gate PASS 2026-09-16T12:55:52Z |
| **OPEN gaps** | **0 Medium · 0 Low · 2 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **3 passed** (`tests/test_story_21_oas_path_contract.py`) @ 2026-09-16T12:58Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-21** | 🟢 Implemented (P3 · next P4) · pkg-000018 | **Confirmed** ADR-3; gate PASS; **this P4** → next **P5** |
| **t01** | Done — Dockerfile COPY openapi | **Confirmed** `Dockerfile:13` `COPY docs/openapi ./docs/openapi`; both YAML on disk |
| **t02** | Done — `.env.example` Phase A | **Confirmed** §8 pins · local + `/app` comments · SCHEMA_ID/VERSION |
| **t03** | Done — web runbook pins | **Confirmed** `aibridge-web-service-local-railway.md` §1.1b |
| **t04** | Done — path contract | **Confirmed** `tests/test_story_21_oas_path_contract.py` |
| **t05** | Done — story gate PASS | **Confirmed** `acceptance-verification-…t05…md` + pytest 3 passed |
| **pkg-000018** | Active (story 21 P3 · next P4) | `--verify` **ok 5 paths** |
| **Siblings 19–20** | Done / Implemented | Not re-audited |
| **STORY-22** | Todo | Out of scope |

---

## AC matrix (`$storyFile` Target · REQ-05 §4.3–4.4)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | §4.4: openapi dir in image; OPENAPI_PATH = Story Intake | **PASS (Dockerfile + repo)** · **PARTIAL (live image)** | `COPY docs/openapi ./docs/openapi`; host has `story-intake-actions.openapi.yaml` + `aibridge-channel-v1.openapi.yaml`; `.env.example` OPENAPI_PATH = Story Intake. **No** `docker build`/`ls` evidence this pass → **G-01** |
| 2 | §4.3: documented Phase A pins (incl. SCHEMA_ID/VERSION) | **PASS** | `.env.example` + runbook §1.1b local/`/app`; `uus_veerenni_civic` / `v3` |
| Channel not in instruction `files[]` | **PASS** | `test_channel_oas_not_in_instruction_manifest_files` |
| Channel YAML rides in openapi dir | **PASS** | Both files under `docs/openapi/`; `.dockerignore` does **not** exclude `docs/openapi` |

### Scope extras

| Item | Status | Evidence |
|------|--------|----------|
| ADR-3: OAS not under `src/instructions/` | **PASS** | Paths stay `docs/openapi/` |
| No new env aliases | **PASS** | Existing `DOGESTONIA_*` names |
| Railpack redesign | **Out of scope** | Explicit; residual note **G-02** |
| Multi-repo CI / secrets invent | **Out of scope** | |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Info** | «Image contains `docs/openapi/`» verified by Dockerfile COPY line + host files + unit test string assert — **not** by building/running an image and listing `/app/docs/openapi/`. | Optional STORY-22 / ops smoke: `docker build` + assert both YAML under `/app/docs/openapi`; or WAIVE as docs/Dockerfile-sufficient DoD. |
| **G-02** | **Info** | Runbook still offers **Railpack** alternative without Dockerfile (`aibridge-web-service-local-railway.md`). `railpack.json` has startCommand only — **no** OAS packaging guarantee. Story OOS «Railpack spaceship»; recommended path is Dockerfile. Risk if deploy uses Railpack alone. | Prefer Dockerfile builder in ops; or document Railpack must still ship `docs/openapi` (later ops note / STORY-22); do not invent Railpack redesign under STORY-21. |

### Non-gaps

| Topic | Note |
|-------|------|
| `.env.example` CONTENT_SOURCE_COMMIT empty | Operator pin placeholder — documented as required to set |
| Channel OAS in repo | Present; correctly excluded from `files[]` |
| `.dockerignore` excluding openapi | Does not; only `docs/tasks` etc. |
| Pilot n8n runbook OPENAPI wording | Already says Story Intake ≠ channel; not STORY-21 primary surface |

---

## Cited paths

- `Dockerfile` (`COPY docs/openapi ./docs/openapi`, `WORKDIR /app`)
- `docs/openapi/story-intake-actions.openapi.yaml`
- `docs/openapi/aibridge-channel-v1.openapi.yaml`
- `.env.example` (§8 Phase A)
- `docs/runbooks/aibridge-web-service-local-railway.md` (§1.1b)
- `tests/test_story_21_oas_path_contract.py`
- `railpack.json` (alternative residual)
- `.dockerignore`
- Gate: `acceptance-verification-task-aibridge-21-t05-story-gate.md`
- REQ-05 §4.3–4.4 · R5-A-03 · R5-A-04 · TECH ADR-3 · §9

---

## Handoff

- **OPEN:** G-01 (Info), G-02 (Info)
- **Critical:** 0
- **OPEN counts:** Critical **0** · Medium **0** · Low **0** · Info **2**
- **next:** **P5** disposition
