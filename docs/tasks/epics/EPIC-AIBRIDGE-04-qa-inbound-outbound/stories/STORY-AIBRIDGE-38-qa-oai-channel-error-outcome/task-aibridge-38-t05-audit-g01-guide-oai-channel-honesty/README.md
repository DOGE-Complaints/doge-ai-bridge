# Task: docs — guide §10.5 OAI-008/009 Option A honesty (G-01)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_38_audit_20260918`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-18  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-38-qa-oai-channel-error-outcome-20260918.md`  
**Parent story:** [`STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md`](../STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md)  
**P5 scaffold:** 2026-09-18T13:53:25Z  
**Maps:** OAI-008 · OAI-009 · CHAR-006 · guide §10.5 · gaps §38

## Purpose

Relabel parent guide §10.5 OAI-008/009 Expected from «Bounded internal channel error under current implementation» to CHAR-006 Option A channel codes (**429** `rate_limited` / **503** `transient_failure`) **or** explicit «superseded by STORY-38 / CHAR-006». Docs-only.

**Out of this task:** middleware RL assert (t06); ASGI Production wire (t07); invent OAS fields; invent gateway; product code.

## AC/DoD

- [x] Guide §10.5 OAI-008/009 aligned with Option A (or superseded note → STORY-38).
- [x] No invent OAS / gateway / live TG.
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/docs/tasks/qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md` §10.5 — **P6**
