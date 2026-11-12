# Task: fix — hash rate-limit principal key (G-05)

**Status:** Done  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Wave:** `run_mode=aibridge_23_audit_20260917`  
**Gap:** G-05 (Low) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-23-qa-auth-ops-boundaries-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md`](../STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md)  
**P5 scaffold:** 2026-09-17T14:14:10Z  
**P6 Done:** 2026-09-17T14:18:28Z  
**Gate:** [acceptance-verification-task-aibridge-23-t06-audit-g05-rate-limit-principal.md](./acceptance-verification-task-aibridge-23-t06-audit-g05-rate-limit-principal.md) PASS  

## Purpose

In `channel_rate_limit_middleware`, replace `principal_key = auth[:24]` with a hashed/HMAC form so `RateLimiter` store keys do not contain raw `Authorization` Bearer prefix. Hygiene adjacent to AUTH-009; keep rate-limit behavior equivalent for distinct principals.

**Out of this task:** AUTH-009 log asserts (t05); invent Railway SUCCESS; IP/CIDR ACL for `/metrics` (G-02 WAIVED); rewrite rate-limit policy knobs beyond principal key.

## Code Facts (verified exists — post P6)

1. `src/aibridge/rate_limit.py` · `hash_principal_key` (SHA-256 · `p:<hex>`).
2. `src/aibridge/app.py` · `channel_rate_limit_middleware` uses `hash_principal_key(...)` (no `auth[:24]`).
3. Characterization: `test_rate_limit_principal_key_is_hashed` in contract suite.
4. pytest contract: 16 passed @ 2026-09-17T14:18:28Z.

## AC/DoD

- [x] Principal key stored in rate limiter is hashed/HMAC (no raw Bearer prefix substring from Authorization).
- [x] Distinct Authorization values still map to distinct principals (behavior preserved).
- [x] Existing contract / rate-limit tests still pass (or minimal characterization added).
- [x] `Skill declared: python-pro` present.

## Where to change

- `doge-ai-bridge/src/aibridge/app.py` — **Done**
- `doge-ai-bridge/src/aibridge/rate_limit.py` — **Done**
- `doge-ai-bridge/tests/contract/test_auth_ops_boundaries.py` — **Done** (characterization)

## Verification commands (P6)

```bash
rg -n 'principal_key|auth\[:24\]|hash_principal_key' doge-ai-bridge/src/aibridge/app.py doge-ai-bridge/src/aibridge/rate_limit.py
cd doge-ai-bridge && DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/contract/test_auth_ops_boundaries.py -q --noconftest
```
