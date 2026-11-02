# REQ15 semantic state / roles / instruction assembly — target technical architecture (overview)

| Field | Value |
|-------|--------|
| **Focus** | App-owned semantic interview state; five versioned roles; code-driven instruction assembly (hybrid C); consume parity; L13-3 invalidation via REQ-11 seam |
| **Parent REQ** | [`../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md`](../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) |
| **Peers** | [`../req15-dual-confirm-handoff/00-overview.md`](../req15-dual-confirm-handoff/00-overview.md) · [`../req15-interview-providers/00-overview.md`](../req15-interview-providers/00-overview.md) · [`../runtime/02-content-packaging.md`](../runtime/02-content-packaging.md) · [GPT UI REQ-48](../../../../GPT%20UI/docs/requirements/REQ-48-req15-role-oriented-instruction-line-and-export.md) |
| **T1** | [`../../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md`](../../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md) |
| **Wave readiness** | [`../../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md`](../../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md) §5.3 |
| **Story scope** | [`STORY-AIBRIDGE-62…64`](../../tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md) Present (Todo · AC-05 Partial Q1) |
| **Interview** | [`../../analysis/zeya888.target-tech-arch-interview-req15-semantic-state-roles-2026-11-02.md`](../../analysis/zeya888.target-tech-arch-interview-req15-semantic-state-roles-2026-11-02.md) |
| **Recorded** | 2026-11-02T08:19:34Z |
| **Mode** | Target technical architecture of the focus — not implementation tasks |
| **Slug** | `req15-semantic-state-roles` |
| **Layout** | system (`archDocMode=auto` → ≥3 concerns) |

**Levels:** functional = REQ-13 (AC-AIB-13-01…08, L13-1…3) · this folder = how state/roles/assembly/parity coexist · work items = **other prompts**.

**Siblings:** [`01-semantic-state-store-invalidation.md`](./01-semantic-state-store-invalidation.md) · [`02-roles-coordinator-assembly.md`](./02-roles-coordinator-assembly.md) · [`03-content-volume-parity-verify.md`](./03-content-volume-parity-verify.md)

---

## 1) Context & functional vs tech split

| Layer | Lives in | Content |
|-------|----------|---------|
| Product | REQ-13 + parent REQ15 | Goal, OOS, AC, L13 locks |
| Peer tech | REQ-11 handoff · REQ-12 interview port · GPT-48 authoring/export | Keep boundaries |
| Target tech (this package) | `docs/architecture/req15-semantic-state-roles/` | Store, roles, assembly, volume/parity, evidence |
| Work items | [`STORY-62…64`](../../tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md) | **Not here** |

**Use case:** Application owns interview meaning and role orchestration; instructions are assembled from configured dir (local GPT UI path or prod volume), not authored in aibridge.

**Packaging:** same image. **Packaging seam applied** — Git ownership ≠ image packaging (`runtime/02`).

---

## 2) Target technical architecture (summary)

```text
  GPT-48 export / local GPT UI tree → DOGESTONIA_INSTRUCTIONS_DIR + MANIFEST
         │  consume parity gate (fail-closed if incomplete/mismatch)
         ▼
  assembly: shared core + per-role slice → session pin
         │
         ▼
  coordinator policy (phase/flags) → one role
         │
         ▼
  REQ-12 interview port → Keep InterviewEngine
         │
         ▼
  semantic store (Postgres, ≠ HistoryStore)
         │ meaning change: confirmed facts / corrections / (phase if rights change)
         ▼
  invalidate_send_permission (REQ-11 Keep) → confirm / stash / SPA pipe
```

| Concern | Target | Cite |
|---------|--------|------|
| Semantic store | Separate Postgres store (Interview D1=B) | AC-01 · T1 Replace |
| Meaning → invalidate | Confirmed facts/corrections/(phase) only (D2=B) | L13-3 Target A |
| Until store Present | Transition C — EDIT/revision only | L13-3 · REQ-11 `02` |
| Coordinator | Policy table → one next role (D3=B) | AC-02 |
| Assembly | Shared core + role slice + pin (D5=A) | AC-03 |
| Content home | Volume prod; baked fixture/dev; local env may point at GPT UI (D4=A) | L13-2 · AC-04/05/06 |
| Confirm-offer | Soft understanding OK; send never auto (L13-1) | AC-08 |
| Role prompts | No gateway/SPA procedure | AC-07 · REQ-11 |
| Evidence | Stub required; live Partial without ops window (D6=A) | AC-04/05 spirit |

---

## 3) Ownership / contracts

| Artifact | Owner |
|----------|-------|
| Semantic state + role orchestration | aibridge |
| Instruction markdown / export | GPT UI REQ-48 |
| Model vendor keys / interview provider | REQ-12 |
| Dual-confirm / stash / SPA URL | REQ-11 |
| Telegram I/O | telegram REQ-01 |
| Session utterance history | aibridge HistoryStore (**Keep**, ≠ semantic SSOT) |

---

## 4) Runtime / packaging / verify / env

- **Runtime:** single ASGI — Keep [`../runtime/00-overview.md`](../runtime/00-overview.md).  
- **Packaging:** Git ≠ image; prod instructions via configured dir / Railway volume.  
- **Env:** `DOGESTONIA_INSTRUCTIONS_DIR` + `DOGESTONIA_INSTRUCTIONS_MANIFEST` (+ content commit / OAS / pack as Present). Local may absolute-path to GPT UI checkout or export.  
- **Verify:** see [`03-…`](./03-content-volume-parity-verify.md).

---

## 5) Coexistence with as-is

| As-is | Role |
|-------|------|
| History + `last_confirmed_state` string map | **Keep** history; **not** semantic SSOT |
| `confirm.py:407–445` `invalidate_send_permission` / `apply_edit` | Named seam for Target A when store Present |
| `coordinator.py` auto-offer interpret | **Adapt** under L13-1 + policy coordinator |
| `content.py` / `config.py` `DOGESTONIA_INSTRUCTIONS_*` | **Keep** read contract; **Adapt** parity + per-role assembly |
| `src/instructions/` in image | Fixture/dev after volume cutover (L13-2) |
| `interview_providers/` | Keep — roles call this port |

---

## 6) Open questions

- Exact Postgres DDL for semantic store.  
- Consume-parity inventory/hash wire format (joint GPT-48).  
- Concrete policy-table rows (phase→role).  
- Ops live evidence calendar (volume + real export).  
- Present GPT UI working tree may lack aibridge-compatible manifest — export layout (REQ-48) required for consume Pass.  
- Later: hard understanding-offer gate; role merge/split.

---

## 7) Explicit “Not in this doc”

- NEW STORY / pkg / P3 / product code  
- Invented DDL or hash-file SSOT  
- GPT-48 instruction bodies · provider HTTP · telegram transport · gateway redesign  

**Method notes:** inputs (REQ) ≠ target tech arch ≠ new work items · Git ownership ≠ image packaging · recommendation advisory; operator decided D1–D6.
