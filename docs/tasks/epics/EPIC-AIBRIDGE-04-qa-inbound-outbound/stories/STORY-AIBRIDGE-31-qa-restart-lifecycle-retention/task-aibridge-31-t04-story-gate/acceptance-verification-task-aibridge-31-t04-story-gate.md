# Acceptance verification — task-aibridge-31-t04-story-gate

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-17T20:12:21Z |
| **Story** | STORY-AIBRIDGE-31-qa-restart-lifecycle-retention |
| **Pkg** | pkg-000028 |
| **Wave** | P3 Execute |

## AC check

- [x] Every LIFE-001…012 covered by fixtures + `tests/integration/test_lifecycle_retention.py`.
- [x] LIFE-009/010 marked characterization — capture-first; no silent product invent.
- [x] Package originals hash_eq vs copies; originals intact (promote=copy).
- [x] No live Telegram / Railway SUCCESS invent / silent product invent.
- [x] Memory/fake-clock/GC + MemConfirmSessions restart seams (disposable PG absent → Preference A).

## Evidence

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/integration/test_lifecycle_retention.py -q
→ 13 passed

DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/integration/ -q -k 'life or lifecycle or restart or retention or ttl or gc'
→ 14 passed, 60 deselected

hash_eq: 13 LIFE envelopes package ↔ tests/fixtures/{settings,channel,spies}/
```
