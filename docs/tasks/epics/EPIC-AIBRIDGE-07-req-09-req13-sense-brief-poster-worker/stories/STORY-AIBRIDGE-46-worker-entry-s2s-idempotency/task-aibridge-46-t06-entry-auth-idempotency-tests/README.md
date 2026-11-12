# Task: tests — entry / S2S / idempotency

**Status:** Done · 2026-10-14T12:02:26Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md`  
**Parent story:** [`STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md`](../STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md)  
**P1 scaffold:** 2026-10-14T11:54:36Z  
**Maps:** T06

## Purpose

Unit/integration: channel Bearer rejected; valid S2S admits; same-version idempotent. No live LLM/storage. Full AC-09 harness remains STORY-50.

## AC/DoD

- [x] Tests green for T03–T05 behaviors without live LLM/storage.
- [x] Live vendor smoke **not** required.
- [x] STORY-50 harness **not** claimed Done.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved — do **not** invent path/env/JSON SSOT.

## Where to change (P3)

- `tests/` focused on accept/auth/idempotency (paths as implement chooses).

**Open:** no invent of final route string in assertions as permanent SSOT beyond what P3 chooses locally.


## Implement names (chosen P3; were Open)

| Kind | Value |
|------|-------|
| Path | `POST /v1/worker/sense-brief/accept` |
| Prefix | `/v1/worker/` |
| Env enable | `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED` |
| Env S2S | `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` |
| JSON | `issue_id`, `generation_version`, optional `corpus` |

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-46-t06-entry-auth-idempotency-tests.md` (create at P3 close)
