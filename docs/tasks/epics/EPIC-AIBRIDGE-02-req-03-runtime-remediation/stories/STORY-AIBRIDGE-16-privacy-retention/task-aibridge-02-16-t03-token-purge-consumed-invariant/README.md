# Task: implement — purge expired tokens; consumed token stays unusable

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-16-privacy-retention.md`  
**Parent story:** [`STORY-AIBRIDGE-16-privacy-retention.md`](../STORY-AIBRIDGE-16-privacy-retention.md)  
**P1 scaffold:** 2026-09-13T17:43:00Z
**P3 Done:** 2026-09-13T17:49:14Z  
**Maps:** Scope #2 (tokens) · Scope #4 · Target #2

## Purpose

Purge expired action tokens per audit policy, and prove deletion/expiry **never** makes an already consumed action token usable again (tombstone OK).

## Code Facts (verified exists — P1)

1. `pg_runtime.py` — token `expires_at`; `TokenConflictError("Token expired")` on stale lookup.
2. Consume / fail-closed facets covered in story 11/13 tests (wrong owner, second consume).
3. Dedicated retention purge of expired tokens + tombstone after session delete: **Unknown** at P1.

## AC/DoD

- [x] Expired action tokens purged (or equivalent audit-policy retention) with test evidence.
- [x] After delete/expiry, a previously **consumed** token remains non-usable (Target #2).
- [x] Minimized non-PII tombstone may remain for audit window (coordinate with t05).
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/pg_runtime.py` (and related token stores), tests.

## Verification commands

```bash
rg -n "TokenConflictError|expires_at|consumed|tombstone" doge-ai-bridge/src/aibridge doge-ai-bridge/tests --glob '*.py' | head -40
cd doge-ai-bridge && python -m pytest tests/ -q -k 'token or consumed or story_16' --tb=short
```

## Out of scope

Inventing channel `/actions` schema changes; operator delete HTTP path invent (t04).
