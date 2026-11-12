# STORY-AIBRIDGE-43 — Minimal ValidationContext bind + readiness

## Meta
- **Key:** `STORY-AIBRIDGE-43-validation-context-bind-readyz`
- **Status:** ✅ P6 Done · G-01/G-02/G-03 CLOSED · next **P7** · `run_mode=aibridge_43_audit_20260924` · pkg-000042 · 2026-09-24T11:43:20Z
- **Parent Epic:** [`EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat.md`](../../EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat.md)
- **source:** `backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-43-validation-context-bind-readyz.md`
- **decision_ref:** [`STORY-AIBRIDGE-43-….md`](../../../../backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-43-validation-context-bind-readyz.md) · [`REQ-07`](../../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §5 · [`TECH-ARCH-REQ-07`](../../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §2.3–2.4
- **Package:** [`req-07-openai-strict-schema-compat/INDEX.md`](../../../../backlog-stories/req-07-openai-strict-schema-compat/INDEX.md)
- **Skill declared:** `python-pro` · Composition: `fastapi-expert`
- **Active pkg (wave):** `pkg-000042-20260924-epic-aibridge-05-story-43-validation-context-bind-readyz.yaml`
- **P1 materialize:** 2026-09-24T11:30:36Z
- **P3 close:** 2026-09-24T11:33:03Z · [run-summary](../../../../run-reports/run-summary-20260924-1133-story-aibridge-43-p3.md)
- **Gate:** [t04](./task-aibridge-43-t04-story-gate/README.md) **PASS**
- **Depends:** STORY-41 · STORY-42 (Done)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-07 ValidationContext | [`REQ-07`](../../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §5 · AIB-COMPAT-05/07/08 |
| Tech-arch bind | [`TECH-ARCH-REQ-07`](../../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §2.3–2.4 |
| Code seam | `src/aibridge/app.py` · `confirm.py` · `coordinator.py` · `readiness.py` |

## Scope
Bind `ConfirmationGuard.validation_context` in `create_app` composition with dual schemas when content configured. `/readyz` not_ready if VC missing/invalid when gates required (default reason `validation_context_not_bound`). Prefer existing `coordinator.ValidationContext` shape.

## Вне scope
- Full REQ-04 confirm/FSM/token; new public HTTP APIs; invent alternate dataclass; live Telegram (45); merge-gate invent (44).

## Context
P3: `_bind_validation_context` wires projected tool_parameters + canonical pack + wire schema; readiness reason `validation_context_not_bound`.

## Target / AC
- [x] Dual Gate contract wired in production composition (TECH-ARCH §2.3–2.4).
- [x] Missing/invalid VC → `/readyz` not_ready with stable reason (`validation_context_not_bound`).
- [x] AC-06 partial: no silent accept of consequential FC without schemas when content configured.
- [x] Nested tasks Done at execute.

## Nested tasks (pkg-000042 + P5 audit override)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-43-t01-validation-context-create-app-bind](./task-aibridge-43-t01-validation-context-create-app-bind/README.md) | create_app VC bind | **Done** |
| t02 | [task-aibridge-43-t02-readyz-validation-context-fail-closed](./task-aibridge-43-t02-readyz-validation-context-fail-closed/README.md) | readyz fail-closed | **Done** |
| t03 | [task-aibridge-43-t03-vc-bind-readyz-tests](./task-aibridge-43-t03-vc-bind-readyz-tests/README.md) | bind + readyz tests | **Done** |
| t04 | [task-aibridge-43-t04-story-gate](./task-aibridge-43-t04-story-gate/README.md) | story AC gate | **PASS** |
| t05 | [task-aibridge-43-t05-audit-g01-g03-envelope-schema-version-stamp](./task-aibridge-43-t05-audit-g01-g03-envelope-schema-version-stamp/README.md) | G-01 · G-03 envelope stamp | **Done** · P6 |
| t06 | [task-aibridge-43-t06-audit-g02-backlog-verified-sync](./task-aibridge-43-t06-audit-g02-backlog-verified-sync/README.md) | G-02 backlog Verified | **Done** · P6 |

### P5 disposition → P6 CLOSED (2026-09-24T11:43:20Z)

| Gap | Sev | Disposition | Task |
|-----|-----|-------------|------|
| G-01 | Medium | TASKED → **CLOSED** (P6) | t05 Done |
| G-02 | Low | TASKED → **CLOSED** (P6) | t06 Done |
| G-03 | Low | TASKED → **CLOSED** (P6) | t05 Done |
| G-04 | Info | **WAIVED** info-nonblocking | — |

**activation:** `run_mode=aibridge_43_audit_20260924` · [p6](../../../../run-reports/run-summary-20260924-1143-story-aibridge-43-p6.md) · next=P7
