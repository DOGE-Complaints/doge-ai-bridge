# Task: test — UC-03 LIFE-009 post-cancel follow-up (G-02)

**Status:** Done  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Wave:** `run_mode=aibridge_34_audit_20260917`  
**Gap:** G-02 (Medium) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-34-qa-product-journey-scenarios-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-34-qa-product-journey-scenarios.md`](../STORY-AIBRIDGE-34-qa-product-journey-scenarios.md)  
**P5 scaffold:** 2026-09-17T21:30:11Z
**P6 closed:** 2026-09-17T21:35:04Z  
**Maps:** UC-03 · LIFE-009 follow-up

## Purpose

Guide UC-03: after cancel at first confirmation, a following new resident message must be covered by LIFE-009. Wire fixture `expect.life009_followup`; drive post-cancel `/turns` assert (or mark characterization + align fixture notes). Capture-first; **no** product invent; **no** live Telegram / Railway SUCCESS invent.

## AC/DoD

- [x] `life009_followup` from `spies/uc-03-cancel-first-confirm.json` is read and asserted.
- [x] Post-cancel `/turns` (or explicit characterization) covers LIFE-009 handoff.
- [x] No live Telegram / Railway SUCCESS invent / silent product invent.
- [x] `Skill declared: python-pro` present.

## Where to change

- `tests/integration/test_product_journey_scenarios.py` — **P6**
- `tests/fixtures/spies/uc-03-cancel-first-confirm.json` (+ package original promote=copy if notes change) — **P6**
