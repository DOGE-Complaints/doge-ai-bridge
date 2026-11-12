# STORY-AIBRIDGE-42 — Canonical uniqueItems validation (Gate 2)

## Meta
- **Key:** `STORY-AIBRIDGE-42-canonical-uniqueitems-validation`
- **Status:** ✅ P6 Done · G-01/G-02 CLOSED · next **P7** · `run_mode=aibridge_42_audit_20260924` · pkg-000041 · 2026-09-24T11:25:01Z
- **Parent Epic:** [`EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat.md`](../../EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat.md)
- **source:** `backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md`
- **decision_ref:** [`STORY-AIBRIDGE-42-….md`](../../../../backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md) · [`REQ-07`](../../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) · [`TECH-ARCH-REQ-07`](../../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §2.3 · §2.5
- **Package:** [`req-07-openai-strict-schema-compat/INDEX.md`](../../../../backlog-stories/req-07-openai-strict-schema-compat/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000041-20260924-epic-aibridge-05-story-42-canonical-uniqueitems-validation.yaml`
- **P1 materialize:** 2026-09-24T11:13:54Z
- **P3 close:** 2026-09-24T11:17:36Z · [run-summary](../../../../run-reports/run-summary-20260924-1117-story-aibridge-42-p3.md)
- **Gate:** [t04](./task-aibridge-42-t04-story-gate/README.md) **PASS**

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-07 uniqueItems | [`REQ-07`](../../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) AIB-COMPAT-04/05 · §8.2 · §9.1 · T-UNIQUE-* |
| Tech-arch Gate 2 | [`TECH-ARCH-REQ-07`](../../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §2.3 · §2.5 |
| Code seam | `src/aibridge/request_assembly.py` · `readiness.py` |

## Scope
Enforce JSON Schema `uniqueItems: true` in Gate 2 canonical validator (structural equality; key-order independent). Extend `schema_validation_complete()` to prove uniqueness. Gate 2 always uses untouched canonical pack schema.

## Вне scope
- OpenAI projection (STORY-41); ValidationContext bind (43); live Telegram (45); deleting `uniqueItems` from pack JSON.

## Context
P3: `FULL_SCHEMA_KEYWORDS` includes `uniqueItems`; Gate 2 enforces structural uniqueness; `schema_validation_complete()` probes uniqueItems behaviorally.

## Target / AC
- [x] AC-04: duplicate house ids under one street rejected at **unit Gate 2** (`validate_gate2_pack_payload`). Evidence = Gate 2 contract only — **not** invent freeze / Send / gateway write proof in this story.
- [x] T-UNIQUE-01…09 covered by tests (incl. Uus Veerenni pack path).
- [x] Incomplete uniqueness capability → readiness fail-closed (`schema_validation_incomplete*`).
- [x] Nested tasks Done at execute (incl. P6 gap t05–t06).

> **Footnote (G-01 / P6):** end-to-end FC path (freeze / Send / gateway) requires `ValidationContext` bind — owned by STORY-AIBRIDGE-43. Do not invent `app.py` VC bind here.

## Nested tasks (pkg-000041 + P5 audit override)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-42-t01-uniqueitems-gate2-enforcement](./task-aibridge-42-t01-uniqueitems-gate2-enforcement/README.md) | Gate 2 uniqueItems enforce | **Done** |
| t02 | [task-aibridge-42-t02-schema-validation-complete-uniqueitems](./task-aibridge-42-t02-schema-validation-complete-uniqueitems/README.md) | readiness prove | **Done** |
| t03 | [task-aibridge-42-t03-uniqueitems-t-unique-tests](./task-aibridge-42-t03-uniqueitems-t-unique-tests/README.md) | T-UNIQUE / AC-04 tests | **Done** |
| t04 | [task-aibridge-42-t04-story-gate](./task-aibridge-42-t04-story-gate/README.md) | story AC gate | **PASS** |
| t05 | [task-aibridge-42-t05-audit-g01-ac04-gate2-scope-docs](./task-aibridge-42-t05-audit-g01-ac04-gate2-scope-docs/README.md) | G-01 AC-04 docs | **Done** · CLOSED |
| t06 | [task-aibridge-42-t06-audit-g02-uniqueitems-negative-prove](./task-aibridge-42-t06-audit-g02-uniqueitems-negative-prove/README.md) | G-02 negative prove | **Done** · CLOSED |

### P5 disposition (2026-09-24T11:22:57Z) → P6 CLOSED (2026-09-24T11:25:01Z)

| Gap | Sev | Disposition | Task |
|-----|-----|-------------|------|
| G-01 | Low | **TASKED→CLOSED** | t05 Done |
| G-02 | Low | **TASKED→CLOSED** | t06 Done |
| G-03 | Info | **WAIVED** info-nonblocking | — |
| G-04 | Info | **WAIVED** info-nonblocking | — |

**activation:** `run_mode=aibridge_42_audit_20260924` · [p5](../../../../run-reports/run-summary-20260924-1122-story-aibridge-42-p5-disposition.md) · [p6](../../../../run-reports/run-summary-20260924-1125-story-aibridge-42-p6.md)
