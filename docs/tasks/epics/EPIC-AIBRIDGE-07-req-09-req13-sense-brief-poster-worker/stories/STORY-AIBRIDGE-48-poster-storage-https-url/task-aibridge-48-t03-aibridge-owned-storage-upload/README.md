# Task: aibridge-owned storage upload (DP2)

**Status:** Done · P3 2026-10-14T13:50:18Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-48-poster-storage-https-url.md`  
**Parent story:** [`STORY-AIBRIDGE-48-poster-storage-https-url.md`](../STORY-AIBRIDGE-48-poster-storage-https-url.md)  
**P1 scaffold:** 2026-10-14T13:41:02Z · [p1 draft](../../../../../../../../.cursor/plans/p1_aibridge_48_scaffold_20261014T133840Z.plan.md)  
**Maps:** T03 · DP2

## Purpose

Upload with aibridge-owned credentials; gateway MVP does not hold storage write keys. Fail-closed when creds missing.

## AC/DoD

- [x] Gate from Purpose satisfied on disk at P3.
- [ ] `Skill declared: python-pro` present.
- [ ] Open markers preserved — do **not** invent path/env/provider/bucket/model SSOT.
- [ ] Bind-in (49) / Arweave primary / SPA not claimed.
- [ ] No live bucket required as Done gate.

## Where to change (P3)

- Storage client module — path/provider/bucket Open.

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-48-t03-aibridge-owned-storage-upload.md` (create at P3 close)
