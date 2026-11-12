# Task: implement — wire Settings knobs when set (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_12_audit_20260913`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-12-readyz-env-dryrun-gate-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md`](../STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md)  
**P5 scaffold:** 2026-09-13T16:26:12Z
**P6 Done:** 2026-09-13T16:30:46Z  
**Maps:** REQ-03 §5.6 enforceable when set

## Purpose

Settings already **accept** TTL / max response bytes / HTTP timeouts / log level / rate limits / LLM budgets. Wire runtime consumers so non-None env values change behavior (no inventing numeric defaults).

## AC/DoD

- [x] `BudgetGuard`/`BudgetLimits` built from Settings and attached to `InterviewEngine` in `create_app` when any budget field set.
- [x] Action-token TTL uses `AIBRIDGE_ACTION_TOKEN_TTL_SECONDS` when set.
- [x] Gateway / Responses timeouts honor `AIBRIDGE_HTTP_*` / total when set; `AIBRIDGE_MAX_RESPONSE_BYTES` enforced on gateway response body when set.
- [x] `AIBRIDGE_LOG_LEVEL` applied to `aibridge` logger when set.
- [x] Principal/global rate limits enforced when set (429 channel envelope).
- [x] Unit tests prove env values change behavior.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/app.py`, `budgets.py`, `confirm.py` / `action_tokens.py` wiring, `gateway.py`, `responses_client.py` (connect timeout), optional rate helper, `tests/`

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "budget or ttl or timeout or rate_limit or max_response or log_level or story_12" --maxfail=10
```
