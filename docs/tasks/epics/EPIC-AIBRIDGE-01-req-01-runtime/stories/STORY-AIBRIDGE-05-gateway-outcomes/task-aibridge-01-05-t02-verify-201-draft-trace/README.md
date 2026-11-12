# Task: implement — verify 201 + draft_id + trace_id

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-05-gateway-outcomes.md`  
**P3 Done:** 2026-09-12T21:54:48Z
**Parent story:** [`STORY-AIBRIDGE-05-gateway-outcomes.md`](../STORY-AIBRIDGE-05-gateway-outcomes.md)

## Purpose

Success only on verified **201** + non-empty `draft_id` + `trace_id` per wire OAS; malformed 201 → not `stashed` (AC #3 / AIB-HTTP-03).

**Out of this task:** inventing gateway lookup; SPA E2E.

## Code Facts (verified exists)

1. Wire OAS — `docs/openapi/story-intake-actions.openapi.yaml`.
2. Arch success rule — `03-confirm-gateway.md` §5.
3. FSM has `stashed` / failure states — `confirm_fsm.py`.

## AC/DoD

- [x] Verified 201 + `draft_id` + `trace_id` → may become `stashed`.
- [x] Malformed / incomplete 201 body → not `stashed` (fail closed / mapped outcome).
- [x] Tests cover happy path + malformed 201.
- [x] `Skill declared: python-pro` present.

## Where to change

- Response verifier in executor / outcomes helper.
- Tests with mocked HTTP responses.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# malformed 201 → not stashed
```
