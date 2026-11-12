# Task: test — UC-01 revision assert after Edit (G-03)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_34_audit_20260917`  
**Gap:** G-03 (Low) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-34-qa-product-journey-scenarios-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-34-qa-product-journey-scenarios.md`](../STORY-AIBRIDGE-34-qa-product-journey-scenarios.md)  
**P5 scaffold:** 2026-09-17T21:30:11Z
**P6 closed:** 2026-09-17T21:35:04Z  
**Maps:** UC-01 · revision after Edit

## Purpose

Guide UC-01: revision must change after Edit. Replace tautology `sess2.revision != rev0 or rev0 >= 0` with strict `sess2.revision > rev0` (or ≠) after Edit. Assert-only; **no** product invent; **no** live Telegram / Railway SUCCESS invent.

## AC/DoD

- [x] UC-01 asserts strict revision change after Edit (no tautology OR).
- [x] Fixture expect/notes aligned if needed (promote=copy).
- [x] No live Telegram / Railway SUCCESS invent / silent product invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/integration/test_product_journey_scenarios.py` — **P6**
- `tests/fixtures/spies/uc-01-normal-dry-run.json` (+ package original if notes) — **P6**
