# Target tech-arch interview — req15-semantic-state-roles

| Field | Value |
|-------|--------|
| **utc_now** | 2026-11-02T08:19:34Z (`builder_resolve_queue.py --print-utc-now`) |
| **Slug** | `req15-semantic-state-roles` |
| **builder_project** | `aibridge` |
| **focusFolder** | `doge-ai-bridge` |
| **Requirement** | [`../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md`](../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) |
| **Arch root** | [`../architecture/req15-semantic-state-roles/00-overview.md`](../architecture/req15-semantic-state-roles/00-overview.md) |
| **Story scope** | none (0 STORY files) |

---

## 1) Inputs + use case

**Inputs:** REQ-13 only; T1 + wave readiness §5.3; peers REQ-11/12 + GPT-48 + `runtime/02`.

**Use case:** Target technical architecture for semantic interview state, five roles, hybrid-C assembly/parity — not backlog stories, not code.

---

## 2) Level classify

| Level | Evidence | Implication |
|-------|----------|-------------|
| Mixed functional+tech | REQ-13 AC-01…08 · L13-1…3 · §7 Open DDL/parity/sensitivity | This prompt primary |

---

## 3) Decision log

### D1 — Semantic store home

- **Question:** Where does semantic state live?
- **Options:** A extend session/history · B separate Postgres store · C files on volume
- **Recommendation:** B
- **Operator:** **B** — **accepted**
- **Locks:** Replace Absent store; history Keep as utterance log

### D2 — Meaning-change trigger

- **Question:** What invalidates send permission under L13-3 Target A?
- **Options:** A any write · B confirmed facts/corrections/(phase) · C explicit commit only
- **Recommendation:** B
- **Operator:** **B** — **accepted**
- **Locks:** Draft hypotheses/gaps do not auto-invalidate

### D3 — Coordinator

- **Question:** How are five roles selected?
- **Options:** A fixed pipeline · B policy table one role · C LLM router
- **Recommendation:** B
- **Operator:** **B** — **accepted**
- **Locks:** No free meta-agent; calls REQ-12 port

### D4 — Volume + consume parity

- **Question:** Prod/local content home + parity gate?
- **Options:** A volume prod / baked fixture / parity fail-closed · B baked prod · C GitHub fetch
- **Recommendation:** A
- **Operator:** **A** — **accepted**
- **Follow-up (chat):** Operator wants local `.env` → GPT UI `instructions/`; arch documents hybrid C intent. Verified: GPT UI `instructions.manifest.json` **Absent** at materialize — export/compatible manifest still required for loader Pass.
- **Locks:** L13-2 · Git ≠ image

### D5 — Assembly

- **Question:** How are role instructions built?
- **Options:** A shared core + role slice + pin · B five full megas · C one monolithic string
- **Recommendation:** A
- **Operator:** **A** — **accepted**

### D6 — Evidence

- **Question:** Stub vs live Done?
- **Options:** A split gate · B stub=full Done · C live always blocking
- **Recommendation:** A
- **Operator:** **A** — **accepted**

### L13-1

- **Cited from REQ** (soft understanding / never auto-send) — not re-opened; arch enforces.

---

## 4) Open Unknowns

- Postgres DDL for semantic store  
- Consume-parity hash/inventory format (joint GPT-48)  
- Policy-table concrete rows  
- Live ops evidence calendar  
- GPT UI export layout Present for aibridge `content.py` (root-child manifest entries)

---

## 5) Link matrix

| Artifact | Link |
|----------|------|
| REQ-13 | → arch `00-overview` + this report |
| Arch root | → REQ-13 · T1 · readiness · peers · this report |
| Stories | none |

---

## 6) Method notes

- Inputs (REQ) ≠ target tech arch ≠ new work items  
- **Git ownership ≠ image packaging** (packaging pack applied)  
- Recommendation advisory; operator decides (D1–D6 **accepted**)  
- analysis.mdc: name ≠ create for DDL / hash SSOT / instruction stubs  
