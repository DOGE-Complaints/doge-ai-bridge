# Task: implement — Edit/Cancel invalidate + ownership

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-04-dual-confirm-tokens.md`  
**Parent story:** [`STORY-AIBRIDGE-04-dual-confirm-tokens.md`](../STORY-AIBRIDGE-04-dual-confirm-tokens.md)

## Purpose

Content edit increments revision and invalidates prior Send tokens. Cancel cancels session/tokens. Ownership checks on consume / `/v1/channel/actions`.

**Out of this task:** gateway stash HTTP (05).

## Code Facts (verified exists)

1. Arch: Edit invalidates; Cancel cancels — `03-confirm-gateway.md` §2.
2. Channel action stub ignores ownership — `channel.py`.
3. Session store from story 02 available for pin/session id.

## AC/DoD

- [ ] Content edit increments revision and invalidates prior Send tokens (AC #4).
- [ ] Cancel cancels; prior tokens unusable.
- [ ] Foreign principal / ownership mismatch rejected.
- [ ] `Skill declared: python-pro` present.

## Where to change

- Token store + FSM integration; channel action consume path.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# edit → old Send rejected; foreign principal rejected
```
