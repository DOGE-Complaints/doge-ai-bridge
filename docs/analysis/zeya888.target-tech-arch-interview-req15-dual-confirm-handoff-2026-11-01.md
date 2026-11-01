# Target tech-arch interview — req15-dual-confirm-handoff

| Field | Value |
|-------|--------|
| **utc_now** | 2026-11-01T14:10:30Z (`builder_resolve_queue.py --print-utc-now`) |
| **Slug** | `req15-dual-confirm-handoff` |
| **builder_project** | `aibridge` |
| **focusFolder** | `doge-ai-bridge` |
| **Requirement** | [`../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md`](../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) |
| **Arch root** | [`../architecture/req15-dual-confirm-handoff/00-overview.md`](../architecture/req15-dual-confirm-handoff/00-overview.md) |
| **Story scope** | none (0 STORY files) |

---

## 1) Inputs + use case

**Inputs:** REQ-11 only; T1 + wave readiness cited; Keep etalon `runtime/03-confirm-gateway.md`.

**Use case:** Target technical architecture for Keep dual-confirm → gateway stash → SPA handoff, plus REQ15 L11-1 coexistence seam — not new backlog stories, not code.

---

## 2) Level classify

| Level | Evidence | Implication |
|-------|----------|-------------|
| Mixed functional+tech | REQ-11 Goal/AC/L11-1; §3 path:line Keep; §7 Open for Studio | This prompt primary; tech in arch package |

---

## 3) Decision log

### D1 — Doc layout vs `runtime/03`

- **Question:** How to package REQ-11 arch relative to Present `runtime/03-confirm-gateway.md`?
- **Options:** A delta package · B amend runtime/03 in-place · C full replace SSOT
- **Recommendation:** A
- **Operator:** **A** — recommendation **accepted**
- **Locks:** system folder `req15-dual-confirm-handoff/`; Keep SSOT = runtime/03

### D2 — L11-1 hook while REQ-13 Absent

- **Question:** How to document L11-1 before semantic state Present?
- **Options:** A named seam + transition C only · B provisional field taxonomy now · C defer entirely to REQ-13 arch
- **Recommendation:** A
- **Operator:** «принимаю рекомендацию» → **A** — **accepted**
- **Locks:** named invalidate seam; no field invent; enforce today = `apply_edit`

### D3 — Confirm storage

- **Question:** SSOT for confirm artifacts?
- **Options:** A reuse ActionToken/revision/draft_hash · B new schema now · C explicit Unknown defer
- **Recommendation:** A
- **Operator:** «принимаю рекомендацию» → **A** — **accepted**
- **Locks:** no parallel confirm store in this arch

### D4 — Tool loop vs pure role chat

- **Question:** Stash-intent path in REQ-11 target tech?
- **Options:** A Keep internal tool loop as transition · B forbid tool path now · C defer entirely to REQ-13
- **Recommendation:** A
- **Operator:** «принимаю рекомендацию» → **A** — **accepted**
- **Locks:** tool-intent ≠ permission; hard-cut to pure roles = sibling later

### D5 — Evidence / Done

- **Question:** Minimum evidence for AC-AIB-11-07 in arch?
- **Options:** A split gate stub vs live · B stub enough for full AC-07 Done · C live always blocking
- **Recommendation:** A
- **Operator:** «A принимаю» → **A** — **accepted**
- **Locks:** stub required for tech accept; live Pass only with ops window; else Partial

---

## 4) Open Unknowns

- Semantic-field sensitivity (meaning change) — REQ-13 + thin product  
- Live evidence window calendar — ops  
- Tool → pure role hard-cut timing — after REQ-13/48  
- Confirm store Adapt only if future gap proven  

---

## 5) Link matrix

| Artifact | Link |
|----------|------|
| REQ-11 | → arch `00-overview` + this report |
| Arch root | → REQ-11 · T1 · readiness · runtime/03 · siblings 01–03 · this report |
| Stories | none |

---

## 6) Method notes

- Inputs (REQ) ≠ target tech arch ≠ new work items  
- **Packaging N/A** (same image / `src/aibridge`; no new non-src FS ownership)  
- Recommendation advisory; operator decides (all five **accepted**)  
- analysis.mdc: name ≠ create; no stub instruction/schema files; code claims path:line where cited  
