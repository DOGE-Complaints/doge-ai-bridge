# Acceptance verification — task-aibridge-24-t05-audit-g01-negative-content-length

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T14:44:12Z |
| **Story** | STORY-AIBRIDGE-24-qa-json-schema-boundary |
| **Gap** | G-01 (Medium) |
| **Wave** | `run_mode=aibridge_24_audit_20260917` |
| **Pkg** | pkg-000021 (YAML default unchanged) |

## AC check

- [x] Negative Content-Length rejected with HTTP 400 `bad_request` before body parse.
- [x] Non-integer Content-Length still 400 `bad_request`.
- [x] Fixture + contract assert cover negative branch (`val-negative-content-length`; promote=copy).
- [x] `Skill declared: python-pro` present.

## Evidence

```text
rg: length < 0 + Invalid Content-Length in BodySizeLimitMiddleware
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/contract/test_json_schema_boundary.py -q --noconftest → 21 passed
```
