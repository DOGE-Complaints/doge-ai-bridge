# Task: test — CHAR-001…008 bind refs (G-03)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_35_audit_20260917`  
**Gap:** G-03 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-35-qa-gates-layers-dod-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-35-qa-gates-layers-dod.md`](../STORY-AIBRIDGE-35-qa-gates-layers-dod.md)  
**P5 scaffold:** 2026-09-17T21:51:00Z  
**P6 closed:** 2026-09-17T22:21:55Z  
**Maps:** CHAR-001…008 · guide §16

## Purpose

Bind each CHAR-001…008 to existing capture suite/fixture paths (`refs` / `bound_tests`) **or** document per-CHAR defer reason; suite asserts refs present. Capture-first — **no** silent product invent for CHAR answers. Opportunistic: align TRACEABILITY Gate-5 to deferred (G-04 hygiene). **No** live Telegram / Railway invent.

**Out of this task:** Gate suite evidence (t05); Layer D (t06); inventing product behavior for CHAR questions.

## AC/DoD

- [x] Each CHAR-001…008 has `refs`/`bound_tests` **or** explicit defer reason in fixture-index program.
- [x] Checklist suite asserts refs/defer completeness (not labels-only).
- [x] No live Telegram / Railway SUCCESS invent / silent product invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/fixtures/meta/fixture-index.json` (+ package original promote=copy) — **P6**
- `tests/test_qa_gates_layers_dod.py` — **P6**
- Optional: `TRACEABILITY-MATRIX.md` Gate-5 row — **P6**
