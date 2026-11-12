# Task: test — VAL-016 assert no DB side effect on 413 (G-02)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_24_audit_20260917`  
**Gap:** G-02 (Low) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-24-qa-json-schema-boundary-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-24-qa-json-schema-boundary.md`](../STORY-AIBRIDGE-24-qa-json-schema-boundary.md)  
**P5 scaffold:** 2026-09-17T14:40:05Z  
**P6 closed:** 2026-09-17T14:44:12Z  
**Gate:** [acceptance-verification-task-aibridge-24-t06-audit-g02-val016-db-side-effect.md](./acceptance-verification-task-aibridge-24-t06-audit-g02-val016-db-side-effect.md) PASS  

## Purpose

On VAL-016 oversize → 413 path, assert no DB/dedupe side effect beyond request handling (`EventDedupeStore.side_effect_count(...)==0` or equivalent). Keep existing `no_openai_calls` assert.

**Out of this task:** negative Content-Length product fix (t05); invent Railway SUCCESS; change rate-limit / trim policy.

## Code Facts (verified exists — P5 APPLY)

1. Contract VAL-016 asserts `no_openai_calls` only.
2. P4 probe: after 413, `side_effect_count==0` but unasserted.
3. Suite: `tests/contract/test_json_schema_boundary.py`.

## AC/DoD

- [x] VAL-016 413 path asserts DB/dedupe side-effect counter == 0 (or equivalent).
- [x] Existing `no_openai_calls` assert remains.
- [x] Contract suite still passes (`DATABASE_URL=memory` + `--noconftest`).
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/tests/contract/test_json_schema_boundary.py` — **P6 Done**

## Verification commands (P6)

```bash
rg -n 'side_effect|no_openai|VAL-016|payload-too-large' \
  doge-ai-bridge/tests/contract/test_json_schema_boundary.py
cd doge-ai-bridge && DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/contract/test_json_schema_boundary.py -q --noconftest
```
