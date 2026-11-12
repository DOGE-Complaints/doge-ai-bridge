# Task: test — T-UNIQUE / AC-04 uniqueItems proofs

**Status:** Done · P3 2026-09-24T11:17:36Z  

**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md`  
**Parent story:** [`STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md`](../STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md)  
**P1 scaffold:** 2026-09-24T11:13:54Z  
**Maps:** T-UNIQUE-01…09 · AC-04 · REQ §11

## Purpose

Cover T-UNIQUE-01…09 and AC-04: unique arrays pass; duplicates fail at correct path; key-order-independent objects; nested arrays; `false`/absent pass; empty/one-element pass; Uus Veerenni duplicate houses under one street rejected; same house under two streets not conflated. No freeze/Send/gateway invent beyond Gate 2 validation unit/contract tests. No live Telegram.

**Out of this task:** product enforce (t01/t02); story gate (t04); STORY-45 live invent.

## AC/DoD

- [x] T-UNIQUE-01…09 (or mapped equivalents) covered.
- [x] AC-04 duplicate houses under one street → Gate 2 reject evidenced.
- [x] Suite green under filter; no invent live TG / OpenAI network SUCCESS.
- [x] `Skill declared: python-pro` present.

## Where to change (execute — not P1)

- `tests/` (extend existing request_assembly / gate tests and/or dedicated module) — **P3**
