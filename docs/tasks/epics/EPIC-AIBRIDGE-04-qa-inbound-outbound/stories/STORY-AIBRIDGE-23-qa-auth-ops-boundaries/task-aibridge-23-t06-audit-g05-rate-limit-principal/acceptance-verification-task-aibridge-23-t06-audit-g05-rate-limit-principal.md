# Acceptance verification — task-aibridge-23-t06-audit-g05-rate-limit-principal

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T14:18:28Z |
| **Story** | STORY-AIBRIDGE-23-qa-auth-ops-boundaries |
| **Gap** | G-05 (Low) |
| **Wave** | `run_mode=aibridge_23_audit_20260917` |
| **Pkg** | pkg-000020 (YAML default unchanged) |

## AC check

- [x] Principal key is SHA-256 hash (`hash_principal_key`) — no raw Bearer prefix in store.
- [x] Distinct Authorization values map to distinct principals.
- [x] Contract + characterization tests pass.
- [x] `Skill declared: python-pro` present.

## Evidence

```text
rg: hash_principal_key in app.py / rate_limit.py; no auth[:24]
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/contract/test_auth_ops_boundaries.py -q --noconftest → 16 passed
```
