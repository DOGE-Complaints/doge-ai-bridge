# Acceptance verification — task-aibridge-34-t06-audit-g04-uc07-restart-ambiguity

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T21:35:04Z |
| **Story** | STORY-AIBRIDGE-34-qa-product-journey-scenarios |
| **Gap** | G-04 |
| **Wave** | `run_mode=aibridge_34_audit_20260917` |

## AC check

- [x] `rebuild_app_same_pg` preserves `unknown_outcome` / `send_blocked_for_revision`.
- [x] No automatic gateway calls after restart (`transport.calls == []`).
- [x] Runbook assert: `docs/runtime-docs/01-api.md` contains `unknown_outcome`.
- [x] No live Telegram / Railway SUCCESS invent / silent product invent.

## Evidence

```text
.venv/bin/pytest tests/integration/test_product_journey_scenarios.py::test_uc_07_ambiguous_gateway_timeout -q
→ passed (in full suite 11 passed)
```
