# STORY-AIBRIDGE-48 — Civic poster + aibridge-owned storage HTTPS URL

## Meta
- **Key:** `STORY-AIBRIDGE-48-poster-storage-https-url`
- **Status:** P5 Done · TASKED=0 · WAIVED G-01…G-03 · pkg-000051 · next **P7** (skip P6) · activation **none** · 2026-10-14T14:00:18Z
- **Parent Epic:** [`EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker.md`](../../EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker.md)
- **source:** `backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-48-poster-storage-https-url.md`
- **decision_ref:** [`STORY-AIBRIDGE-48-….md`](../../../../backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-48-poster-storage-https-url.md) · [`REQ-09`](../../../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) §§1.2–3,2,4.3,5 AC-03,8.4 · [`02-brief-poster-pipeline.md`](../../../../architecture/sense-brief-poster-worker/02-brief-poster-pipeline.md) · [`03-storage-bind-verify.md`](../../../../architecture/sense-brief-poster-worker/03-storage-bind-verify.md)
- **Package:** [`req-09-req13-sense-brief-poster-worker/INDEX.md`](../../../../backlog-stories/req-09-req13-sense-brief-poster-worker/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000051-20261014-epic-aibridge-07-story-48-poster-storage-https-url.yaml`
- **P1 materialize:** 2026-10-14T13:41:02Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_48_scaffold_20261014T133840Z.plan.md)
- **P3 Execute:** 2026-10-14T13:50:18Z · [p3](../../../../run-reports/run-summary-20261014-1350-story-aibridge-48-p3.md)
- **P4 Audit:** 2026-10-14T13:56:01Z · [p4](../../../../analysis/p4-audit-STORY-AIBRIDGE-48-poster-storage-https-url-20261014.md)
- **P5 APPLY:** 2026-10-14T14:00:18Z · [p5](../../../../run-reports/run-summary-20261014-1400-story-aibridge-48-p5-disposition.md)
- **Gate:** [t07](./task-aibridge-48-t07-story-gate/README.md) · **PASS**
- **Depends:** STORY-AIBRIDGE-46 · STORY-AIBRIDGE-47

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-09 | [`REQ-09`](../../../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) |
| Poster / slots | [`02-brief-poster-pipeline.md`](../../../../architecture/sense-brief-poster-worker/02-brief-poster-pipeline.md) |
| Storage / HTTPS | [`03-storage-bind-verify.md`](../../../../architecture/sense-brief-poster-worker/03-storage-bind-verify.md) |
| Brief (47) | `src/aibridge/sense_brief/` |
| Poster (48) | `src/aibridge/poster/` |

## Scope
- Generate civic poster image from brief (image-poster capability slot; model id via env).
- Upload via aibridge-owned object storage credentials → public HTTPS URL.
- Gateway does not need storage write keys for MVP.
- Fail classes for image/storage failures (wire strings Open): `image_generation_failed`, `storage_upload_failed`.
- Provider/bucket id Open — do not invent SSOT.

## Вне scope
- Bind-in to gateway (49); Arweave as primary MVP media; SPA rendering.
- Inventing provider/bucket/model id SSOT; live bucket as Done gate.

## Context
Accept + L2 brief Present (46/47). Image generation / poster storage upload — **Present** (P3).

## Target / AC
- [x] AC-09-03: Successful job yields public HTTPS poster URL.
- [x] Upload uses aibridge-owned creds; fail-closed if missing when worker enabled.
- [x] Poster derived from brief (not interview templates).
- [x] Nested tasks Done at execute

**Implement names (P3):** `src/aibridge/poster/` · `AIBRIDGE_WORKER_IMAGE_POSTER_MODEL` · `AIBRIDGE_WORKER_STORAGE_UPLOAD_CREDENTIAL` · fail `image_generation_failed` / `storage_upload_failed` · mint host implement-local (provider/bucket/CDN still Open).

## Nested tasks (pkg-000051)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-48-t01-image-poster-capability-slot](./task-aibridge-48-t01-image-poster-capability-slot/README.md) | T01 · DP6 | **Done** |
| t02 | [task-aibridge-48-t02-poster-bytes-from-brief](./task-aibridge-48-t02-poster-bytes-from-brief/README.md) | T02 · from brief | **Done** |
| t03 | [task-aibridge-48-t03-aibridge-owned-storage-upload](./task-aibridge-48-t03-aibridge-owned-storage-upload/README.md) | T03 · DP2 | **Done** |
| t04 | [task-aibridge-48-t04-public-https-url-failure-classes](./task-aibridge-48-t04-public-https-url-failure-classes/README.md) | T04 · AC-09-03 | **Done** |
| t05 | [task-aibridge-48-t05-mockable-upload-port](./task-aibridge-48-t05-mockable-upload-port/README.md) | T05 · harness | **Done** |
| t06 | [task-aibridge-48-t06-storage-mock-tests](./task-aibridge-48-t06-storage-mock-tests/README.md) | T06 fixtures | **Done** |
| t07 | [task-aibridge-48-t07-story-gate](./task-aibridge-48-t07-story-gate/README.md) | story AC gate | **PASS** |
