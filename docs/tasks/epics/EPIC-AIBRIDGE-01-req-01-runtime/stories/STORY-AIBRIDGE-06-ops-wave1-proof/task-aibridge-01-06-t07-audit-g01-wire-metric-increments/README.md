# Task: implement — wire metric increments (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_06_audit_20260912`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-12  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-06-ops-wave1-proof-20260912.md`  
**Parent story:** [`STORY-AIBRIDGE-06-ops-wave1-proof.md`](../STORY-AIBRIDGE-06-ops-wave1-proof.md)  
**P5 scaffold:** 2026-09-12T22:11:56Z  
**P6 Done:** 2026-09-12T22:14:25Z

## Purpose

Prometheus HELP already advertises `aibridge_openai_calls_total`, `aibridge_gateway_posts_total`, `aibridge_channel_http_errors_total`, but increment helpers are never called. Wire them at real call sites so pilot scrape is not a false zero signal.

## Code Facts (verified exists — post P6)

1. `interview.py` → `get_metrics().inc_openai_calls()` after `client.create`.
2. `gateway.py` → `inc_gateway_posts()` immediately before `transport.request` (not dry-run).
3. `app.py` → outermost middleware counts channel HTTP ≥400 via `inc_http_errors`.
4. Tests — `tests/test_metric_increments.py`.

## AC/DoD

- [x] `inc_openai_calls` invoked on each Responses `create`.
- [x] `inc_gateway_posts` invoked when gateway HTTP POST is attempted.
- [x] `inc_http_errors` invoked on channel-facing HTTP error responses (≥400).
- [x] Unit tests assert counters increase (no narrative in `/metrics`).
- [x] Latency / confirm-state / prompt-cache series **out of scope** this task.
- [x] `Skill declared: python-pro` present.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_metric_increments.py
# full: .venv/bin/pytest -q → 100 passed, 1 skipped
```
