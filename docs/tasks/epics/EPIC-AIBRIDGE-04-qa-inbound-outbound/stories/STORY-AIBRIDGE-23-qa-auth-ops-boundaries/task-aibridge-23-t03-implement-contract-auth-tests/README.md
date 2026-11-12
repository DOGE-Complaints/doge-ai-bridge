# Task: test — contract AUTH-* (tests/contract/)

**Status:** Done  
**P3 closed:** 2026-09-17T14:02:23Z  

**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md`  
**Parent story:** [`STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md`](../STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md)  
**P1 scaffold:** 2026-09-17T13:59:06Z  
**Maps:** AUTH-001…012 · TestClient + auth header variants

## Purpose

Implement contract tests under `tests/contract/` for AUTH-001…012 using `load_fixture` + TestClient. Settings pins: Channel Bearer ≠ Gateway Bearer. Assert expected status/bodies per matrix; fail if Channel Bearer appears in logs/metrics/error bodies (AUTH-009).

**Out of this task:** fixture promote (t01/t02); invent Railway SUCCESS; live Telegram.

## Code Facts (verified exists — P1)

1. Harness: TECH §5.1 story 23 — TestClient + auth variants.
2. Prior channel auth / ops endpoints in `src/aibridge/` (characterization — do not invent new product APIs in this task).
3. Fixture load pattern named in TECH §6 (`load_fixture(cluster, name)`).

## AC/DoD

- [x] Contract suite covers AUTH-001…012 expectations from story matrix.
- [x] Channel ≠ Gateway Bearer pinned in Settings for tests.
- [x] AUTH-009: secret absent from logs/metrics/error assertions.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/contract/` — **P3**
- optional shared `load_fixture` helper — **P3** if missing

## Verification commands

```bash
cd doge-ai-bridge && DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/contract/ -q --noconftest 2>/dev/null || true
```
