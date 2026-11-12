# Task: test — AUTH-009 forbid_substrings_in_logs (G-01)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_23_audit_20260917`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-23-qa-auth-ops-boundaries-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md`](../STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md)  
**P5 scaffold:** 2026-09-17T14:14:10Z  
**P6 Done:** 2026-09-17T14:18:28Z  
**Gate:** [acceptance-verification-task-aibridge-23-t05-audit-g01-auth009-logs.md](./acceptance-verification-task-aibridge-23-t05-audit-g01-auth009-logs.md) PASS  

## Purpose

Assert fixture field `forbid_substrings_in_logs` from `tests/fixtures/spies/auth-forbid-bearer-leak.json` during AUTH-009 401 path (capture structured/app logs or fail-closed spy bag). Keep existing error-body + `/metrics` asserts. Do not invent product APIs.

**Out of this task:** implement G-05 rate-limit principal (t06); invent Railway SUCCESS; network ACL middleware (G-02 WAIVED); wall-clock timing microbench (G-03 WAIVED).

## Code Facts (verified exists — post P6)

1. Spy fixture: `tests/fixtures/spies/auth-forbid-bearer-leak.json` · `forbid_substrings_in_logs` declared.
2. Contract: `tests/contract/test_auth_ops_boundaries.py` · AUTH-009 asserts error + metrics + log bag from fixture needles.
3. AUTH-009 path: Authorization carries CHANNEL while settings accept a different token → 401; needles absent from logs/error/metrics.
4. pytest contract: 16 passed @ 2026-09-17T14:18:28Z.

## AC/DoD

- [x] Test reads and asserts `forbid_substrings_in_logs` needles absent from captured logs on 401 AUTH-009 path.
- [x] Existing error-body + `/metrics` forbid asserts remain.
- [x] Contract suite still passes (`DATABASE_URL=memory` + `--noconftest`).
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/tests/contract/test_auth_ops_boundaries.py` — **Done**

## Verification commands (P6)

```bash
rg -n 'forbid_substrings_in_logs' doge-ai-bridge/tests/contract/test_auth_ops_boundaries.py \
  doge-ai-bridge/tests/fixtures/spies/auth-forbid-bearer-leak.json
cd doge-ai-bridge && DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/contract/test_auth_ops_boundaries.py -q --noconftest
```
