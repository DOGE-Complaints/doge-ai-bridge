# Task: implement — wire expire_idle + durable TTL on confirm path (G-01)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_16_audit_20260913`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-16-privacy-retention-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-16-privacy-retention.md`](../STORY-AIBRIDGE-16-privacy-retention.md)  
**P5 scaffold:** 2026-09-13T17:52:16Z
**P6 Done:** 2026-09-13T17:55:59Z  
**Maps:** R3-P1-10 TTL expiry · narrative minimize · token purge

## Purpose

Call `expire_idle_session_narrative` (minimize + purge/invalidate) when session TTL elapses on the confirm/ASGI path; use durable `confirm_session.updated_at` (not process-local clock alone) so restart cannot resurrect idle narrative.

## AC/DoD

- [x] Idle expiry minimizes history and invalidates/purges pending tokens (not only pop in-memory maps).
- [x] PG hydrate refuses expired sessions based on durable `updated_at` + TTL.
- [x] Tests cover in-memory path; disposable-PG when available.
- [x] `Skill declared: python-pro` present.

## Where to change

`confirm.py`, `privacy_retention.py`, `pg_runtime.py` (confirm updated_at / token purge), `app.py`, `tests/test_story_16_audit_gaps.py`.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_story_16_audit_gaps.py tests/test_story_16_privacy_retention.py --tb=short
```
