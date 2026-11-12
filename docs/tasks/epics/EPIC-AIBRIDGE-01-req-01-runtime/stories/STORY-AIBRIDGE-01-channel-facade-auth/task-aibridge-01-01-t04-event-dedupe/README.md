# Task: implement — Event dedupe by `(channel, event_id)`

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md`  
**Parent story:** [`STORY-AIBRIDGE-01-channel-facade-auth.md`](../STORY-AIBRIDGE-01-channel-facade-auth.md)

## Purpose

Event dedupe by `(channel, event_id)` returning **stored** response; no second side-effect path.

**Out of this task:** content bundle registry (story 02); full session/interview engine beyond storing channel response for dedupe.

## Code Facts (verified exists)

1. Dedupe requirement — story Scope / AC #3; façade arch `01-channel-facade.md`.
2. Postgres noted for sessions/locks/registry in pilot — `00-overview.md` §3 (if used here: **only** dedupe key; not story-02 registry).
3. Product store path: **Unknown** until t01/t03 scaffold.

## AC/DoD

- [x] Duplicate `event_id` → same stored response — story AC #3.
- [x] No second side-effect path on duplicate.
- [x] `Skill declared: python-pro` present.

## Where to change

- Store + lookup around turns/actions handlers from t03.
- Persistence choice at P3 must not implement story-02 content registry.

## Verification commands

```bash
# After implement: two identical events → equal bodies; side-effect once
```
