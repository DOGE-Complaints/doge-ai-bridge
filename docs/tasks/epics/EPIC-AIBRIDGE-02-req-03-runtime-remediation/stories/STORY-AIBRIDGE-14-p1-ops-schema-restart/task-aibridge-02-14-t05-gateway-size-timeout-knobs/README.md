# Task: implement — gateway response-size + remaining §17 timeout knobs

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md`  
**Parent story:** [`STORY-AIBRIDGE-14-p1-ops-schema-restart.md`](../STORY-AIBRIDGE-14-p1-ops-schema-restart.md)  
**P1 scaffold:** 2026-09-13T17:03:24Z  
**Maps:** Scope #5 · R3-P1-06

## Purpose

Close R3-P1-06: gateway response-size limit and any remaining REQ-01 §17 timeout knobs for ops hardness (beyond story-12 «when set» wiring).

## Code Facts (verified exists — P1)

1. `GatewayExecutor.max_response_bytes` enforced when set (`gateway.py`).
2. HTTP connect/total / OpenAI timeout Settings fields accepted; wired in story 12 (`config.py`, `responses_client.py`, audit tests).
3. Gap for this story: finish remaining §17 knobs + harden defaults/evidence so P1-06 is closed (not only «optional when set»).

## AC/DoD

- [x] Gateway oversize responses fail closed with tested outcome.
- [x] Remaining §17 timeout knobs accepted, documented in `.env.example`, and enforced with tests.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/gateway.py`, `config.py`, `responses_client.py`, `.env.example`, `tests/`.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "max_response or timeout or story_14" --maxfail=10
```
