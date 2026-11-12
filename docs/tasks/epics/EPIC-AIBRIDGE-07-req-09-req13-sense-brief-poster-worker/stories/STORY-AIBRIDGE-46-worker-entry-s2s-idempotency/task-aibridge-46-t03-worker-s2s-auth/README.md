# Task: auth — dedicated worker S2S

**Status:** Done · 2026-10-14T12:02:26Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md`  
**Parent story:** [`STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md`](../STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md)  
**P1 scaffold:** 2026-10-14T11:54:36Z  
**Maps:** T03 · DP3

## Purpose

Validate dedicated worker S2S on accept; reject channel Bearer and citizen credentials. Do not reuse `channel_bearer_middleware` as worker auth. Outbound gateway service token remains a separate direction.

## AC/DoD

- [x] Channel Bearer → unauthorized on accept.
- [x] Valid worker S2S → admitted (pipeline may still fail later).
- [x] Citizen creds rejected.
- [x] `channel_bearer_middleware` not reused as worker auth.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved — do **not** invent path/env/JSON SSOT.

## Where to change (P3)

- Auth near `config.py` / dedicated middleware or dependency — **not** channel Bearer middleware (~542+).

**Open / name≠create:** header / token env names remain Open.


## Implement names (chosen P3; were Open)

| Kind | Value |
|------|-------|
| Path | `POST /v1/worker/sense-brief/accept` |
| Prefix | `/v1/worker/` |
| Env enable | `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED` |
| Env S2S | `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` |
| JSON | `issue_id`, `generation_version`, optional `corpus` |

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-46-t03-worker-s2s-auth.md` (create at P3 close)
