# Acceptance verification — task-aibridge-27-t05-audit-g01-oai009-channel-depth

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T18:54:18Z |
| **Gap** | G-01 Medium |
| **Wave** | P6 · `run_mode=aibridge_27_audit_20260917` |

## AC

- [x] ASGI `/turns` 5xx/raise → 500 `internal_error` retryable (characterization)
- [x] gw=[] · forbid secrets · dedupe abort
- [x] transport TRANSIENT_FAILURE retained

## Evidence

```text
.venv/bin/pytest tests/integration/test_openai_prompt_behavior.py -q
→ 18 passed
```
