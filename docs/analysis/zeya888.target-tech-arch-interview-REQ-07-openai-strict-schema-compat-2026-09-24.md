# Target tech-arch interview — REQ-07 OpenAI strict-schema compatibility projection

**Method:** Architect Studio — inputs → target technical architecture  
**Emitted:** 2026-09-24T10:07:20Z (`builder_resolve_queue.py --print-utc-now`)  
**builder_project:** aibridge · **focus_folder:** `doge-ai-bridge`  
**Slug:** REQ-07-openai-strict-schema-compat

---

## 1. Inputs & use case

| Input | Path |
|-------|------|
| Requirement | `doge-ai-bridge/docs/requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md` |
| Story package | `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/` (INDEX + STORY-AIBRIDGE-19…22) |
| Arch root (materialized) | `doge-ai-bridge/docs/architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md` |

**Use case:** Target tech SSOT so aibridge can send an OpenAI-compatible strict tool (strip `uniqueItems` from projection only) while keeping canonical pack rules and enforcing uniqueness server-side; unblock Telegram turns without weakening node schema.

**Story scope line:** package `req-05-content-phase-a-flat-launch` — **4** STORY files (19–22), all Implemented; used as **seam context only**, not uniqueItems AC.

---

## 2. Level classify

| Level | Evidence | Implication |
|-------|----------|-------------|
| Already path-level technical (+ product AC) | REQ-07 §§6–8, 11–16 | Operator chose **A**: still produce thin target-arch doc |

---

## 3. Decision log (verbatim)

### Q1 — Continue with arch vs implement vs fix REQ id first

- **Options summary:** A arch doc; B switch to implement; C arch + fix REQ id first.
- **Agent recommendation:** C.
- **Operator decision:** **overridden** → **A**.
- **Answer:** A.

### Q2 — Gate 1 schema after projection

- **Options summary:** A Gate1=projection; B Gate1=full canonical; C dual (Gate1 projected, Gate2 canonical, Gate3 wire) explicit.
- **Agent recommendation:** C.
- **Operator decision:** **accepted**.
- **Answer:** C.

### Q3 — ValidationContext bind in create_app scope

- **Options summary:** A full in-scope; B OOS to REQ-04; C minimal schema bind only.
- **Agent recommendation:** C.
- **Operator decision:** **accepted**.
- **Answer:** C.

### Q4 — Verify / DoD residual

- **Options summary:** A local merge + live deploy residual; B live blocks Done; C local-only.
- **Agent recommendation:** A.
- **Operator decision:** **accepted** with elaboration (**two-stage DoD**).
- **Answer (operator, verbatim summary):**  
  Merge gate: unit, projection, validator, readiness, integration (fake transport) must prove: no `uniqueItems` in OpenAI-facing tools; canonical unchanged; Gate 2 rejects duplicate houses; missing/invalid ValidationContext → `/readyz` not_ready; regression fixture for prior `invalid_function_parameters`. Code may merge after merge gate. Focus status then **implemented, live verification pending** (not Done). Deployment verification: after Railway deploy, one real Telegram turn via n8n + aibridge + real OpenAI without schema error → **production verified / rollout complete** (AC-09). Live evidence: time, deployment/version or commit SHA, scenario, status, correlation/request ID; no user text or secrets.

---

## 4. Open Unknowns

1. REQ H1 «REQ-06» vs filename REQ-07 vs Phase B REQ-06.
2. Exact readiness reason string(s) for unbound/invalid ValidationContext.
3. On-disk location for AC-09 live-evidence note.

---

## 5. Link matrix

| Artifact | Role |
|----------|------|
| REQ-07 | Product AC / DoD |
| TECH-ARCH-REQ-07-… | Target tech of focus |
| This interview report | Decision log |
| req-05 INDEX / STORY-19…22 | Prior Implemented seams (Related only) |
| `runtime/00–04` | Broader runtime arch (unchanged bodies) |

---

## 6. Packaging

**Packaging N/A** for Volume hot-swap: OpenAI projection is in-memory; canonical OAS/pack remain Git/image read-only. Method note: **Git ownership ≠ image packaging** still applies to content pins generally; this focus does not add a new FS packaging seam.

---

## 7. Method notes

- Inputs (REQ and/or stories) ≠ target tech arch ≠ new work items.
- Recommendation advisory; operator decides.
- No NEW STORY/pkg created in this materialize.
- analysis.mdc: name ≠ create; materialize only on «запиши».
