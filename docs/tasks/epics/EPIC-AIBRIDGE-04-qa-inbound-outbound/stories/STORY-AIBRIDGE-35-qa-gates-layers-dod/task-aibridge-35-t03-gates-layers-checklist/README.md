# Task: test — gates/layers + CHAR checklist

**Status:** Done  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-35-qa-gates-layers-dod.md`  
**Parent story:** [`STORY-AIBRIDGE-35-qa-gates-layers-dod.md`](../STORY-AIBRIDGE-35-qa-gates-layers-dod.md)  
**P1 scaffold:** 2026-09-17T21:40:06Z  
**P3 close:** 2026-09-17T21:45:30Z  
**Maps:** Gate-1…5 · CHAR-001…008 · Layers A–F · guide §9/§15/§16

## Purpose

Implement Gate-1…5 + CHAR-001…008 capture/defer checklist; assert required layer directories present (unit/contract/integration/n8n as required). Gate-5 / Layer F live pilot **out of default CI** (flag-gated / documented defer). Characterization capture-first — **no** silent product invent. No live Telegram / Railway SUCCESS invent.

## AC/DoD

- [x] Checklist/suite asserts Gate-1…5 must-rows (or explicit defer for Gate-5 live).
- [x] CHAR-001…008 marked characterization / deferred with reason (capture-first).
- [x] Layer dirs present as required by TECH §5.1 / guide §9.
- [x] No live Telegram / Railway SUCCESS invent / silent product invent.
- [x] `Skill declared: python-pro` present.

## Verification commands (P3)

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/ -q -k 'gate or layer or char or dod or fixture_index'
```

## Where to change

- `doge-ai-bridge/tests/` (checklist / meta asserts) — **P3**
