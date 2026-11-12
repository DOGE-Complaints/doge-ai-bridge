# Task: audit G-03 — channel==worker S2S rejection test

**Status:** Done · 2026-10-14T12:33:45Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md`  
**Parent story:** [`STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md`](../STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md)  
**P5 scaffold:** 2026-10-14T12:25:32Z · [p5 draft](../../../../../../../../.cursor/plans/p5_aibridge_46_gap_20261014T122159Z.plan.md)  
**Maps:** P4 G-03 · Info

## Purpose

Add dedicated unit/integration test: when Authorization Bearer equals channel token **and** worker S2S is the same string (misconfig), accept still **401** (`is_worker_s2s_authorized` rejects channel set first). Logic already Present in `auth.py`.

## AC/DoD

- [x] Test in `tests/test_worker_accept_story_46.py` (or sibling) asserts channel==worker → 401 on accept.
- [x] Existing 10-pass suite still green (+ new case).
- [x] `Skill declared: python-pro` present.
- [x] No durable idempotency store / brief/poster/bind invent.

## Where to change (P6)

- `tests/test_worker_accept_story_46.py`
- Read-only cite: `src/aibridge/auth.py` `is_worker_s2s_authorized`

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-46-t09-audit-g03-channel-eq-worker-test.md`](./acceptance-verification-task-aibridge-46-t09-audit-g03-channel-eq-worker-test.md)
