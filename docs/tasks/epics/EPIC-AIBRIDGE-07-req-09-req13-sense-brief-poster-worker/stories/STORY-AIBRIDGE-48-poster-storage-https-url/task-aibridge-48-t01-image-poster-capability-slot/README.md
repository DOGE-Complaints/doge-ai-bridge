# Task: image-poster capability slot (DP6)

**Status:** Done · P3 2026-10-14T13:50:18Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-48-poster-storage-https-url.md`  
**Parent story:** [`STORY-AIBRIDGE-48-poster-storage-https-url.md`](../STORY-AIBRIDGE-48-poster-storage-https-url.md)  
**P1 scaffold:** 2026-10-14T13:41:02Z · [p1 draft](../../../../../../../../.cursor/plans/p1_aibridge_48_scaffold_20261014T133840Z.plan.md)  
**Maps:** T01 · DP6 fail-closed

## Purpose

Bind image-poster model/vendor id via env/config only. Worker enabled ⇒ image-poster configured or fail-closed.

## AC/DoD

- [x] Gate from Purpose satisfied on disk at P3.
- [ ] `Skill declared: python-pro` present.
- [ ] Open markers preserved — do **not** invent path/env/provider/bucket/model SSOT.
- [ ] Bind-in (49) / Arweave primary / SPA not claimed.
- [ ] No live bucket required as Done gate.

## Where to change (P3)

- Near config/readiness — env name Open.

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-48-t01-image-poster-capability-slot.md` (create at P3 close)
