# Task: fix — schema_validation_complete probes validator (G-03)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_14_audit_20260913`  
**Gap:** G-03 (Info) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-14-p1-ops-schema-restart-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-14-p1-ops-schema-restart.md`](../STORY-AIBRIDGE-14-p1-ops-schema-restart.md)  
**P5 scaffold:** 2026-09-13T17:18:05Z  
**P6 Done:** 2026-09-13T17:23:30Z  
**Maps:** R3-P1-03 readiness helper

## Purpose

Replace frozenset-membership tautology in `schema_validation_complete()` with a real validator probe (enum reject + const accept). Keep `AIBRIDGE_SCHEMA_VALIDATION_COMPLETE` as operator attestation.

## AC/DoD

- [x] `schema_validation_complete()` fails closed if enum/const validation broken.
- [x] Existing readyz dry-run-lift tests still green.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/request_assembly.py`, `tests/test_story_14_audit_gaps.py`

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "schema_validation or story_14" --maxfail=10
```
