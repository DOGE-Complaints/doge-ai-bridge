# Task: test — fixture expect SSOT after mint-replace (G-02)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_29_audit_20260917`  
**Gap:** G-02 (Low) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-29-qa-action-token-fsm-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-29-qa-action-token-fsm.md`](../STORY-AIBRIDGE-29-qa-action-token-fsm.md)  
**P5 scaffold:** 2026-09-17T19:35:13Z  
**P6 closed:** 2026-09-17T19:38:16Z  
**Gate:** [acceptance-verification-task-aibridge-29-t06-audit-g02-fixture-expect-ssot.md](./acceptance-verification-task-aibridge-29-t06-audit-g02-fixture-expect-ssot.md) PASS  

## Purpose

Drive HTTP/unit paths from channel fixture `body` + `expect` after mint-replace `PLACEHOLDER_TOKEN` (ACT-001 Looks right · ACT-005 random). Assert `expect.http_status` / `state` / `error_code` from envelope — fixture expect is SSOT. **No** live Telegram / Railway invent.

## AC/DoD

- [x] ACT-001/005 load channel fixture body, mint-replace PLACEHOLDER where needed, assert against envelope `expect`.
- [x] Representative IDs: ACT-001 and ACT-005 (unit + HTTP).
- [x] Package originals intact (promote=copy unchanged).
- [x] No live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/unit/test_action_token_fsm.py` · `tests/integration/test_action_token_fsm_http.py` — **P6 Done**
