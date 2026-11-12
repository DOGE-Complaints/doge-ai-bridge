# Task: test — E2E restart recovery + OpenAPI channel conformance (AC #7–#9)

**Status:** Done  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md`  
**Parent story:** [`STORY-AIBRIDGE-13-wave1-asgi-e2e.md`](../STORY-AIBRIDGE-13-wave1-asgi-e2e.md)  
**P1 scaffold:** 2026-09-13T16:34:47Z  
**Maps:** REQ-03 §4 AC #7–#9; Scope #3

## Purpose

ASGI E2E: restart in pending-confirm preserves buttons/state; restart with unknown gateway delivery does not auto-resend; every success/replay/non-2xx channel response conforms to OpenAPI SSOT; transport replay returns stored status+body without OpenAI/gateway recompute.

## Code Facts (verified exists — P1)

1. OpenAPI SSOT — `docs/openapi/aibridge-channel-v1.openapi.yaml`.
2. Postgres-backed dedupe/session — story 09 product path.
3. Dedicated restart + OpenAPI assert suite for wave-1 E2E not present.

## AC/DoD

- [x] E2E restart pending-confirm preserves confirm UI/state from Postgres.
- [x] E2E unknown_outcome / indeterminate delivery path: no automatic gateway resend after restart.
- [x] Success, replay, and representative non-2xx responses validated against OpenAPI SSOT.
- [x] Replay does not call OpenAI/gateway again (counters/spies).
- [x] `Skill declared: test-master` present.

## Where to change

`tests/` E2E module(s); OpenAPI validation helper if missing.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "story_13 and (restart or openapi or unknown_outcome)" --maxfail=5
```
