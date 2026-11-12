# Task: test — implement restart / lifecycle / retention suite

**Status:** Done  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md`  
**Parent story:** [`STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md`](../STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md)  
**P1 scaffold:** 2026-09-17T20:05:23Z  
**Maps:** LIFE-001…012 · layer `tests/integration/`

## Purpose

Lifecycle tests via disposable PG + `rebuild_app_same_pg` (+ fake clock for TTL): shutting_down 503; restart restore without duplicate side effects; pending/consumed tokens; open gateway→unknown; session TTL; bundle GC retain vs eligible; LIFE-009/010 characterization capture-first; edit from unknown_outcome; deployment mismatch. No live Telegram. Guide must-rows → automated asserts; no silent product invent.

## AC/DoD

- [x] Suite under `tests/integration/` asserts LIFE-001…012 must-rows.
- [x] LIFE-009/010 marked characterization — capture-first; no silent invent.
- [x] No live Telegram / Railway invent.
- [x] No silent product invent for LIFE-*.
- [x] `Skill declared: python-pro` present.

## Verification commands (P3)

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/integration/ -q -k 'life or lifecycle or restart or retention or ttl or gc'
```

## Where to change

- `doge-ai-bridge/tests/integration/` — **P3**
- Surfaces: `story13_e2e_helpers.rebuild_app_same_pg` · `privacy_retention` · `app.py` shutting_down (assert only; no product invent in P1)
