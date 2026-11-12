# Task: implement — wire ops session-delete CLI to Postgres (G-02)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_16_audit_20260913`  
**Gap:** G-02 (Medium) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-16-privacy-retention-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-16-privacy-retention.md`](../STORY-AIBRIDGE-16-privacy-retention.md)  
**P5 scaffold:** 2026-09-13T17:52:16Z
**P6 Done:** 2026-09-13T17:55:59Z  
**Maps:** R3-P1-10 ops delete · Target #3

## Purpose

Make `python -m aibridge.ops_session_delete` execute against live `DATABASE_URL` stores (history/tokens/confirm/session) when Postgres is configured; keep fail-closed ops bearer; **no** channel OAS invent.

## AC/DoD

- [x] CLI attaches PG history/tokens/confirm/session when `DATABASE_URL` is Postgres.
- [x] Without DATABASE_URL / non-PG: still fail-closed on authz; clear error if stores unavailable for delete.
- [x] Disposable-PG integration test (or skip with reason).
- [x] `Skill declared: python-pro` present.

## Where to change

`ops_session_delete.py`, `privacy_retention.py` (if needed), `tests/test_story_16_audit_gaps.py`, privacy-pilot note.

## Verification commands

```bash
cd doge-ai-bridge && ./scripts/start-disposable-pg.sh
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_story_16_audit_gaps.py -k ops_cli --tb=short
```
