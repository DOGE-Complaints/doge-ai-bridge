# Sense brief + civic poster worker (aibridge) — target technical architecture (overview)

| Field | Value |
|-------|--------|
| **Focus** | aibridge AI worker: Issue sense brief + civic poster → object storage HTTPS URL → gateway bind-in |
| **Parent REQ** | [`../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md`](../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) |
| **Parent product** | [`docs/requirements backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md`](../../../../docs/requirements%20backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md) §11 Wave 2 |
| **Story scope** | none (0 STORY files) |
| **Interview** | [`../../analysis/zeya888.target-tech-arch-interview-sense-brief-poster-worker-2026-10-14.md`](../../analysis/zeya888.target-tech-arch-interview-sense-brief-poster-worker-2026-10-14.md) |
| **Recorded** | 2026-10-14T11:23:06Z |
| **Mode** | Target technical architecture of the focus — **not** implementation tasks / STORY / pkg |
| **Slug** | `sense-brief-poster-worker` |
| **Layout** | system (`archDocMode=auto` → ≥3 concerns) |

**Levels:** functional = REQ-09 · this folder = how the focus is realized in `doge-ai-bridge` · work items = backlog / P1.3 elsewhere.

**Siblings (contracts only):** gateway [`issue-sense-brief-poster`](../../../../doge-complaints-gateway/docs/architecture/issue-sense-brief-poster/00-overview.md) (Issue SSOT, nudge, bind-in); spa [23](../../../../spa-app/docs/requirements/23-req13-issue-poster-board-surfaces.md) (reads gateway public Issue only — no SPA↔aibridge MVP).

**Wave lock:** Wave 2 after gateway Wave-1 locks (bind-in + thin nudge + sweep; worker uploads; public status/version/URL; no public raw brief blob). HTTP paths / exact JSON keys remain **Open** (joint freeze — do not invent as SSOT here).

---

## 1) Context & functional vs tech split

| Layer | Lives in | Content |
|-------|----------|---------|
| Product | Parent REQ13 + child REQ-09 | Why, OOS, AC-09-01…06, PA.2 order |
| Target tech (this package) | `docs/architecture/sense-brief-poster-worker/` | Components, flows, ownership, packaging entry, verify |
| Work items | backlog STORY (other prompts) | **Not here** |

**Use case:** aibridge hosts a **separate** worker path (≠ Telegram interview / channel) that builds a structured Issue sense brief, generates a civic poster image, uploads to aibridge-owned object storage, and binds success/failure onto the gateway Issue — without becoming board SSOT.

**Packaging:** same deployable image as aibridge runtime; **separate worker entry** (AC-09-01). Git ownership ≠ image packaging: worker module + dedicated prompts must be present in the production image for the worker start path (exact module/argv — **Open**).

---

## 2) Operator locks (Architect Studio interview 2026-10-14)

| # | Topic | Decision | Rec. vs op |
|---|--------|----------|------------|
| DP0 | Wave-1 inherit | Gateway DP1–6 baseline; paths/keys Open | accepted |
| DP1 | Topology | Same image; **separate** worker entry ≠ interview/channel | accepted |
| DP2 | Storage | aibridge-owned bucket/creds; upload → HTTPS URL → gateway bind | accepted |
| DP3 | Nudge auth | Dedicated worker S2S token ≠ channel Bearer | accepted |
| DP4 | Brief schema | Logical L2 field set + policy; exact keys Open | accepted |
| DP5 | Idempotency | Issue id + generation-version; same version no-op; regen = bump | accepted |
| DP6 | Models | Capability slots text-brief + image-poster; ids via env | accepted |
| DP7 | Prompts | Dedicated worker prompt module (not interview templates) | accepted |
| DP8 | Verify | Contract + isolation harness; live vendor smoke optional ops | accepted |
| DP9 | Fail codes | Logical reason classes; wire strings Open | accepted |

---

## 3) Target components (logical)

| Component | Responsibility | Must not |
|-----------|----------------|----------|
| Worker entry | Accept gateway nudge on separate process/route surface | Share interview/channel handler as entry (AC-09-01) |
| Accept + S2S auth | Validate dedicated worker token; reject channel Bearer | Accept citizen/channel credentials |
| Idempotency gate | Dedupe on Issue id + generation-version | Silent full recompute on same version |
| Brief pipeline | Corpus → structured brief (logical L2); EN instructions; no invented civic facts | Invent addresses/agencies beyond corpus (AC-09-05) |
| Poster pipeline | Brief → image via image-poster slot | Skip version bump on regenerate |
| Prompt module | Dedicated EN system/instructions for brief + poster | Reuse Telegram interview corpus templates as SSOT |
| Storage upload | aibridge-owned object store → public HTTPS URL | Require gateway to hold storage write keys (MVP) |
| Bind-in client | POST success (brief apply payload + URL + version) or fail (reason class) to gateway service-auth | Own public board status SSOT |
| Observability | job/Issue ids, success/fail, latency — PII-safe | Log citizen message bodies / secrets |

Siblings:

- [`01-entry-auth-idempotency.md`](./01-entry-auth-idempotency.md)
- [`02-brief-poster-pipeline.md`](./02-brief-poster-pipeline.md)
- [`03-storage-bind-verify.md`](./03-storage-bind-verify.md)

---

## 4) Primary flows (logical)

```text
Gateway: Issue pending + thin nudge (path Open)
  → Worker accept (dedicated S2S)
  → Idempotency: same Issue+generation-version → no-op / same outcome
  → Brief (text-brief slot + dedicated prompts) → logical L2 JSON
  → Poster (image-poster slot) → bytes
  → Upload (aibridge-owned storage) → public HTTPS URL
  → Bind-in on gateway (service-auth):
        success → brief apply payload + URL + version
        fail    → reason class (no fake brief)  // AC-09-04
  → Gateway remains Issue SSOT (status/version/URL public)

Manual regenerate (gateway service token)
  → version bump → new pending → nudge → new URL/asset (AC-09-06)

Sweep/retry duplicate nudge
  → same version → idempotent at worker
```

---

## 5) Runtime / packaging / env / deploy-residual

| Theme | Target |
|-------|--------|
| Runtime | Same aibridge deployable image; **separate** worker entry from interview/channel |
| Packaging seam | Worker code + dedicated prompt module must ship in image used by worker start; do not verify only interview unit tests |
| Env (names Open) | Worker S2S token; storage credentials; text-brief + image-poster model ids; gateway bind-in base/URL + gateway service token for outbound bind — **fail-closed** when worker enabled and required vars missing |
| Deploy residual | Live LLM+image+bucket smoke = optional ops; arch gate = isolation harness (DP8) |

---

## 6) Coexistence with as-is (verified)

| Fact | Evidence |
|------|----------|
| Interview + content runtime present | [`../runtime/00-overview.md`](../runtime/00-overview.md) and siblings |
| Issue sense-brief / civic poster worker in `src/aibridge` | **Absent** (REQ-09 §3; workspace skim 2026-10-14 — no matching module) |
| Gateway Wave-1 target | [`doge-complaints-gateway/.../issue-sense-brief-poster/00-overview.md`](../../../../doge-complaints-gateway/docs/architecture/issue-sense-brief-poster/00-overview.md) DP1–6 |
| aibridge → gateway intake direction | Present (parent REQ13 / REQ-09 transport lean) |
| Channel Bearer trust domain | Existing channel façade — **must not** authorize worker accept |

---

## 7) Open questions (residual)

1. Literal HTTP paths for worker accept and gateway bind-in.  
2. Exact JSON keys for brief L2 and bind success/fail payloads.  
3. Object storage provider / bucket id / CDN.  
4. Env var names (worker token, storage, model slots, bind client).  
5. Concrete model/vendor strings for capability slots.  
6. Exact fail reason wire enum strings.  
7. Prompt module filesystem path inside the image.  
8. Production start command / process split detail (separate entry locked; argv/module Open).

---

## 8) Explicit not in this doc

- NEW STORY keys, pkg YAML, P3 tasks, or product code  
- Invented final HTTP paths, bucket names, or model IDs as SSOT  
- Gateway public Issue field rename; aibridge as board SSOT  
- SPA UI / SPA↔aibridge MVP calls  
- Reuse of interview/channel entry as worker accept  
