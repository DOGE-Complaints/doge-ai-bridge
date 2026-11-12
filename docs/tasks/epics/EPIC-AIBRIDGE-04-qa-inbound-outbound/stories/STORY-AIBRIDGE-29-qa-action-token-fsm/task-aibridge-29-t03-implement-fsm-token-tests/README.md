# Task: test — implement action-token / dual-confirm FSM suite

**Status:** Done  
**Skill declared:** python-pro  
**Secondary skill:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-29-qa-action-token-fsm.md`  
**Parent story:** [`STORY-AIBRIDGE-29-qa-action-token-fsm.md`](../STORY-AIBRIDGE-29-qa-action-token-fsm.md)  
**P1 scaffold:** 2026-09-17T19:21:48Z  
**Maps:** ACT-001…018 · layers `tests/unit/` + `tests/integration/`

## Purpose

FSM/token tests via create_app + ConfirmationGuard (+ RecordingGatewayTransport): Looks right → interpretation_confirmed · gw=0; Edit/Cancel transitions · siblings invalidated · no gateway; Send → one authorized attempt with frozen body; reject paths 404/403/409; ACT-017 hash-only persist; ACT-018 token >64 → 422; generated tokens ≤64. Fake clock for ACT-008 TTL. No live Telegram. Guide must-rows → automated asserts; no silent product invent.

## AC/DoD

- [x] Suite under `tests/unit/` and/or `tests/integration/` asserts ACT-001…018 must-rows.
- [x] Zero gateway on Looks right / Edit / Cancel.
- [x] No live Telegram / network Telegram API in default CI path.
- [x] No silent product invent for ACT-*.
- [x] `Skill declared: python-pro` present.

## Verification commands (P3)

```text
DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/unit/ tests/integration/ -q -k 'act or token or fsm'
```

## Where to change

- `doge-ai-bridge/tests/unit/` · `doge-ai-bridge/tests/integration/` — **P3**
- Surfaces: `src/aibridge/confirm.py` · `confirm_fsm.py` · channel actions (assert only; no product invent in P1)
