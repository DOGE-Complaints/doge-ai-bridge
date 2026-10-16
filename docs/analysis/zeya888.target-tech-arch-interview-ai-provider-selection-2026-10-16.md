# Target tech-arch interview — AI provider selection + mock mode (aibridge)

**Method:** Architect Studio — inputs → target technical architecture  
**Emitted:** 2026-10-16T10:23:21Z (`builder_resolve_queue.py --print-utc-now`)  
**builder_project:** aibridge · **focus_folder:** `doge-ai-bridge`  
**Slug:** `ai-provider-selection`  
**archDocMode:** `auto` → **system** (folder, 4 files)

---

## 1. Inputs & use case

| Input | Path |
|-------|------|
| Requirement | `doge-ai-bridge/docs/requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md` |
| Story package / list | none (0 STORY files) |
| Sibling worker arch | `doge-ai-bridge/docs/architecture/sense-brief-poster-worker/00-overview.md` |
| Sibling gateway REQ | `doge-complaints-gateway/docs/requirements/58-req13-existing-issues-sense-brief-backfill-via-regenerate.md` |
| Arch root (materialized) | `doge-ai-bridge/docs/architecture/ai-provider-selection/00-overview.md` |

**Use case:** Target tech SSOT for worker-only selectable text/image provider ports (`mock` + first live OpenAI text), fail-closed / readyz / prod refuse mock, so gateway REQ-58 can mock-first dry-run without rewriting accept/bind or channel interview.

**Story scope line:** none — **0** STORY files.

**Pre-closed in REQ (not re-opened):** L10-1…L10-8 (2026-10-16). This interview closed residual tech gaps (env names, nest, readyz, defaults, verify, enforce points).

---

## 2. Level classify

| Level | Evidence | Implication |
|-------|----------|-------------|
| Mixed functional+tech | REQ-10 AC-10-01…10 + L10-*; residual Open env/override naming | Extract tech into arch package; REQ stays product-facing |

---

## 3. Decision log (verbatim)

### Q1 — Nest provider selectors with model slots

- **Options analytics summary:** A Provider + model nested (model-id only if openai) / B Replace model slot with provider id / C Keep model always required + provider beside.
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A.

### Q2 — Readyz / OpenAI presence when mock

- **Options analytics summary:** A Slot-gated OpenAI (key only if live provider selected) / B Worker-only gate separate from channel / C Keep always-require OpenAI key.
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A.

### Q3 — Production refuse mock signal

- **Options analytics summary:** A Explicit allow-mock flag / B Environment class (`AIBRIDGE_ENV=…`) / C Public-board deploy profile (Unknown as-is).
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A.

### Q4 — Env naming convention

- **Options analytics summary:** A Parallel `AIBRIDGE_WORKER_*_PROVIDER` + `AIBRIDGE_ALLOW_MOCK_PROVIDERS` / B Short `AIBRIDGE_TEXT_PROVIDER` / C Nested JSON blob.
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A.

### Q5 — Default when provider unset

- **Options analytics summary:** A Fail-closed unset / B Default `mock` + allow-flag gate / C Default `openai` legacy.
- **Agent recommendation:** B.
- **Operator decision:** **accepted**.
- **Answer:** B.

### Q6 — Verify surfaces

- **Options analytics summary:** A Unit ports + readyz matrix / B A + worker-accept smoke on mock / C Full gateway e2e.
- **Agent recommendation:** B.
- **Operator decision:** **accepted**.
- **Answer:** B — unit + readyz matrix + один worker-accept smoke на mock.

### Q7 — Enforce allow-mock refuse

- **Options analytics summary:** A Readyz + accept / B Readyz only / C Accept only.
- **Agent recommendation:** A.
- **Operator decision:** **accepted**.
- **Answer:** A — readyz + accept.

**Rejected for v1:** replace Present model-slot semantics; always-require OpenAI key with mock/mock; default openai when unset; gateway e2e as sole aibridge arch gate; readyz-only or accept-only mock refuse; short/JSON env families; channel registry in this REQ.

---

## 4. Open Unknowns

1. Exact readiness reason / accept fail-class **string** for mock-without-allow.  
2. When to add live image vendor (REQ-10 residual).  
3. Channel readiness nuance when same process hosts live channel OpenAI + worker mock (policy in arch `02-…`; channel registry still OOS).

---

## 5. Link matrix

| Artifact | Role |
|----------|------|
| REQ-10 | Product AC / DoD / L10 locks |
| `ai-provider-selection/00-overview.md` (+ 01–03) | Target tech of focus |
| This interview report | Decision log |
| `sense-brief-poster-worker/` | Sibling REQ-09 as-built cite |
| Gateway REQ-58 | Ops mock-first order cite |

---

## 6. Method notes

- Inputs (REQ and/or stories) ≠ target tech arch ≠ new work items.  
- Git ownership ≠ image packaging — **packaging N/A** for this focus (same image; ports under Present `src/aibridge/`).  
- Recommendation advisory; operator decides (Q1–Q7: recommendation **accepted**).

---

## 7. Materialize

| Artifact | Path |
|----------|------|
| Overview | `docs/architecture/ai-provider-selection/00-overview.md` |
| Provider ports | `…/01-provider-ports.md` |
| Readyz / env / fail-closed | `…/02-readyz-env-fail-closed.md` |
| Verify / coexistence | `…/03-verify-coexistence.md` |
| This report | `docs/analysis/zeya888.target-tech-arch-interview-ai-provider-selection-2026-10-16.md` |
| REQ Related | Architecture + interview links on REQ-10 |

**Not created:** STORY, pkg YAML, product code, stub paths.
