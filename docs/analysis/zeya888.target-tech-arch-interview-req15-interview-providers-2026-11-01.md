# Target tech-arch interview — req15-interview-providers

| Field | Value |
|-------|--------|
| **utc_now** | 2026-11-01T18:55:37Z (`builder_resolve_queue.py --print-utc-now`) |
| **Slug** | `req15-interview-providers` |
| **builder_project** | `aibridge` |
| **focusFolder** | `doge-ai-bridge` |
| **Requirement** | [`../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md`](../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) |
| **Arch root** | [`../architecture/req15-interview-providers/00-overview.md`](../architecture/req15-interview-providers/00-overview.md) |
| **Story scope** | none (0 STORY files) |

---

## 1) Inputs + use case

**Inputs:** REQ-12 only; T1 + wave readiness cited; worker arch `ai-provider-selection/` as orthogonal etalon.

**Use case:** Target technical architecture for interview provider selection (DeepSeek \| OpenAI) behind a shared port — not backlog stories, not code.

---

## 2) Level classify

| Level | Evidence | Implication |
|-------|----------|-------------|
| Mixed functional+tech | REQ-12 Goal/AC/L12; §3 Keep OpenAI / Absent DeepSeek; §7 layout Open | This prompt primary |

---

## 3) Decision log

### D1 — Package vs worker arch

- **Question:** Where to place REQ-12 target tech relative to `ai-provider-selection/`?
- **Options:** A sibling `req15-interview-providers/` · B extend worker package · C runtime-only InterviewEngine if/else
- **Recommendation:** A
- **Operator:** **A** — **accepted**
- **Locks:** system package separate from worker; AC-02 boundary

### D2 — Unset / unknown provider

- **Question:** Default when `AIBRIDGE_INTERVIEW_PROVIDER` unset/unknown?
- **Options:** A fail-closed · B unset→openai transition · C unset→deepseek
- **Recommendation:** A
- **Operator:** **A** — **accepted**
- **Locks:** explicit env required; no silent OpenAI; transition sets `openai` deliberately

### D3 — Port ↔ InterviewEngine

- **Question:** How does shared port connect to Present Engine?
- **Options:** A port supplies backend, Keep Engine · B port replaces Engine path · C two engines
- **Recommendation:** A
- **Operator:** **A** — **accepted**
- **Locks:** Keep budgets/tools/confirm coexistence; DeepSeek adapts to narrow client/turn contract

### D4 — Mid-conversation switch

- **Question:** In-session provider flip in v1?
- **Options:** A wire/start only · B controlled in-session flip · C silent hot-reload
- **Recommendation:** A
- **Operator:** **A** — **accepted**
- **Locks:** no flip API in this arch; §4.5 restore = future

### D5 — Evidence / Done

- **Question:** Stub vs live for AC-04?
- **Options:** A split gate · B stub=full Done · C live always blocking
- **Recommendation:** A
- **Operator:** **A** — **accepted**
- **Locks:** stub both adapters required; live Pass per provider only with ops window

---

## 4) Open Unknowns

- DeepSeek model string after live confirm (L12-2); example `deepseek-v4-pro`  
- Fail-reason string catalog  
- Live evidence window calendar  
- Future in-session flip  

**Post-interview product lock (2026-11-01):** L12-3 DeepSeek nest names — `AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY` · `AIBRIDGE_INTERVIEW_DEEPSEEK_BASE_URL` · `AIBRIDGE_INTERVIEW_DEEPSEEK_MODEL` (see REQ-12 §6 · `.env.example` §4b).  

---

## 5) Link matrix

| Artifact | Link |
|----------|------|
| REQ-12 | → arch `00-overview` + this report |
| Arch root | → REQ-12 · T1 · readiness · worker sibling · this report |
| Stories | none |

---

## 6) Method notes

- Inputs (REQ) ≠ target tech arch ≠ new work items  
- **Packaging N/A**  
- Recommendation advisory; operator decides (all five **accepted**)  
- analysis.mdc: name ≠ create for DeepSeek env name SSOT  
