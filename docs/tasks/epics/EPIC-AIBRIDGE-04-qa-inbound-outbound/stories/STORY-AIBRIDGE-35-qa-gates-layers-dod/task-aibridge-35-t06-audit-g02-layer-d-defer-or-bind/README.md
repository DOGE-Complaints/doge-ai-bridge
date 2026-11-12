# Task: test — Layer D defer-or-bind (G-02)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_35_audit_20260917`  
**Gap:** G-02 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-35-qa-gates-layers-dod-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-35-qa-gates-layers-dod.md`](../STORY-AIBRIDGE-35-qa-gates-layers-dod.md)  
**P5 scaffold:** 2026-09-17T21:51:00Z  
**P6 closed:** 2026-09-17T22:21:55Z  
**Maps:** Layer D · guide §9

## Purpose

Add Layer D (container/deployment) evidence dir/tests **or** explicit `deferred`/`WAIVE` in fixture-index `program` + suite assert. Optionally bind existing STORY-21/22 docker/container proofs as evidence paths (assert-only). Layer F / Gate-5 stay `deferred_live`. **No** Railway SUCCESS invent; **no** live Telegram.

**Out of this task:** Gate-1…4 suite bind (t05); CHAR refs (t07); inventing container suite from scratch beyond defer-or-bind.

## AC/DoD

- [x] Layer D present in program as deferred/WAIVE **or** bound to evidence paths/tests.
- [x] Checklist suite asserts Layer D disposition (not silently absent).
- [x] No live Telegram / Railway SUCCESS invent / silent product invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/test_qa_gates_layers_dod.py` — **P6**
- `tests/fixtures/meta/fixture-index.json` (+ package original promote=copy) — **P6**
- Optional bind: Dockerfile / STORY-21/22 proof paths — **P6** (assert-only)
