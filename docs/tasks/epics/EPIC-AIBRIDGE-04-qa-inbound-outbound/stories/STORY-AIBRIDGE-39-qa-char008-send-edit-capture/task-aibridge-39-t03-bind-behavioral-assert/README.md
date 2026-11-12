# Task: test — CHAR-008 behavioral assert beyond file-presence

**Status:** Done · 2026-09-18T14:06:43Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md`  
**Parent story:** [`STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md`](../STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md)  
**P1 scaffold:** 2026-09-18T14:03:38Z  
**Maps:** CHAR-008 · P1-Q3 · gaps §39 T03

## Purpose

Extend CHAR-008 bind beyond file-presence: assert capture payload non-empty (`response_states`, `retry_dedupe_policy`); keep meta path checks optional. If export/capture absent — keep **visible** `defer_reason` (fixture-index / DoD). No silent covered.

**Out of this task:** observe (t01); write fixture (t02); TRACEABILITY gate (t04); invent capture.

## AC/DoD

- [x] Behavioral assert on capture content **or** defer_reason remains visible.
- [x] Meta `test_char_*` path checks may remain; not sole Done evidence.
- [x] No invent live TG / export / product.
- [x] `Skill declared: test-master` present.

## Where to change (execute — not P1)

- `tests/test_qa_gates_layers_dod.py` (and/or dedicated CHAR-008 bind) — **P3**
- `tests/fixtures/meta/fixture-index.json` CHAR-008 row — **P3**
