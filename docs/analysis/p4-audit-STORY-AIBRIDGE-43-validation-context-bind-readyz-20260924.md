# P4 Audit — STORY-AIBRIDGE-43-validation-context-bind-readyz

| Field | Value |
|-------|-------|
| **Date** | 2026-09-24T11:38:11Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-05-…/STORY-AIBRIDGE-43-validation-context-bind-readyz/STORY-AIBRIDGE-43-validation-context-bind-readyz.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-43-validation-context-bind-readyz.md` |
| **Method** | Read/Glob + live pytest filter (44) + `app._bind_validation_context` / `readiness` / `coordinator` / Gate 3 enum probe; no product patches; no live TG invent |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway / live Telegram** | **No** Railway SUCCESS · **No** live Telegram PASS invented |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (VC bind + readyz fail-closed)** | **PASS (core bind/readyz)** · **1 Medium** residual — `ServerConstants.schema_version` stamp wrong for Gate 3 envelope enum |
| **Bullrun t01–t04 Done** | **Confirmed** vs code + acceptance + gate PASS 2026-09-24T11:33:03Z |
| **OPEN gaps** | **0 Critical · 1 Medium · 2 Low · 1 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **44 passed** (`test_validation_context_bind` + story-19 + readyz contract + openai projection) @ 2026-09-24T11:38:11Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-43** | ✅ P3 Done · next P4 · pkg-000042 | **Confirmed** bind + readyz · **this P4** → next **P5** · residual **G-01 Medium** |
| **t01** | Done — create_app VC bind | **Confirmed** `_bind_validation_context` · dual schemas · **G-01** constants stamp |
| **t02** | Done — readyz fail-closed | **Confirmed** reason `validation_context_not_bound` |
| **t03** | Done — tests · 5 | **Confirmed** 5 in module · filter **44** |
| **t04** | Done · PASS | **Confirmed** acceptance gate |
| **pkg-000042** | Active · 4 paths | YAML under `aibridge-active-packages/` |
| **Backlog Verified** | «create_app does not assign» | **Stale** vs P3 bind → **Low G-02** |
| **active-package.current comment** | «next P2» | **Stale** → **Info G-04** |

---

## AC matrix (`$storyFile` / pipeline · REQ-07 §5 · TECH-ARCH §2.3–2.4)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| Dual Gate contract wired | `tool_parameters`←projected; `pack_schema`←canonical pack; `wire_schema`←Story Intake; `constants` | **PASS (bind)** · **Medium G-01** | `_bind_validation_context` wires all four; test asserts projected params == `strict_tool["parameters"]`; pack/wire from disk/OAS · **constants.schema_version incorrectly set to pack version** |
| `/readyz` missing/invalid VC | not_ready + `validation_context_not_bound` | **PASS** | `test_readyz_validation_context_not_bound_when_missing` · readiness after content-ready check |
| AC-06 partial | No silent FC accept without schemas | **PASS** | `validate_function_calls(..., validation=None)` → `schemas not configured` |
| Prefer existing `ValidationContext` | No alternate dataclass invent | **PASS** | `build_validation_context` → `coordinator.ValidationContext` |
| Content not configured | VC bind not required | **PASS** | `test_no_content_skips_vc_bind_requirement` |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| `/readyz` passes guard VC | **PASS** | `app.py` ~596–597 `evaluate_readiness(..., validation_context=vc)` |
| Fail-closed leave unbound on bind error | **PASS** | early `return` in `_bind_validation_context` |
| Live TG / REQ-04 expand | **Out of scope** | |
| SPA / hasUxPipeline | false | |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | `_bind_validation_context` sets `ServerConstants(schema_version=schema_version or "m2…")` where `schema_version` is **pack** `DOGESTONIA_SCHEMA_VERSION` (e.g. `v1`). Wire OAS requires top-level `schema_version` enum `["m2.story_intake_envelope.v2"]`. Live bind yields `constants.schema_version='v1'` → `assemble_server_body` stamps envelope field `v1` → Gate 3 **enum mismatch** (verified ad-hoc). `schema_version_pack` is correctly `v1`. Suite never asserts envelope constant. | Stamp `constants.schema_version` with envelope default `m2.story_intake_envelope.v2` (keep pack only in `schema_version_pack`); add assert in bind tests. |
| **G-02** | **Low** | Backlog `$storyFile` «Verified current state» still claims `create_app` does not assign `validation_context` (pre-P3 emit text) while P3 bind exists. | Sync Verified section to post-P3 bound state. |
| **G-03** | **Low** | Bind tests do not assert `vc.constants.schema_version == "m2.story_intake_envelope.v2"` (allowed G-01 to ship). | Add constant envelope assert alongside schema_id. |
| **G-04** | **Info** | `aibridge-active-package.current.yaml` header still «P1.3 APPLY · next P2» though P3 closed 11:33:03Z. | Refresh pointer comment. |

### Non-gaps

| Topic | Note |
|-------|------|
| Invent alternate ValidationContext dataclass | Avoided |
| Silent FC accept without VC | Avoided |
| Invent live TG / OpenAI network SUCCESS | Avoided |
| Pack vs projected confusion for Gate 1/2 | Avoided — projected params + disk pack |

### Regressions

| Topic | Note |
|-------|------|
| vs gate t04 (44 passed) | **None** — re-run **44 passed** @ 2026-09-24T11:38:11Z |
| STORY-41 projection suite in filter | Still green |

---

## Cited paths

- `src/aibridge/app.py` — `_bind_validation_context`, `/readyz` VC pass-through
- `src/aibridge/readiness.py` — `validation_context_not_bound`
- `src/aibridge/coordinator.py` — `ValidationContext`, `build_validation_context`, `validation_context_is_bound`
- `src/aibridge/confirm.py` — `validation_context` field
- `src/aibridge/tool_gen.py` — `load_wire_request_schema`
- `src/aibridge/request_assembly.py` — `ServerConstants`, `assemble_server_body`
- `docs/openapi/story-intake-actions.openapi.yaml` — `schema_version` enum
- `tests/test_validation_context_bind.py`
- Gate: `…/task-aibridge-43-t04-story-gate/acceptance-verification-….md`
- P3: `docs/tasks/run-reports/run-summary-20260924-1133-story-aibridge-43-p3.md`
- Pkg: `docs/tasks/aibridge-active-packages/pkg-000042-20260924-epic-aibridge-05-story-43-validation-context-bind-readyz.yaml`

---

## Handoff

- **OPEN gaps:** 0 Critical · **1 Medium** · **2 Low** · **1 Info**
- **OPEN IDs:** G-01, G-02, G-03, G-04
- **Product Story AC/DoD (bind + readyz):** **PASS core** · Medium constants stamp residual
- **next:** **P5** (disposition; do not implement in P4)
