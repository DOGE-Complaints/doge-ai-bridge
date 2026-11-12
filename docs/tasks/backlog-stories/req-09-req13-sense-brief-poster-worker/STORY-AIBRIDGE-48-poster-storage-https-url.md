# STORY-AIBRIDGE-48 — Civic poster + aibridge-owned storage HTTPS URL

## Meta
- **Key:** `STORY-AIBRIDGE-48-poster-storage-https-url`
- **Status:** P5 Done · TASKED=0 · WAIVED G-01…G-03 · pkg-000051 · next **P7** (skip P6) · activation **none** · 2026-10-14T14:00:18Z  
- **P1 materialize:** 2026-10-14T13:41:02Z · [p1 APPLIED](../../../../../.cursor/plans/p1_aibridge_48_scaffold_20261014T133840Z.plan.md) · pipeline [`STORY-….md`](../../epics/EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker/stories/STORY-AIBRIDGE-48-poster-storage-https-url/STORY-AIBRIDGE-48-poster-storage-https-url.md)
- **P3 Execute:** 2026-10-14T13:50:18Z · [p3](../../run-reports/run-summary-20261014-1350-story-aibridge-48-p3.md)
- **P5 APPLY:** 2026-10-14T14:00:18Z · [p5](../../run-reports/run-summary-20261014-1400-story-aibridge-48-p5-disposition.md)
- **Parent REQ:** [`REQ-09`](../../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) §§1.2–3,2,4.3,5 AC-03,8.4
- **Tech-arch:** [`02-brief-poster-pipeline.md`](../../../architecture/sense-brief-poster-worker/02-brief-poster-pipeline.md) · [`03-storage-bind-verify.md`](../../../architecture/sense-brief-poster-worker/03-storage-bind-verify.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [46](STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md) · [47](STORY-AIBRIDGE-47-sense-brief-prompts-policy.md) · [49](STORY-AIBRIDGE-49-gateway-bind-fail-version.md) · [50](STORY-AIBRIDGE-50-worker-isolation-harness.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-10-14T11:37:31Z
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)
- **Subtasks:** derived from sense-brief-poster-worker arch (2026-10-14)

## Scope
- Generate civic poster image from brief (image-poster capability slot; model id via env).
- Upload via aibridge-owned object storage credentials → public HTTPS URL.
- Gateway does not need storage write keys for MVP.
- Fail classes for image/storage failures (wire strings Open): `image_generation_failed`, `storage_upload_failed`.
- Provider/bucket id Open — do not invent SSOT.

## Out of scope
- Bind-in to gateway (49); Arweave as primary MVP media; SPA rendering.

## Verified current state
- Image generation / aibridge-owned storage — **Present** (P3): `src/aibridge/poster/` · `AIBRIDGE_WORKER_IMAGE_POSTER_MODEL` · `AIBRIDGE_WORKER_STORAGE_UPLOAD_CREDENTIAL`.

## Target / AC
- [x] AC-09-03: Successful job yields public HTTPS poster URL.
- [x] Upload uses aibridge-owned creds; fail-closed if missing when worker enabled.
- [x] Poster derived from brief (not interview templates).

**Implement names (P3):** `src/aibridge/poster/` · env slots above · fail `image_generation_failed` / `storage_upload_failed`. Provider/bucket/CDN remain Open.

## Code points
- Storage client module — **Present**: `src/aibridge/poster/storage.py`
- image-poster slot wiring — **Present**: `AIBRIDGE_WORKER_IMAGE_POSTER_MODEL`

## Technical subtasks

Arch: [`02-brief-poster-pipeline.md`](../../../architecture/sense-brief-poster-worker/02-brief-poster-pipeline.md) (poster/slots) · [`03-storage-bind-verify.md`](../../../architecture/sense-brief-poster-worker/03-storage-bind-verify.md) (storage) · DP2/DP6 · AC-09-03.

### T01 — image-poster capability slot (DP6)

- Bind image-poster model/vendor id via env/config only.
- Worker enabled ⇒ image-poster configured or **fail-closed**.

**Gate:** missing image-poster id when worker enabled → fail-closed.  
**Не:** invent concrete model string SSOT; multi-provider v1.

### T02 — Poster bytes from brief

- Generate civic poster image **from** brief (not interview templates / unrelated corpus).
- Hand bytes to storage upload (T03).

**Gate:** poster input is brief-derived; interview templates are not the source.  
**Не:** Arweave primary MVP media; SPA rendering.

### T03 — aibridge-owned storage upload (DP2)

- Upload with aibridge-owned credentials; gateway MVP does **not** hold storage write keys.
- Provider / bucket id / CDN — **Open** (do not invent SSOT).
- Fail-closed when worker enabled and storage creds missing.

**Gate:** upload path uses aibridge-owned creds only.  
**Не:** gateway-side upload of poster bytes.

### T04 — Public HTTPS URL + failure classes

- Successful upload yields **public HTTPS** poster URL for later bind (49).
- Failures map to logical classes `image_generation_failed` / `storage_upload_failed` (wire strings Open).

**Gate:** success path returns HTTPS URL; failures are explicit classes (no silent fake URL).  
**Не:** bind-in client (49).

### T05 — Mockable upload port

- Expose a mockable upload port/interface so STORY-50 can stub storage without live bucket.

**Gate:** harness can inject mock returning HTTPS URL.  
**Не:** require live bucket in CI.

### T06 — Storage-mock tests (AC-09-03 slice)

- Tests: mock upload → HTTPS URL; missing creds fail-closed when enabled; image-slot failure class.

**Gate:** isolation tests green without live vendor/bucket.  
**Не:** live smoke as Done gate (ops residual).

## Dependencies
- STORY-AIBRIDGE-46, STORY-AIBRIDGE-47
