# Task: implement — dual-confirm FSM states + transitions

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-04-dual-confirm-tokens.md`  
**Parent story:** [`STORY-AIBRIDGE-04-dual-confirm-tokens.md`](../STORY-AIBRIDGE-04-dual-confirm-tokens.md)

## Purpose

Explicit dual-confirm FSM states and permitted transitions per AIB-CONF-01A / arch `03-confirm-gateway.md` §1.

**Out of this task:** gateway HTTPS executor (05); inventing n8n workflow JSON.

## Code Facts (verified exists)

1. Canonical states described in `docs/architecture/runtime/03-confirm-gateway.md` §1.
2. Channel stub returns `awaiting_confirm` without FSM — `src/aibridge/channel.py`.
3. No FSM module under `src/aibridge/` yet.

## AC/DoD

- [ ] States + permitted transitions match AIB-CONF-01A / arch §1.
- [ ] Illegal transitions rejected (fail closed).
- [ ] `Skill declared: python-pro` present.

## Where to change

- New FSM module under `src/aibridge/` (e.g. `confirm_fsm.py`).
- Session/state persistence seam (story 02 sessions).

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# transition unit tests legal/illegal
```
