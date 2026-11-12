# Task: test — remove VAL characterization tautology band (QUAL-001)

**Status:** Done · 2026-09-18T14:28:02Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-40-qa-suite-assert-hygiene.md`  
**Parent story:** [`STORY-AIBRIDGE-40-qa-suite-assert-hygiene.md`](../STORY-AIBRIDGE-40-qa-suite-assert-hygiene.md)  
**P1 scaffold:** 2026-09-18T14:25:26Z  
**P3 closed:** 2026-09-18T14:28:02Z  
**Maps:** QUAL-001 · P1-Q1 · gaps §40 T01

## Purpose

Edit `tests/contract/test_json_schema_boundary.py`::`test_val_characterization_capture_first`: **delete** `assert 100 <= response.status_code < 600`; keep explicit expected status (+ shape) for VAL-014/018. No invent product VAL behavior.

**Out of this task:** hash_eq policy docs (t02); QUAL-003 WAIVE (t03); Gate-5 / live TG.

## AC/DoD

- [x] Vacuous HTTP band assert removed.
- [x] Explicit expected status (+ shape) remain for VAL-014/018.
- [x] Contract suite still green under filter.
- [x] `Skill declared: test-master` present.

## Where changed

- `tests/contract/test_json_schema_boundary.py` — band removed

## Evidence

```text
.venv/bin/python -m pytest tests/contract/test_json_schema_boundary.py -q
21 passed
```
