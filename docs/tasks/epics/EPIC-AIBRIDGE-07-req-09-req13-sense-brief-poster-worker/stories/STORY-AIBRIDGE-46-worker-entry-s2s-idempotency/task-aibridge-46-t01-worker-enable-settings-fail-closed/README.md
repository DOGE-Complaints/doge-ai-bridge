# Task: settings — worker enable + S2S fail-closed

**Status:** Done · 2026-10-14T12:02:26Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md`  
**Parent story:** [`STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md`](../STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md)  
**P1 scaffold:** 2026-10-14T11:54:36Z  
**Maps:** T01 · fail-closed

## Purpose

Add settings surface for worker enable + dedicated worker S2S secret near `src/aibridge/config.py`. When worker enabled and S2S (or required peer config) missing/invalid → fail-closed (do not accept).

## AC/DoD

- [x] Worker enable + dedicated S2S settings surface exists.
- [x] Enabled + missing/invalid S2S → no accept / refuse.
- [x] Channel Bearer rename **not** done.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved — do **not** invent path/env/JSON SSOT.

## Where to change (P3)

- Near `src/aibridge/config.py` (and readiness/accept wiring as needed).

**Open / name≠create:** env **names** remain Open (do not invent SSOT).


## Implement names (chosen P3; were Open)

| Kind | Value |
|------|-------|
| Path | `POST /v1/worker/sense-brief/accept` |
| Prefix | `/v1/worker/` |
| Env enable | `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED` |
| Env S2S | `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` |
| JSON | `issue_id`, `generation_version`, optional `corpus` |

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-46-t01-worker-enable-settings-fail-closed.md` (create at P3 close)
