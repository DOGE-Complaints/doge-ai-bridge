# Target tech-arch interview — sense brief + civic poster worker (aibridge)

**Method:** Architect Studio — inputs → target technical architecture  
**Emitted:** 2026-10-14T11:23:06Z (`builder_resolve_queue.py --print-utc-now`)  
**builder_project:** aibridge · **focus_folder:** `doge-ai-bridge`  
**Slug:** `sense-brief-poster-worker`  
**archDocMode:** `auto` → **system** (folder, 4 files)

---

## 1. Inputs & use case

| Input | Path |
|-------|------|
| Requirement | `doge-ai-bridge/docs/requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md` |
| Story package / list | none (0 STORY files) |
| Sibling gateway arch | `doge-complaints-gateway/docs/architecture/issue-sense-brief-poster/00-overview.md` |
| Arch root (materialized) | `doge-ai-bridge/docs/architecture/sense-brief-poster-worker/00-overview.md` |

**Use case:** Wave-2 target tech SSOT for an aibridge worker that produces Issue sense brief + civic poster, uploads to aibridge-owned storage, and binds to gateway — separate from interview/channel — without inventing path/key SSOT before joint freeze.

**Story scope line:** none — **0** STORY files.

---

## 2. Level classify

| Level | Evidence | Implication |
|-------|----------|-------------|
| Mixed functional+tech | REQ-09 §§1–5 AC + Open Qs; PA.2 Wave-2 lock; gateway Wave-1 path/keys Open | This prompt primary; extract tech into arch package |

---

## 3. Decision log (verbatim)

### Q0 / DP0 — Inherit gateway Wave-1 locks

- **Options summary:** A inherit DP1–6 as baseline / B re-open transport / C wait (no Wave-2).
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A.

### Q1 / DP1 — Runtime topology

- **Options summary:** A same image separate entry / B new dedicated service / C hook into interview path.
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A.

### Q2 / DP2 — Object storage ownership

- **Options summary:** A aibridge-owned bucket+creds / B gateway-owned upload / C shared creds both sides.
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A.

### Q3 / DP3 — Nudge → worker auth

- **Options summary:** A dedicated worker S2S token / B reuse GATEWAY_SERVICE_API_TOKEN inverted / C mTLS/network-only.
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A.

### Q4 / DP4 — Brief schema depth

- **Options summary:** A logical L2 field set + policy (exact keys Open) / B exact JSON keys now / C defer entirely.
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A.

### Q5 / DP5 — Idempotency

- **Options summary:** A Issue+generation-version / B client job-id only / C always recompute.
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A.

### Q6 / DP6 — Model binding

- **Options summary:** A capability slots + env Open / B lock OpenAI family now / C multi-provider abstraction v1.
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A.

### Q7 / DP7 — Prompt packaging

- **Options summary:** A dedicated worker prompt module / B reuse interview prompt store / C external prompt CMS v1.
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A.

### Q8 / DP8 — Verify surfaces

- **Options summary:** A contract+isolation harness / B live vendor smoke required in arch / C logs-only.
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A.

### Q9 / DP9 — Fail reason codes

- **Options summary:** A logical reason classes / B exact enum freeze now / C free-text only.
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A.

**Rejected for v1:** interview/channel as worker entry; gateway storage write keys for MVP; channel Bearer on worker accept; inventing exact JSON keys/paths/model IDs as SSOT; always-recompute duplicates; multi-provider abstraction; external prompt CMS; live-vendor as arch gate; free-text-only fails; aibridge as board SSOT; SPA↔aibridge MVP.

---

## 4. Open Unknowns

1. Literal HTTP paths for worker accept and gateway bind-in.  
2. Exact JSON keys for brief L2 and bind payloads.  
3. Object storage provider / bucket id / CDN.  
4. Env var names (worker token, storage, model slots, bind client).  
5. Concrete model/vendor strings.  
6. Exact fail reason wire enum strings.  
7. Prompt module filesystem path in image.  
8. Production start command / process split detail.

---

## 5. Link matrix

| Artifact | Role |
|----------|------|
| REQ-09 | Product AC / DoD / Wave-2 lock |
| `sense-brief-poster-worker/00-overview.md` (+ 01–03) | Target tech of focus |
| This interview report | Decision log |
| Gateway `issue-sense-brief-poster/` | Sibling Wave-1 contract cite |
| spa REQ 23 | Indirect consumer (cite only) |

---

## 6. Method notes

- Inputs (REQ and/or stories) ≠ target tech arch ≠ new work items.  
- Git ownership ≠ image packaging — packaging pack **applied** (same image, separate worker entry; prompts+worker must ship in production image).  
- Recommendation advisory; operator decides (all DP0–DP9: recommendation **accepted**).

---

## 7. Materialize

| Artifact | Path |
|----------|------|
| Overview | `docs/architecture/sense-brief-poster-worker/00-overview.md` |
| Entry / auth / idempotency | `…/01-entry-auth-idempotency.md` |
| Brief / poster pipeline | `…/02-brief-poster-pipeline.md` |
| Storage / bind / verify | `…/03-storage-bind-verify.md` |
| This report | `docs/analysis/zeya888.target-tech-arch-interview-sense-brief-poster-worker-2026-10-14.md` |
| REQ Related | Architecture + interview links on REQ-09 |

**Not created:** STORY, pkg YAML, product code.
