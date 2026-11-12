# Task: implement — ASGI E2E harness (disposable PG + fake OpenAI + dry-run/fake gateway)

**Status:** Done  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md`  
**Parent story:** [`STORY-AIBRIDGE-13-wave1-asgi-e2e.md`](../STORY-AIBRIDGE-13-wave1-asgi-e2e.md)  
**P1 scaffold:** 2026-09-13T16:34:47Z  
**Maps:** Scope #1 harness

## Purpose

Shared ASGI test harness: real disposable Postgres, fake/recording OpenAI Responses client, fake or dry-run gateway transport — no real `POST /story-drafts`.

## Code Facts (verified exists — P1)

1. Disposable PG script — `scripts/start-disposable-pg.sh`.
2. Existing PG-gated tests — `tests/test_app_pg_runtime_wire.py`, `tests/test_story_11_coordinator.py` (`_pg_available`).
3. Fake/recording Responses patterns — story 10/11 unit tests (not full wave-1 E2E module).

## AC/DoD

- [x] Pytest fixtures/helpers start ASGI app against disposable Postgres with injected fake OpenAI + fake/dry-run gateway.
- [x] Harness documents how to skip when PG unavailable (same convention as existing PG tests).
- [x] Zero real gateway HTTPS stash from harness defaults.
- [x] `Skill declared: test-master` present.

## Where to change

`tests/` (conftest/helpers or `tests/e2e/`), optionally thin wiring in app factory for test DI only.

## Verification commands

```bash
cd doge-ai-bridge && ./scripts/start-disposable-pg.sh
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "e2e_harness or story_13" --maxfail=5
```
