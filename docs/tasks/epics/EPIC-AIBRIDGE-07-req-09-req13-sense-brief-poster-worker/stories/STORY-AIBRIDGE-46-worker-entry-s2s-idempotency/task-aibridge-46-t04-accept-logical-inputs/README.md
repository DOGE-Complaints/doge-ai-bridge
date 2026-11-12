# Task: accept — Issue id + generation-version

**Status:** Done · 2026-10-14T12:02:26Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md`  
**Parent story:** [`STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md`](../STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md)  
**P1 scaffold:** 2026-10-14T11:54:36Z  
**Maps:** T04

## Purpose

Parse logical accept: Issue id + generation-version; corpus may passthrough as opaque/stub for later 47. Optional locale hints — shape Open.

## AC/DoD

- [x] Well-formed accept with S2S reaches idempotency gate.
- [x] Brief L2 schema **not** finalized here (47).
- [x] Wire keys **not** invented as SSOT.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved — do **not** invent path/env/JSON SSOT.

## Where to change (P3)

- Accept handler / parser module (exact path Open).

**Open / name≠create:** exact JSON field names remain Open (joint with gateway).


## Implement names (chosen P3; were Open)

| Kind | Value |
|------|-------|
| Path | `POST /v1/worker/sense-brief/accept` |
| Prefix | `/v1/worker/` |
| Env enable | `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED` |
| Env S2S | `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` |
| JSON | `issue_id`, `generation_version`, optional `corpus` |

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-46-t04-accept-logical-inputs.md` (create at P3 close)
