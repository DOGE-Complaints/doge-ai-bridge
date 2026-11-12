# Acceptance verification — task-aibridge-23-t04-story-gate

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T14:02:23Z |
| **Story** | STORY-AIBRIDGE-23-qa-auth-ops-boundaries |
| **Pkg** | pkg-000020 |
| **ADR** | ADR-Q1/Q2 |

## AC check

- [x] AUTH-001…012 covered via fixtures + `tests/contract/test_auth_ops_boundaries.py` (15 passed).
- [x] TRACEABILITY story key on AUTH fixtures; Channel ≠ Gateway in default Settings.
- [x] AUTH-009: Channel Bearer absent from 401 body and `/metrics`.
- [x] Package `fixtures/turns-valid-private.json` original intact; copies under `tests/fixtures/`.
- [x] No Railway SUCCESS invented.

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/contract/test_auth_ops_boundaries.py -q --noconftest → 15 passed
test -f docs/tasks/.../fixtures/turns-valid-private.json
test -f tests/fixtures/channel/turns-valid-private.json
```
