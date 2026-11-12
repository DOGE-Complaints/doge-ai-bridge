# Task: test — Send fail-closed ASGI+PG E2E (G-03)

**Status:** Done  
**Skill declared:** test-master  
**Wave:** `run_mode=aibridge_13_audit_20260913`  
**Gap:** G-03 (Info) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-13-wave1-asgi-e2e-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-13-wave1-asgi-e2e.md`](../STORY-AIBRIDGE-13-wave1-asgi-e2e.md)  
**P5 scaffold:** 2026-09-13T16:54:19Z
**P6 Done:** 2026-09-13T16:58:55Z  
**Maps:** REQ-03 §4 #5 fail-closed facets on wave-1 ASGI+PG

## Purpose

Demonstrate on disposable Postgres ASGI: wrong owner / second consume fail closed without gateway HTTPS (complements story-11 unit coverage).

## AC/DoD

- [x] E2E: Send token with wrong `user_id`/`chat_id` → 403 (or mapped fail-closed) · `transport.calls == []`.
- [x] E2E: successful Send then second consume of same token → 409 (or fail-closed) · no second gateway call.
- [x] Document in backlog Verified that remaining §4 #5 facets stay story-11 units if not covered here.
- [x] `Skill declared: test-master` present.

## Where to change

`tests/test_story_13_wave1_asgi_e2e.py` (audit negatives), backlog Verified sync

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "story_13 and (failclosed or wrong_owner or double_consume)" --maxfail=5
```
