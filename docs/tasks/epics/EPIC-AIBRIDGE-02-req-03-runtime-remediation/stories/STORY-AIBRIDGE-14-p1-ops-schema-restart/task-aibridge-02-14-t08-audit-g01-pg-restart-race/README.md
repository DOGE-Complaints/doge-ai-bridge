# Task: tests — disposable-PG restart/race Send / pending / unknown (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_14_audit_20260913`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-14-p1-ops-schema-restart-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-14-p1-ops-schema-restart.md`](../STORY-AIBRIDGE-14-p1-ops-schema-restart.md)  
**P5 scaffold:** 2026-09-13T17:18:05Z  
**P6 Done:** 2026-09-13T17:23:30Z  
**Maps:** R3-P1-04 · Target #3 DB facet

## Purpose

Close G-01: prove Send / pending-confirm / `unknown_outcome` restart+race against disposable Postgres (`GatewayAttemptStore` / confirm sessions), not in-memory fakes alone.

## AC/DoD

- [x] Disposable-PG tests: executing → recover → `unknown_outcome` blocks resend (no auto gateway POST).
- [x] Pending-confirm / Send token path survives PG restart or is blocked after unknown (evidence).
- [x] Concurrent duplicate `create_executing` same `(session, revision)` fails closed (unique attempt).
- [x] `Skill declared: python-pro` present.

## Where to change

`tests/test_story_14_audit_gaps.py` (new), reuse `story13_e2e_helpers` / `pg_runtime` as needed.

## Verification commands

```bash
cd doge-ai-bridge && ./scripts/start-disposable-pg.sh
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "story_14_audit or story_14" --maxfail=10
```
