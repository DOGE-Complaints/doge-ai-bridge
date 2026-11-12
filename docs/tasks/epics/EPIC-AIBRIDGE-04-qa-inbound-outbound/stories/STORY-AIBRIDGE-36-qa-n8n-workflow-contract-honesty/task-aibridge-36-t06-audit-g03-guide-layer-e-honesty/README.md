# Task: docs — guide Layer E adapter-contract honesty (G-03)

**Status:** Done · 2026-09-18T12:42:35Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_36_audit_20260918`  
**Gap:** G-03 (Medium) — P4 audit 2026-09-18  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty-20260918.md`  
**Parent story:** [`STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md`](../STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md)  
**P5 scaffold:** 2026-09-18T12:40:26Z
**P6 closed:** 2026-09-18T12:42:35Z  
**Maps:** Layer E · guide § n8n · TECH §5.1 · N8N-WF-001

## Purpose

Relabel parent guide `AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md` Layer E (section still titled «n8n contract tests») to match package TECH §5.1: `tests/n8n/` = **adapter-contract** (fixture + Python helpers; **not** live workflow e2e / Bot API). Add pointer to STORY-36 / N8N-WF-001 for runtime pin + out-of-CI smoke. Docs-only.

**Out of this task:** ops TRACEABILITY (t05); fixture-index stats (t07); invent export; live TG; Railway; product code.

## AC/DoD

- [x] Guide Layer E wording = adapter-contract honesty aligned with TECH §5.1.
- [x] Explicit pointer to STORY-36 / N8N-WF-001 (runtime pin / out-of-CI).
- [x] No invent export / live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/docs/tasks/qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md` — **P6**
- cross-check: package `TECHNICAL-ARCHITECTURE.md` §5.1 — **P6** (read)
