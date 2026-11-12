# Sense brief + civic poster worker (aibridge) — target technical architecture (overview)

| Field | Value |
|-------|--------|
| **Focus** | aibridge AI worker: Issue sense brief + civic poster → object storage HTTPS URL → gateway bind-in |
| **Parent REQ** | [`../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md`](../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) |
| **Parent product** | [`docs/requirements backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md`](../../../../docs/requirements%20backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md) §11 Wave 2 |
| **Story scope** | [`req-09-req13-sense-brief-poster-worker`](../../tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/INDEX.md) — STORY-AIBRIDGE-46…50 |
| **Interview** | [`../../analysis/zeya888.target-tech-arch-interview-sense-brief-poster-worker-2026-10-14.md`](../../analysis/zeya888.target-tech-arch-interview-sense-brief-poster-worker-2026-10-14.md) |
| **Recorded** | 2026-10-14T11:23:06Z · **As-built refresh** 2026-10-15T10:13:28Z |
| **Mode** | Target technical architecture + as-built implement freeze (code Present) |
| **Slug** | `sense-brief-poster-worker` |
| **Layout** | system (`archDocMode=auto` → ≥3 concerns) |
| **Validation** | [`../../analysis/zeya888.req-09-stories-46-50-code-validation-2026-10-15.md`](../../analysis/zeya888.req-09-stories-46-50-code-validation-2026-10-15.md) |
| **Gateway handoff** | [`../../analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md`](../../analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md) |

**Levels:** functional = REQ-09 · this folder = how the focus is realized in `doge-ai-bridge` · work items = backlog STORY-46…50.

**Siblings (contracts only):** gateway [`issue-sense-brief-poster`](../../../../doge-complaints-gateway/docs/architecture/issue-sense-brief-poster/00-overview.md) (Issue SSOT, nudge, bind-in); spa [23](../../../../spa-app/docs/requirements/23-req13-issue-poster-board-surfaces.md) (reads gateway public Issue only — no SPA↔aibridge MVP).

**Wave lock:** Wave 2 after gateway Wave-1 locks. Operator interview left paths/keys **Open**; **as-built** (below) records implement choices from STORY-46…50 — joint freeze with gateway receiver still required for public board SSOT.

---

## 1) Context & functional vs tech split

| Layer | Lives in | Content |
|-------|----------|---------|
| Product | Parent REQ13 + child REQ-09 | Why, OOS, AC-09-01…06, PA.2 order |
| Target tech (this package) | `docs/architecture/sense-brief-poster-worker/` | Components, flows, ownership, packaging entry, verify |
| Work items | backlog STORY (other prompts) | **Not here** |

**Use case:** aibridge hosts a **separate** worker path (≠ Telegram interview / channel) that builds a structured Issue sense brief, generates a civic poster image, uploads to aibridge-owned object storage, and binds success/failure onto the gateway Issue — without becoming board SSOT.

**Packaging:** same deployable image as aibridge runtime; **separate worker entry** (AC-09-01). Worker modules + dedicated prompts ship under `src/aibridge/` with ASGI app `aibridge.app:app` (`make serve`).

---

## 1b) As-built implement freeze (2026-10-15)

Implement choices Present in code (not gateway public SSOT until sibling freeze):

| Concern | As-built | Cite |
|---------|----------|------|
| Accept path | `POST /v1/worker/sense-brief/accept` · prefix `/v1/worker/` | `worker_accept.py:21–22`; `app.py:684–685` |
| Accept auth | `Authorization: Bearer` = `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN`; channel Bearer rejected | `auth.py:45–58`; `app.py:566–626` |
| Accept JSON | `issue_id`, `generation_version`, optional `corpus` | `worker_accept.py:25–32` |
| Enable / slots | `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED`, `_S2S_TOKEN`, `_TEXT_BRIEF_MODEL`, `_IMAGE_POSTER_MODEL`, `_STORAGE_UPLOAD_CREDENTIAL` | `config.py:197–219` |
| Brief L2 keys | `title`, `summary.{et,ru,en}`, `problem`, `context`, `severity`, `audience`, `desired_outcome`, `evidence_refs` | `sense_brief/model.py` |
| Bind client path | `POST {GATEWAY_BASE_URL}/v1/issue-sense-brief/bind` | `sense_bind/client.py:32` |
| Bind auth | `GATEWAY_SERVICE_API_TOKEN` (≠ channel / worker S2S) | `sense_bind/client.py:59–88` |
| Bind success | `outcome=success`, `poster_url`, `apply.{title,summary}`, `issue_id`, `generation_version` | `sense_bind/payload.py:31–40` |
| Bind failure | `outcome=failure`, `reason_class` (no brief/apply) | `sense_bind/payload.py:55–64` |
| Reason classes | `accept_unauthorized`, `corpus_insufficient`, `brief_generation_failed`, `image_generation_failed`, `storage_upload_failed`, `bind_rejected`, `internal_error` | `sense_bind/errors.py:8–17` |
| Modules | `worker_accept.py`, `sense_brief/`, `poster/`, `sense_bind/` | `src/aibridge/` |
| OpenAPI | [`../../openapi/aibridge-worker-sense-brief-v1.openapi.yaml`](../../openapi/aibridge-worker-sense-brief-v1.openapi.yaml) | docs |

**Still residual Open:** production object-storage provider/CDN; concrete model vendor strings; gateway **bind receiver** + public Issue wire keys (sibling 57); multi-replica idempotency store (current = in-process).

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
Gateway: Issue pending + thin nudge
  → POST /v1/worker/sense-brief/accept (worker S2S)
  → Idempotency: same Issue+generation-version → no-op / same outcome
  → Brief (text-brief slot + sense_brief prompts) → L2 JSON
  → Poster (image-poster slot) → bytes
  → Upload (aibridge-owned creds) → public HTTPS URL
  → POST {GATEWAY_BASE_URL}/v1/issue-sense-brief/bind (GATEWAY_SERVICE_API_TOKEN):
        success → apply + URL + version
        fail    → reason_class (no fake brief)
  → Gateway remains Issue SSOT

Manual regenerate (gateway service token)
  → version bump → new pending → nudge → new URL/asset

Sweep/retry duplicate nudge
  → same version → idempotent at worker (in-process store)
```

---

## 5) Runtime / packaging / env / deploy-residual

| Theme | Target |
|-------|--------|
| Runtime | Same image; worker routes on `aibridge.app:app` (`make serve`) |
| Packaging seam | `sense_brief/`, `poster/`, `sense_bind/`, `worker_accept.py` in image |
| Env (as-built names) | See §1b; fail-closed when worker enabled and required vars missing |
| Deploy residual | Live LLM+image+bucket+gateway receiver smoke = optional ops; arch gate = isolation harness (DP8) — 48 tests green 2026-10-15 |

---

## 6) Coexistence with as-is (verified)

| Fact | Evidence |
|------|----------|
| Interview + content runtime present | [`../runtime/00-overview.md`](../runtime/00-overview.md) and siblings |
| Issue sense-brief / civic poster worker | **Present** — `worker_accept.py`, `sense_brief/`, `poster/`, `sense_bind/` (2026-10-15) |
| Gateway Wave-1 target | [`doge-complaints-gateway/.../issue-sense-brief-poster/00-overview.md`](../../../../doge-complaints-gateway/docs/architecture/issue-sense-brief-poster/00-overview.md) DP1–6 |
| aibridge → gateway intake direction | Present (`gateway.py` stash + `sense_bind` bind client) |
| Channel Bearer trust domain | Must not authorize worker accept — enforced `auth.py:45–58` |

---

## 7) Open questions (residual)

1. ~~Literal HTTP paths for worker accept and aibridge bind client~~ → **as-built §1b**; gateway **receiver** path still needs sibling confirm.  
2. ~~Exact JSON keys for brief L2 and bind payloads (aibridge side)~~ → **as-built §1b**; gateway public wire keys still Open.  
3. Object storage provider / bucket id / CDN (production).  
4. ~~Env var names (worker side)~~ → **as-built §1b**.  
5. Concrete model/vendor strings for capability slots.  
6. ~~Fail reason wire strings (aibridge enums)~~ → **as-built §1b**.  
7. Production CDN vs fixture mint host (`aibridge-poster.test`).  
8. Shared idempotency store for multi-replica.

---

## 8) Explicit not in this doc

- Closing P7/P8 process for stories  
- Gateway public Issue field rename; aibridge as board SSOT  
- SPA UI / SPA↔aibridge MVP calls  
- Reuse of interview/channel entry as worker accept  
- Inventing production bucket/model catalog as SSOT  
