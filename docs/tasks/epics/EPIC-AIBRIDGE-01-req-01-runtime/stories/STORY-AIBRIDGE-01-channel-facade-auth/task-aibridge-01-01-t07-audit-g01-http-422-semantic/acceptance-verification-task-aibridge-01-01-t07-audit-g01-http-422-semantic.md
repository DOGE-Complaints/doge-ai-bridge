# Acceptance verification — task-aibridge-01-01-t07-audit-g01-http-422-semantic

- **Result:** PASS
- **Date:** 2026-09-12T20:43:28Z
- **Gap:** G-01
- **Wave:** `run_mode=aibridge_01_audit_20260912`
- **Evidence:** `cd doge-ai-bridge && .venv/bin/pytest -q` → **22 passed**
- **Code:** `src/aibridge/app.py` (`parse_channel_body`, `validation_http_status`); `tests/test_channel.py`

## AC check

- [x] Semantic → 422 (`test_non_decimal_user_id_rejected_422`, `test_action_token_max_length_422`)
- [x] Unknown field / malformed JSON → 400
- [x] `rg 422` hits `src/aibridge/app.py`
