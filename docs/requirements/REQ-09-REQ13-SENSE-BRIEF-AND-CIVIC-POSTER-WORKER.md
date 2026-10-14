# REQ-09 — REQ13 sense brief + civic poster worker

Parent: [docs/requirements backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md](../../../docs/requirements%20backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md) §1–4.3, §4.5, §5–8 (L2–L5, L11, L13–L14), AC-02–05, AC-07–08  
Parent-id: REQ13-issue-sense-brief-civic-poster  
Siblings:
- [gateway 57](../../../doge-complaints-gateway/docs/requirements/57-req13-issue-sense-brief-poster-projection.md) (contract: consume enqueue; return bindable brief + poster HTTPS URL / failure)
- [spa-app 23](../../../spa-app/docs/requirements/23-req13-issue-poster-board-surfaces.md) (no direct aibridge↔spa MVP contract; SPA reads gateway public Issue)  
Status: Draft — awaiting PA.2  
Дата: 2026-10-13

**Related — Architecture:** [`../architecture/sense-brief-poster-worker/00-overview.md`](../architecture/sense-brief-poster-worker/00-overview.md) · [01-entry-auth-idempotency](../architecture/sense-brief-poster-worker/01-entry-auth-idempotency.md) · [02-brief-poster-pipeline](../architecture/sense-brief-poster-worker/02-brief-poster-pipeline.md) · [03-storage-bind-verify](../architecture/sense-brief-poster-worker/03-storage-bind-verify.md)  
**Related — Interview:** [`../analysis/zeya888.target-tech-arch-interview-sense-brief-poster-worker-2026-10-14.md`](../analysis/zeya888.target-tech-arch-interview-sense-brief-poster-worker-2026-10-14.md)  
**Related — Backlog:** [`../tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/INDEX.md`](../tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/INDEX.md) (STORY-AIBRIDGE-46…50)  
**Related — Sibling gateway arch:** [`../../../doge-complaints-gateway/docs/architecture/issue-sense-brief-poster/00-overview.md`](../../../doge-complaints-gateway/docs/architecture/issue-sense-brief-poster/00-overview.md)

---

## 1) Goal

Добавить в **aibridge** отдельный **AI worker** (не Telegram interview / channel path), который:

1. по триггеру от gateway строит **Issue sense brief** (структурированный JSON: title ≤80, summary i18n, problem/context/severity/audience/desired_outcome/evidence_refs…);
2. из brief генерирует **civic poster image**;
3. публикует изображение в **object storage** (public HTTPS URL);
4. возвращает/биндит результат на gateway Issue (механизм Open).

REQ13: worker ≠ interview (L5); LLM+image; EN prompt, et/ru/en outputs; no invented facts (L11).

## 2) Scope / Out of scope

**In scope**

- New worker module/job type distinct from interview pipeline.
- Structured brief schema (fields TBD at PA.2; must support REQ13 L2).
- Image generation from brief → poster.
- Upload to object storage → HTTPS URL.
- Failure signaling to gateway (no silent success).
- Prompt/system constraints: EN instruction language; i18n outputs; civic, non-metaphor, non-toxic.
- Versioning support for regenerate (new asset version).

**Out of scope**

- Gateway projection of title/summary (sibling 57).
- SPA rendering (sibling 23).
- Changing Telegram interview / REQ-05 content launch behavior.
- Making Arweave primary MVP media.
- Auto-regen on every Story merge.
- Inventing final OpenAI model IDs / bucket names as SSOT before ops PA.2.

## 3) Verified current state

| Fact | Path / note |
|------|-------------|
| aibridge = interview + content paths | REQ-01 runtime, REQ-05 content Phase A — **no** Issue sense-brief worker Present |
| Image generation for Issues | **Absent** in aibridge (verified by product interview + code skim) |
| Gateway alpha projection | sibling gateway `extraction_policy.py` — consumer of worker output later |

## 4) Target behavior

1. Accept job: Issue id + corpus (Stories text/metadata needed for brief) + optional locale hints.
2. Produce brief JSON matching agreed schema; refuse inventing addresses/agencies not in corpus.
3. Produce poster image from brief; upload; obtain HTTPS URL.
4. Notify gateway of success (brief + URL + version) or failure (reason code).
5. Manual regenerate = new version, not silent overwrite without version bump.
6. Logs/metrics: job id, Issue id, success/fail, latency (PII-safe).

## 5) Acceptance criteria

| ID | Criterion |
|----|-----------|
| **AC-09-01** | Worker path is **not** the interview/channel handler (separate entry) |
| **AC-09-02** | Successful job yields structured brief with title ≤80 and summary et/ru/en |
| **AC-09-03** | Successful job yields public HTTPS poster URL |
| **AC-09-04** | Failure returns explicit error to gateway (no fake brief) |
| **AC-09-05** | Prompt/policy: EN instructions; no invented civic facts beyond corpus |
| **AC-09-06** | Regenerate produces new version id/URL distinguishable from prior |

## 6) Open questions

1. Confirm **aibridge** as permanent home vs future dedicated service (product lean: aibridge).
2. Brief JSON schema exact keys.
3. Transport: gateway→worker HTTP vs shared queue.
4. Object storage provider/bucket/CDN; who owns credentials.
5. Model/vendor for text vs image; cost/rate limits.
6. Idempotency key for duplicate enqueues.

## 7) Dependencies

- Parent REQ13 L2–L5, L11, L13–L14.
- Sibling gateway 57 (enqueue + bind).
- Sibling spa 23 (indirect via gateway public read).
- Orthogonal: existing aibridge REQ-01/03/05/07/08 (do not break interview).

## 8) PA.2 order lock (cite parent REQ13 §11)

**This child is Wave 2** — only after parent [REQ13 §11](../../../docs/requirements%20backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md) **Wave 0** joint seam **and** sibling [gateway 57](../../../doge-complaints-gateway/docs/requirements/57-req13-issue-sense-brief-poster-projection.md) **Wave 1** has locked public wire + **bind-in contract**. Full deep PA.2 here before those locks is **out of order**.

### Why not first (chicken-and-egg)

- Board Issue SSOT stays on **gateway**; this worker does not own pending/ready/failed for the public board.
- Verified Present: **aibridge → gateway** intake. Designing aibridge accept-URLs / buckets / models first without gateway bind-in creates a second incompatible contract.
- False «who publishes the enqueue API first?» → real: consume **gateway-owned job state + bind-in**; transport lean from Wave 0/1.

### This PA.2 may deep-dive only against Wave 1 outputs

1. Worker entry **≠** interview/channel (AC-09-01).
2. Accept job per locked transport lean (HTTP nudge, poll/sweep, or queue — as frozen in Wave 0/1).
3. Finalize brief JSON keys (must satisfy REQ13 L2 + gateway projection needs).
4. Image gen → object storage → public HTTPS URL (ownership of upload per gateway §8 choice).
5. Success/fail **bind to gateway** + reason codes; regenerate = new version.
6. Idempotency for duplicate enqueues.

### Must not do in this wave

- Rename or redefine gateway public Issue fields unilaterally.
- Make aibridge the SSOT for board poster status.
- SPA surfaces (sibling 23 is Wave 3; no SPA↔aibridge MVP calls).

### Transport lean (recommendation until Wave 0/1 freeze)

Prefer **callback/bind on gateway** after compute (align with Present aibridge→gateway). Do not invent a parallel Issue store inside aibridge for board truth.

**Gate:** if gateway 57 PA.2 has not frozen bind-in + status wire → stop and return to Wave 1; do not “helpfully” invent path SSOT here.
