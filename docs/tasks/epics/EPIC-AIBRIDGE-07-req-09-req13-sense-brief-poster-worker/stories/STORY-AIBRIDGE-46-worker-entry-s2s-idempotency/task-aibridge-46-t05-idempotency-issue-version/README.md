# Task: idempotency — Issue + generation-version

**Status:** Done · 2026-10-14T12:02:26Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md`  
**Parent story:** [`STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md`](../STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md)  
**P1 scaffold:** 2026-10-14T11:54:36Z  
**Maps:** T05 · DP5 · AC-09-06

## Purpose

Same Issue id + generation-version as in-flight/completed → no-op / equivalent outcome; no required second full LLM+image spend. New version after regenerate bump → new work allowed. Sweep re-nudge same version must be safe.

## AC/DoD

- [x] Duplicate same version does not imply second successful bind with a new version.
- [x] New version allows new work.
- [x] Bind client (49) **not** implemented here.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved — do **not** invent path/env/JSON SSOT.

## Where to change (P3)

- Local idempotency handling in worker (mechanism Open); not gateway version SSOT.

**Open / name≠create:** local storage mechanism for idempotency may be chosen in P3 without inventing gateway wire SSOT.


## Implement names (chosen P3; were Open)

| Kind | Value |
|------|-------|
| Path | `POST /v1/worker/sense-brief/accept` |
| Prefix | `/v1/worker/` |
| Env enable | `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED` |
| Env S2S | `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` |
| JSON | `issue_id`, `generation_version`, optional `corpus` |

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-46-t05-idempotency-issue-version.md` (create at P3 close)
