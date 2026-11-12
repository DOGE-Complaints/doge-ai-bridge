# Task: test — Gate-1…4 suite evidence bind (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Wave:** `run_mode=aibridge_35_audit_20260917`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-35-qa-gates-layers-dod-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-35-qa-gates-layers-dod.md`](../STORY-AIBRIDGE-35-qa-gates-layers-dod.md)  
**P5 scaffold:** 2026-09-17T21:51:00Z  
**P6 closed:** 2026-09-17T22:21:55Z  
**Maps:** Gate-1…4 · guide §15

## Purpose

Bind Gate-1…4 checklist to recorded suite gate PASS (subprocess `-q` green **or** acceptance-verification paths) **or** mark `program.gates` characterization «path-index only» + TRACEABILITY note. Opportunistic: mirror evidence paths into `program.gates` (G-05 hygiene). Capture-first; **no** live Telegram / Railway SUCCESS invent; **no** silent product invent.

**Out of this task:** Layer D (t06); CHAR refs (t07); product invent; live Gate-5.

## AC/DoD

- [x] Gate-1…4 evidence bound to suite PASS artifacts and/or explicit path-index characterization in fixture-index program.
- [x] Checklist suite asserts the chosen bind (not only `is_file()` unless path-index characterization documented).
- [x] No live Telegram / Railway SUCCESS invent / silent product invent.
- [x] `Skill declared: python-pro` present.

## Where to change

- `tests/test_qa_gates_layers_dod.py` — **P6**
- `tests/fixtures/meta/fixture-index.json` (+ package original promote=copy) — **P6**
