# Task: test — UC-07 restart preserves ambiguity (G-04)

**Status:** Done  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Wave:** `run_mode=aibridge_34_audit_20260917`  
**Gap:** G-04 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-34-qa-product-journey-scenarios-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-34-qa-product-journey-scenarios.md`](../STORY-AIBRIDGE-34-qa-product-journey-scenarios.md)  
**P5 scaffold:** 2026-09-17T21:30:11Z
**P6 closed:** 2026-09-17T21:35:04Z  
**Maps:** UC-07 · restart / unknown_outcome

## Purpose

Guide UC-07: after ambiguous gateway timeout → `unknown_outcome`, restart preserves ambiguity; operator runbook required; no automatic retry. Extend suite with `rebuild_app_same_pg` (or skipif PG) asserting UNKNOWN_OUTCOME persist; add runbook path/string assert **or** mark residual characterization in fixture notes. **No** Railway invent; **no** auto-retry invent; **no** live Telegram.

## AC/DoD

- [x] Restart path preserves `unknown_outcome` / ambiguity (via `rebuild_app_same_pg` or documented skipif).
- [x] Runbook assert **or** fixture notes mark residual characterization (capture-first).
- [x] No automatic second gateway attempt after restart.
- [x] No live Telegram / Railway SUCCESS invent / silent product invent.
- [x] `Skill declared: python-pro` present.

## Where to change

- `tests/integration/test_product_journey_scenarios.py` — **P6**
- `tests/story13_e2e_helpers.py` (`rebuild_app_same_pg`) — assert-only reuse — **P6**
- `tests/fixtures/spies/uc-07-ambiguous-gateway-timeout.json` (+ package promote=copy if notes) — **P6**
