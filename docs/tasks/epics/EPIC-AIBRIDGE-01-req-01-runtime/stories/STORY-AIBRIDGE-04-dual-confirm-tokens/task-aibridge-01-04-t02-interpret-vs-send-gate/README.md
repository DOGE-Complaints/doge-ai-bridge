# Task: implement — interpretation ≠ Send; tool intent ≠ permission

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-04-dual-confirm-tokens.md`  
**Parent story:** [`STORY-AIBRIDGE-04-dual-confirm-tokens.md`](../STORY-AIBRIDGE-04-dual-confirm-tokens.md)

## Purpose

Interpretation confirm never authorizes gateway HTTPS. Only Send may authorize the gateway call site (stub until story 05). Tool/`function_call` intent alone never equals Send permission (arch §3).

**Out of this task:** actual `POST /story-drafts` HTTP (05).

## Code Facts (verified exists)

1. Arch dual-confirm table — `03-confirm-gateway.md` §1, §3.
2. `InterviewEngine.call_gateway` stub exists (story 03) — must remain gated.
3. Three validation gates (story 03) freeze intent — not Send permission.

## AC/DoD

- [ ] Interpretation confirm produces no gateway HTTP / no gateway-authorized flag (AC #1).
- [ ] Tool intent alone never equals Send permission (AC #5).
- [ ] Only Send path may set gateway-authorized call site.
- [ ] `Skill declared: python-pro` present.

## Where to change

- Confirm handlers / FSM actions; gate around gateway stub.
- Integrate with token consume for Send only.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# interpretation path: gateway mock not called; tool intent alone: no Send
```
