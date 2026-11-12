# Task: implement — full schema validation + lift dry-run readiness gate

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md`  
**Parent story:** [`STORY-AIBRIDGE-14-p1-ops-schema-restart.md`](../STORY-AIBRIDGE-14-p1-ops-schema-restart.md)  
**P1 scaffold:** 2026-09-13T17:03:24Z  
**Maps:** Scope #3 · R3-P1-03 · Target #2

## Purpose

Replace unsafe subset validator with full schema validation (enum etc.). Only then may `AIBRIDGE_DRY_RUN=false` pass readiness (REQ-03 §2 / R3-P1-03).

## Code Facts (verified exists — P1)

1. `_validate_type` is a **minimal subset** — type/required/properties/additionalProperties; docstring says no full JSON Schema (`request_assembly.py`).
2. Dry-run gate: `readiness.py` fails when `not aibridge_schema_validation_complete and not aibridge_dry_run`.
3. Flag `AIBRIDGE_SCHEMA_VALIDATION_COMPLETE` defaults `False` (`config.py`).
4. Dry-run stash uses `validate_stash_body_local` — non-empty object only (`gateway.py`).

## AC/DoD

- [x] Full schema validation covers enum (and other REQ-01 §12 / pack-wire needs) before live stash.
- [x] Evidence proves validation; then readiness may accept `AIBRIDGE_DRY_RUN=false` with `AIBRIDGE_SCHEMA_VALIDATION_COMPLETE=true` (or equivalent proven path).
- [x] Tests: invalid enum rejected; dry-run gate lift only after complete flag + proven validator.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/request_assembly.py`, `readiness.py`, `config.py`, `gateway.py`, `tests/`.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "schema or enum or readyz or dry_run or story_14" --maxfail=10
```
