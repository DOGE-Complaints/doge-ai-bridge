# Task: test — schema-boundary unit/contract (VAL-*)

**Status:** Done  
**P3 closed:** 2026-09-17T14:32:38Z  

**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-24-qa-json-schema-boundary.md`  
**Parent story:** [`STORY-AIBRIDGE-24-qa-json-schema-boundary.md`](../STORY-AIBRIDGE-24-qa-json-schema-boundary.md)  
**P1 scaffold:** 2026-09-17T14:26:09Z  
**Maps:** VAL-001…018 · OAS 400/413/422 · characterization VAL-014/018

## Purpose

Implement unit/contract tests under `tests/unit/` and/or `tests/contract/` asserting channel OAS codes for VAL-001…018 via `load_fixture` + TestClient. Characterization VAL-014 / VAL-018: capture-first — do not silently invent product trim or Content-Type policy. No fantasy APIs.

**Out of this task:** fixture generate (t02); story gate artifact (t04); Railway invent; live Telegram.

## Code Facts (verified exists — post P3)

1. `tests/contract/test_json_schema_boundary.py` — VAL must rows + characterization capture.
2. pytest: 20 passed (story-24 suite) · full `tests/contract/` 36 passed @ 2026-09-17T14:32:38Z.
3. VAL-014 / VAL-018 capture current 200; notes mark characterization.

## AC/DoD

- [x] Suite covers VAL-001…018 expectations from story matrix (must rows asserted; characterization capture-first).
- [x] Expected codes: 400 `bad_request` / 422 `semantic_invalid` / 413 `payload_too_large` per matrix — no silent invent.
- [x] VAL-014 and VAL-018 marked characterization in tests/docs.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/contract/test_json_schema_boundary.py` — **Done**

## Verification commands

```bash
cd doge-ai-bridge && DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/contract/test_json_schema_boundary.py -q --noconftest
```
