# Task: test — E2E Send confirmation + dry-run/fake gateway stash (AC #5–#6)

**Status:** Done  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md`  
**Parent story:** [`STORY-AIBRIDGE-13-wave1-asgi-e2e.md`](../STORY-AIBRIDGE-13-wave1-asgi-e2e.md)  
**P1 scaffold:** 2026-09-13T16:34:47Z  
**Maps:** REQ-03 §4 AC #5–#6; Target #3

## Purpose

ASGI E2E: Send confirmation consumes token atomically, ≤1 local gateway attempt with frozen body; fake/dry-run 201 returns `stashed`/`draft_id`/`continuation_url` when applicable; `function_call_output` with original `call_id`; final reply does not claim Story publication; **zero real** `POST /story-drafts`.

## Code Facts (verified exists — P1)

1. Send / commit-before-HTTPS unit path — story 11 tests + gateway wiring.
2. Dry-run readiness gate — story 12 (`AIBRIDGE_DRY_RUN`).
3. No wave-1 E2E proof that fake stash path satisfies AC #5–#6 with zero real gateway.

## AC/DoD

- [x] E2E Send path asserts token consume + single fake/dry-run attempt + frozen body.
- [x] Valid fake/dry-run 201 → stashed fields + `function_call_output` with original `call_id`; no publication claim in resident reply.
- [x] Assert harness/gateway fake never hits real Dogestonia stash URL (or records zero real POSTs).
- [x] `Skill declared: test-master` present.

## Where to change

`tests/` E2E module(s); gateway fake/dry-run injection via t01.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "story_13 and (send or dryrun or stash)" --maxfail=5
```
