# Task: test — middleware vs OpenAI rate_limited discriminator (G-02)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_38_audit_20260918`  
**Gap:** G-02 (Low) — P4 audit 2026-09-18  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-38-qa-oai-channel-error-outcome-20260918.md`  
**Parent story:** [`STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md`](../STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md)  
**P5 scaffold:** 2026-09-18T13:53:25Z  
**Maps:** OAI-008 · CHAR-006 · middleware RL · gaps §38

## Purpose

Assert OpenAI transport vs client middleware `rate_limited` discriminator (e.g. message `OpenAI rate limited` vs `Rate limit exceeded`) in OAI suite — **or** soften TRACEABILITY wording. Suite/docs only; no invent gateway.

**Out of this task:** guide §10.5 (t05); ASGI Production wire (t07); invent OAS; product invent beyond assert.

## AC/DoD

- [x] Suite asserts distinct OpenAI vs middleware RL message/cause **or** TRACEABILITY softened.
- [x] Existing Option A 429 channel asserts remain green.
- [x] No invent gateway / live TG.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/integration/test_openai_prompt_behavior.py` — **P6**
- optional: package/ops TRACEABILITY — **P6**
