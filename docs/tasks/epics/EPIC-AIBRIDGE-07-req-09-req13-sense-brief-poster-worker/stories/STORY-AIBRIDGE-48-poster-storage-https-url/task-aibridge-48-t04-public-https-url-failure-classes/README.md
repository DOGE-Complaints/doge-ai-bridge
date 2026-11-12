# Task: public HTTPS URL + failure classes

**Status:** Done · P3 2026-10-14T13:50:18Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-48-poster-storage-https-url.md`  
**Parent story:** [`STORY-AIBRIDGE-48-poster-storage-https-url.md`](../STORY-AIBRIDGE-48-poster-storage-https-url.md)  
**P1 scaffold:** 2026-10-14T13:41:02Z · [p1 draft](../../../../../../../../.cursor/plans/p1_aibridge_48_scaffold_20261014T133840Z.plan.md)  
**Maps:** T04 · AC-09-03

## Purpose

Successful upload yields public HTTPS poster URL. Failures map to image_generation_failed / storage_upload_failed (wire Open).

## AC/DoD

- [x] Gate from Purpose satisfied on disk at P3.
- [ ] `Skill declared: python-pro` present.
- [ ] Open markers preserved — do **not** invent path/env/provider/bucket/model SSOT.
- [ ] Bind-in (49) / Arweave primary / SPA not claimed.
- [ ] No live bucket required as Done gate.

## Where to change (P3)

- Pipeline error surface — wire strings Open.

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-48-t04-public-https-url-failure-classes.md` (create at P3 close)
