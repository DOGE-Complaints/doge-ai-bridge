# Task: fixtures+test — READY-005 intake missing (G-03)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_33_audit_20260917`  
**Gap:** G-03 (Low) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-33-qa-readiness-configuration-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-33-qa-readiness-configuration.md`](../STORY-AIBRIDGE-33-qa-readiness-configuration.md)  
**P5 scaffold:** 2026-09-17T21:04:00Z  
**P6 closed:** 2026-09-17T21:07:50Z  
**Gate:** [acceptance-verification-task-aibridge-33-t07-audit-g03-ready005-intake-missing.md](./acceptance-verification-task-aibridge-33-t07-audit-g03-ready005-intake-missing.md) PASS  
**Maps:** READY-005 · `intake_base_url_missing`

## Purpose

Add settings fixture `ready-intake-missing` → 503 `intake_base_url_missing` under READY-005; keep existing non-HTTPS fixture; TRACEABILITY/fixture notes — «conflicting» **N/A**. Promote=copy only. **No** product invent; **no** live Telegram / Railway invent.

## AC/DoD

- [x] Package + `tests/fixtures/settings/ready-intake-missing.json` (hash_eq); matrix READY-005.
- [x] Suite asserts 503 `intake_base_url_missing`; non-HTTPS fixture retained.
- [x] TRACEABILITY READY-005 notes «conflicting» N/A.
- [x] No live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- package `fixtures/` + `tests/fixtures/settings/` — **P6 Done** (promote=copy)
- `tests/contract/test_readyz_configuration.py` — **P6 Done**
- TRACEABILITY-MATRIX READY-005 note — **P6 Done**
