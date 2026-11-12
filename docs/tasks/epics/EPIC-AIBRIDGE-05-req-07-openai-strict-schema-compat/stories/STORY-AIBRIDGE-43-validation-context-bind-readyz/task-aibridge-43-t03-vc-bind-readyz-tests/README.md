# Task: test — VC bind + readyz proofs

**Status:** Done · P3 2026-09-24T11:33:03Z  

**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-43-validation-context-bind-readyz.md`  
**Parent story:** [`STORY-AIBRIDGE-43-validation-context-bind-readyz.md`](../STORY-AIBRIDGE-43-validation-context-bind-readyz.md)  
**P1 scaffold:** 2026-09-24T11:30:36Z  
**P3 closed:** 2026-09-24T11:33:03Z  
**Maps:** AC-06 partial · bind + readyz

## Purpose

Automated proofs:

- Bind present when content configured (dual schemas on guard).
- Unbound/invalid VC → readyz reason (default `validation_context_not_bound`).
- AC-06 partial: no silent accept of consequential FC without schemas when content configured.

**Out of this task:** product bind/readyz impl (t01/t02); story gate (t04); live TG invent.

## AC/DoD

- [x] Tests cover bind-when-configured.
- [x] Tests cover unbound/invalid → not_ready + reason.
- [x] Tests cover no silent FC accept without schemas (AC-06 partial).
- [x] `Skill declared: python-pro` present.

## Where changed

- `tests/test_validation_context_bind.py` — **5** tests
