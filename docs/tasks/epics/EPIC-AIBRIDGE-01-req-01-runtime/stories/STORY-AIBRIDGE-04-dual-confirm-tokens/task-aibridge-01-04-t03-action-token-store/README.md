# Task: implement — opaque action token mint + hash store

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-04-dual-confirm-tokens.md`  
**Parent story:** [`STORY-AIBRIDGE-04-dual-confirm-tokens.md`](../STORY-AIBRIDGE-04-dual-confirm-tokens.md)

## Purpose

Mint opaque action tokens ≤64 UTF-8 bytes (Telegram `callback_data`); store hash only; bind principal / session / revision / expiry / action; raw token once in channel callback shape.

**Out of this task:** inventing n8n workflow JSON export body.

## Code Facts (verified exists)

1. Channel schema `action_token` `max_length=64` — `src/aibridge/schemas.py`.
2. Arch token rules — `03-confirm-gateway.md` §2 (pilot TTL 15 minutes).
3. No token store module yet.

## AC/DoD

- [ ] Callback / minted token ≤64 UTF-8 bytes (AC #3).
- [ ] Store hash only (raw not persisted).
- [ ] Bind principal, session, revision, expiry, action (and deployment as required by arch).
- [ ] `Skill declared: python-pro` present.

## Where to change

- New token store module under `src/aibridge/`.
- Config for TTL if needed (do not invent beyond arch pilot 15m without note).

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# length, hash-not-raw, bind fields
```
