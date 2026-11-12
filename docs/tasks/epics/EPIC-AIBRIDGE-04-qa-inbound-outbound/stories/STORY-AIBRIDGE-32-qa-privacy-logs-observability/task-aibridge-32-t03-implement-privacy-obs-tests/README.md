# Task: test — implement privacy / logs / observability suite

**Status:** Done  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-32-qa-privacy-logs-observability.md`  
**Parent story:** [`STORY-AIBRIDGE-32-qa-privacy-logs-observability.md`](../STORY-AIBRIDGE-32-qa-privacy-logs-observability.md)  
**P1 scaffold:** 2026-09-17T20:27:34Z  
**P3 closed:** 2026-09-17T20:33:31Z  
**Maps:** SEC-001…010 · layer `tests/integration/`

## Purpose

Privacy/observability tests via spy bag §14 + Recording* captures: narrative absent from audit/metrics; secret redaction; bounded channel audit; `/metrics` scrub; error envelope + `request_id`; token hash-only; OpenAI `store=false` + no secrets; Gateway Bearer only (no Channel); n8n export secret-free; prompt-injection allowlist / server-owned origin. No live Telegram. Guide must-rows → automated asserts; no silent product invent.

## AC/DoD

- [x] Suite under `tests/integration/` asserts SEC-001…010 must-rows.
- [x] No live Telegram / Railway invent.
- [x] No silent product invent for SEC-*.
- [x] `Skill declared: python-pro` present.

## Verification commands (P3)

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/integration/ -q -k 'sec or privacy or observab or metrics or redact'
```

## Where to change

- `doge-ai-bridge/tests/integration/` — **P3**
- Surfaces: audit buffer · metrics · redact · Recording* · token hash store (assert only; no product invent in P1)
