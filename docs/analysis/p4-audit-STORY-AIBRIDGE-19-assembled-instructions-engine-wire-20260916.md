# P4 Audit — STORY-AIBRIDGE-19-assembled-instructions-engine-wire

| Field | Value |
|-------|-------|
| **Date** | 2026-09-16T12:12:40Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-03-…/STORY-AIBRIDGE-19-assembled-instructions-engine-wire/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md` |
| **Method** | Read/Glob + live pytest story-19; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (REQ-05 §4.1 / R5-A-01)** | **PASS** — ADR-1 helper + create_app wire + XOR prefix + fail-closed empty |
| **Bullrun t01–t05 Done** | **Confirmed** vs code + gate PASS 2026-09-16T12:10:09Z |
| **OPEN gaps** | **0 Medium · 0 Low · 3 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **7 passed** (`tests/test_story_19_engine_wire.py`) @ 2026-09-16T12:12Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-19** | 🟢 Implemented (P3 · next P4) · pkg-000016 | **Confirmed** code wire; gate PASS; **this P4** → next **P5** |
| **t01** | Done — apply-deployment helper | **Confirmed** `_apply_deployment_to_engine` `src/aibridge/app.py:196–230` |
| **t02** | Done — wire after stores | **Confirmed** call after `deployment_bundle` assign `app.py:429–433`; engine still created earlier `~324–387` (ADR-1, no full reorder) |
| **t03** | Done — tools + pack_id | **Confirmed** `strict_tool` → `engine.tools`; `pack_id=schema_id/schema_version` |
| **t04** | Done — fail-closed empty | **Confirmed** `error=assembled_instructions_empty` → `/readyz` 503; engine not overwritten to empty |
| **t05** | Done — story gate PASS | **Confirmed** `acceptance-verification-…t05…md` + pytest 7 passed |
| **pkg-000016** | Active (story 19 P3 · next P4) | `--verify` **ok 5 paths** @ audit time |
| **Siblings 20–22** | Todo (INDEX) | **Out of scope** this story; not re-audited |

---

## AC matrix (`$storyFile` Target · REQ-05 §4.1)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | `prompt_channel=prefix`; assembled in stable prefix; XOR (no API `instructions=`) | **PASS** | Helper sets `prompt_channel="prefix"` + `instructions`; `InterviewEngine._build_request` → `build_stable_prefix` + `assert "instructions" not in request.payload`; `test_create_app_wires_assembled_into_engine_and_prefix_xor` |
| 2 | Strict tool from deploy on interview path when schema id/version | **PASS** | Deploy `generate_strict_tool` when ids set; helper maps `engine.tools=[strict_tool]`; `test_create_app_wires_strict_tool_when_schema_configured` |
| 3 | No silent empty instructions when content_configured + empty/not-ready | **PASS** | Empty/whitespace assembled → fail-closed state (not mutate engine to `""`); `evaluate_readiness` uses `deployment.error` when content configured; `test_helper_fail_closed_empty_assembled` · `test_readyz_fails_when_assembled_empty_after_helper` |

### Scope extras

| Item | Status | Evidence |
|------|--------|----------|
| ADR-1 mutate (no create_app reorder) | **PASS** | Engine before `_init_stores`; mutate after deploy assign |
| No invent tool when `strict_tool is None` | **PASS** | `test_helper_does_not_invent_tool_when_strict_tool_none` |
| Loader still builds assembled | **PASS** | `content.py` `assembled_instructions` |
| Full manifest / Dockerfile / Phase A proof | **Out of scope** | Stories 20–22 |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Info** | Backlog `$storyFile` Meta says Implemented, but nested T01–T05 still **Todo**, Target AC still `[ ]`, and «Verified current state» still describes pre-wire Gap (`InterviewEngine` without bundle). Contradicts bullrun/pipeline Done + code. | Sync backlog verified state / nested task Status / AC checkboxes to Done; point to helper + tests. |
| **G-02** | **Info** | Materialized pipeline story §«Verified current state (P1 scaffold)» and task README «Code Facts» still cite pre-wire Gap / old line refs (`app.py:290–298`) after P3 wire landed at `app.py:196–230` / `429–433`. | Refresh scaffold «current state» to post-P3 facts; keep ADR-1 order note. |
| **G-03** | **Info** | Cross-repo [GPT UI `05` §5](../../../../GPT%20UI/docs/architecture/05-python-bridge-instruction-delivery.md) still titled «Verified gap — assembled ≠ engine» and claims `create_app` does not pass instructions (`app.py` L290–298). Fact: ADR-1 wire closes that runtime gap. | Update §5 to «closed by STORY-19» with helper/wire cites; or mark historical + link this audit. |

### Non-gaps

| Topic | Note |
|-------|------|
| Full `create_app` stores-before-engine reorder | Explicitly rejected Phase A / ADR-1 |
| `assembled_instructions_empty` via natural loader | Loader rejects empty files / empty `files[]`; helper still defense-in-depth for ready+empty/whitespace |
| Channel turns without `/readyz` gate | Pre-existing ops model; story AC targets readiness fail-closed — met |
| Stories 20–22 | Not in pkg-000016 DoD |

---

## Cited paths

- `src/aibridge/app.py` (`_apply_deployment_to_engine`, create_app wire)
- `src/aibridge/interview.py` (`prompt_channel`, `_build_request`, XOR)
- `src/aibridge/request_assembly.py` (`build_stable_prefix`)
- `src/aibridge/deployment.py` (`strict_tool`, `ready`)
- `src/aibridge/content.py` (`assembled_instructions`)
- `src/aibridge/readiness.py` (`content_configured` + `deployment.error`)
- `tests/test_story_19_engine_wire.py`
- Gate: `acceptance-verification-task-aibridge-19-t05-story-gate.md`
- REQ-05 §4.1 · R5-A-01 · TECH ADR-1

---

## Handoff

- **OPEN:** G-01 (Info), G-02 (Info), G-03 (Info)
- **Critical:** 0
- **OPEN counts:** Critical **0** · Medium **0** · Low **0** · Info **3**
- **next:** **P5** disposition
