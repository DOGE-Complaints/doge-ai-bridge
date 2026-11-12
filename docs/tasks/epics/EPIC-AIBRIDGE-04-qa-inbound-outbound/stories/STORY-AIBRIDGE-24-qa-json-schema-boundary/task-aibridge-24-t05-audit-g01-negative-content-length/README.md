# Task: fix — VAL-017 negative Content-Length → 400 (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Wave:** `run_mode=aibridge_24_audit_20260917`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-24-qa-json-schema-boundary-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-24-qa-json-schema-boundary.md`](../STORY-AIBRIDGE-24-qa-json-schema-boundary.md)  
**P5 scaffold:** 2026-09-17T14:40:05Z  
**P6 closed:** 2026-09-17T14:44:12Z  
**Gate:** [acceptance-verification-task-aibridge-24-t05-audit-g01-negative-content-length.md](./acceptance-verification-task-aibridge-24-t05-audit-g01-negative-content-length.md) PASS  

## Purpose

Align VAL-017 with guide **must**: negative `Content-Length` → 400 `bad_request`. In `BodySizeLimitMiddleware`, reject `length < 0` (after successful `int()` parse). Add/extend fixture+contract assert for `Content-Length: -1`. Keep existing non-integer Content-Length → 400 case.

**Out of this task:** VAL-016 DB side-effect assert (t06); invent trim policy (G-05 WAIVED); invent Railway SUCCESS.

## Code Facts (verified exists — P5 APPLY)

1. `src/aibridge/app.py` · `BodySizeLimitMiddleware` — `int(content_length)` without `length < 0` check; probe `-1` → 422.
2. Fixture `val-invalid-content-length` only covers non-integer CL → 400.
3. Guide §10.2 VAL-017: Invalid/**negative** Content-Length → 400.

## AC/DoD

- [x] Negative Content-Length rejected with HTTP 400 `bad_request` before body parse.
- [x] Non-integer Content-Length still 400 `bad_request`.
- [x] Fixture + contract assert cover negative branch (promote=copy if new package envelope).
- [x] `Skill declared: python-pro` present.

## Where to change

- `doge-ai-bridge/src/aibridge/app.py` — **P6 Done**
- `tests/fixtures/channel/` (+ package `fixtures/`) — **P6 Done** (`val-negative-content-length`)
- `tests/contract/test_json_schema_boundary.py` — **P6 Done**

## Verification commands (P6)

```bash
rg -n 'Content-Length|length < 0|bad_request' doge-ai-bridge/src/aibridge/app.py
cd doge-ai-bridge && DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/contract/test_json_schema_boundary.py -q --noconftest
```
