# Acceptance verification — task-aibridge-25-t06-audit-g02-one-reply-assert

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T17:53:25Z |
| **Story** | STORY-AIBRIDGE-25-qa-n8n-telegram-mapping |
| **Gap** | G-02 (Low) |
| **Wave** | `run_mode=aibridge_25_audit_20260917` |
| **Pkg** | pkg-000022 (YAML default unchanged) |

## AC check

- [x] N8N-001 `map-private-text` asserts `one_reply` and single `SendOrEditMessage` in `ack_order`.
- [x] Existing mapping equality asserts remain.
- [x] Suite passes (`DATABASE_URL=memory` + `--noconftest`).
- [x] `Skill declared: test-master` present.

## Evidence

```text
rg: one_reply + SendOrEditMessage count on map-private-text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/n8n/ -q --noconftest → 19 passed
```
