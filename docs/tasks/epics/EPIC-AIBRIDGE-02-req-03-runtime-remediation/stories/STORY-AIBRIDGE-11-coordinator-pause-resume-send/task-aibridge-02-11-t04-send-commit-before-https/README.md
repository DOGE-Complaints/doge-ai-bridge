# Task: implement — Send checks + commit-before-HTTPS txn

**Status:** Done  
**Skill declared:** fastapi-expert  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`  
**Parent story:** [`STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`](../STORY-AIBRIDGE-11-coordinator-pause-resume-send.md)  
**P1 scaffold:** 2026-09-13T15:55:55Z
**P3 Done:** 2026-09-13T16:03:23Z  
**Maps:** Scope #4; REQ-03 §4 AC #5 + no PG lock across HTTPS

## Purpose

Send confirmation validates owner/chat/session/deployment/revision/hash/expiry/state; atomically consumes token + transitions to `executing` + creates gateway-attempt **committed before** external HTTPS; stores outcome in a **separate** transaction; uses frozen body only; ≤ one attempt per authorized revision.

## Code Facts (verified exists — P1)

1. Commit-before-HTTPS helper present — `src/aibridge/confirm.py` `call_gateway` calls `gateway_attempts.create_executing` then HTTPS then `set_outcome`.
2. Unique attempt constraint — `src/aibridge/pg_runtime.py` `GatewayAttemptStore.create_executing` unique `(session_id, revision)`.
3. REQ-03 §5.3 forbids open PG txn/lock across HTTPS — `docs/requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md` §5.3.

## AC/DoD

- [x] Send path enforces owner/chat/session/deployment/revision/hash/expiry/state checks (REQ-03 §4 #5).
- [x] Token consume + `executing` + gateway-attempt commit before HTTPS; outcome separate txn; frozen body only; ≤ one attempt/revision.
- [x] No PostgreSQL txn/session lock held across gateway HTTPS.
- [x] `Skill declared: fastapi-expert` present.

## Where to change

`src/aibridge/confirm.py`, `gateway.py`, `pg_runtime.py`

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "send or gateway_attempt or commit" --maxfail=5
```
