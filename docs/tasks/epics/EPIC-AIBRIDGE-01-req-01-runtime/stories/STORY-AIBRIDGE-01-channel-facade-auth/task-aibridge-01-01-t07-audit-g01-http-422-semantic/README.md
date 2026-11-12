# Task: fix — map semantic channel validation to HTTP 422 (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_01_audit_20260912`  
**Gap:** G-01 (Low) — P4 audit 2026-09-12  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-01-channel-facade-auth-20260912.md`  
**Parent story:** [`STORY-AIBRIDGE-01-channel-facade-auth.md`](../STORY-AIBRIDGE-01-channel-facade-auth.md)  
**P5 scaffold:** 2026-09-12T20:41:08Z  
**P6 Done:** 2026-09-12T20:43:28Z

## Purpose

Align semantic validation HTTP status with OAS / REQ-01 AIB-CH-05: semantic invalid channel input → **422**. Keep **400** for malformed JSON / unknown field when that split is required. Extend channel tests; refresh t05/t06 evidence after live pytest in P6.

**Out of this task:** full AIB-CH-05 matrix (403/404/409/429/500); persistent multi-instance dedupe; Stories 02–06; reopening story AC as failed (residual Low only).

## Code Facts (verified exists — post P6)

1. `parse_channel_body` + `validation_http_status` in `src/aibridge/app.py` — `extra_forbidden` → 400; other ValidationError → 422.
2. OAS lists `"422"` — `docs/openapi/aibridge-channel-v1.openapi.yaml`.
3. Tests: `tests/test_channel.py` (`test_unknown_field_rejected_400`, `test_malformed_json_400`, `test_non_decimal_user_id_rejected_422`, `test_action_token_max_length_422`).

## AC/DoD

- [x] Semantic invalid input → **HTTP 422** with redacted error envelope.
- [x] Malformed JSON and unknown field → **400**.
- [x] `tests/test_channel.py` updated; live pytest green (22 passed @ 2026-09-12T20:43:28Z).
- [x] Evidence in acceptance-verification + run-summary; gate Date from live run.
- [x] `Skill declared: python-pro` present.

## Where to change

- `doge-ai-bridge/src/aibridge/app.py`
- `doge-ai-bridge/tests/test_channel.py`

## Verification commands (P6)

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_channel.py
rg -n '422' doge-ai-bridge/src/aibridge
```
