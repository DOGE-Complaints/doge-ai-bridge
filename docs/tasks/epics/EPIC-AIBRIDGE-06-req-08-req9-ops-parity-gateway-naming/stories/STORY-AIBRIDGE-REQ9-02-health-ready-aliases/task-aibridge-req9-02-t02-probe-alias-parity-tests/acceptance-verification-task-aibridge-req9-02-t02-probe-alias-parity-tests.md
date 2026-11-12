# Acceptance — task-aibridge-req9-02-t02-probe-alias-parity-tests

| Field | Value |
|-------|-------|
| **Date** | 2026-09-26T12:26:24Z |
| **Result** | **Done** |

## Disk facts

| Claim | Evidence |
|-------|----------|
| `/health` ↔ `/healthz` parity | `tests/test_health.py` `test_health_alias_parity_with_healthz` |
| `/ready` ↔ `/readyz` ready | `test_ready_alias_parity_with_readyz_when_ready` |
| `/ready` ↔ `/readyz` 503 | `test_ready_alias_parity_with_readyz_when_not_ready` |
| pytest | `.venv/bin/python -m pytest -q tests/test_health.py` → **7 passed** |
