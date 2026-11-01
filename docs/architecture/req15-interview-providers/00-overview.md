# REQ15 interview DeepSeek / OpenAI providers — target technical architecture (overview)

| Field | Value |
|-------|--------|
| **Focus** | Selectable interview providers `deepseek` \| `openai` behind a shared port; Keep Present OpenAI Responses path; orthogonal to worker REQ-10 |
| **Parent REQ** | [`../../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md`](../../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) |
| **Worker sibling (≠ this)** | [`../ai-provider-selection/00-overview.md`](../ai-provider-selection/00-overview.md) — `AIBRIDGE_WORKER_*` only |
| **T1** | [`../../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md`](../../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md) |
| **Wave readiness** | [`../../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md`](../../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md) |
| **Story scope** | [`STORY-AIBRIDGE-59…61`](../../tasks/backlog-stories/req-12-req15-interview-deepseek-openai-providers/INDEX.md) Present (tech subtasks pre-P1.3) |
| **Interview** | [`../../analysis/zeya888.target-tech-arch-interview-req15-interview-providers-2026-11-01.md`](../../analysis/zeya888.target-tech-arch-interview-req15-interview-providers-2026-11-01.md) |
| **Recorded** | 2026-11-01T18:55:37Z |
| **Mode** | Target technical architecture of the focus — not implementation tasks |
| **Slug** | `req15-interview-providers` |
| **Layout** | system (`archDocMode=auto` → ≥3 concerns) |

**Levels:** functional = REQ-12 (AC-AIB-12-01…05, L12-1–2) · this folder = how interview provider port/adapters/fail-closed coexist · work items = **other prompts**.

**Siblings in this package:** [`01-interview-port-env-fail-closed.md`](./01-interview-port-env-fail-closed.md) · [`02-adapters-openai-deepseek.md`](./02-adapters-openai-deepseek.md) · [`03-verify-evidence-coexistence.md`](./03-verify-evidence-coexistence.md)

---

## 1) Context & functional vs tech split

| Layer | Lives in | Content |
|-------|----------|---------|
| Product | REQ-12 + parent REQ15 | Goal, OOS, AC, L12-1 env, L12-2 model Open |
| Worker tech (orthogonal) | `docs/architecture/ai-provider-selection/` | Must **not** switch interview |
| Target tech (this package) | `docs/architecture/req15-interview-providers/` | Port, env fail-closed, adapters, evidence |
| Work items | backlog STORY-59…61 | Arch-bound tech subtasks in stories; **not** P1.3/P3 here |

**Use case:** Make interview model backend an explicit config flip (`deepseek` \| `openai`) with a shared port for future roles, without reusing worker env and without silent paid OpenAI fallback.

**Packaging:** same image `aibridge.app:app`. **Packaging seam N/A.**

---

## 2) Target technical architecture (summary)

```text
  env: AIBRIDGE_INTERVIEW_PROVIDER ∈ {deepseek, openai}  (required; unset/unknown → fail-closed)
                    │
                    ▼
         Interview provider registry / port
                    │
         ┌──────────┴──────────┐
         ▼                     ▼
   OpenAI adapter          DeepSeek adapter
   (Keep Production        (Chat Completions +
    ResponsesClient)        base_url; new)
         │                     │
         └──────────┬──────────┘
                    ▼
         Keep InterviewEngine (budgets/tools/history)
                    │
                    ▼
         channel / confirm pipe (REQ-11 Keep)
```

| Concern | Target | Cite |
|---------|--------|------|
| Selector | Explicit env only | L12-1 · AC-01/05 · Interview D2 |
| Orthogonality | ≠ `AIBRIDGE_WORKER_*` | AC-02 · worker arch L10-1 |
| Engine | Keep `InterviewEngine`; port supplies backend | Interview D3 · `interview.py` |
| OpenAI | Keep Responses path | T1 · `app.py:418–426` |
| DeepSeek | New adapter behind same narrow client/turn contract | REQ §2 · Absent in `src/` today |
| Mid-switch v1 | Wire/start only | Interview D4 |
| Evidence | Stub both; live per provider with window | Interview D5 · AC-03/04 |

---

## 3) Ownership / contracts

| Artifact | Owner | Note |
|----------|-------|------|
| Interview provider id | Bridge config | Not telegram / not gateway |
| Model API keys | Bridge secrets | Per adapter; never in channel Bearer |
| Worker provider env | REQ-10 package | Must not select interview |
| Instruction texts | GPT UI REQ-48 | OOS |

---

## 4) Runtime / packaging / verify / env

- **Runtime:** single ASGI — Keep [`../runtime/00-overview.md`](../runtime/00-overview.md).  
- **Packaging:** N/A.  
- **Env / fail-closed:** see [`01-…`](./01-interview-port-env-fail-closed.md).  
- **Verify:** see [`03-…`](./03-verify-evidence-coexistence.md).

---

## 5) Coexistence with as-is

| As-is | Role |
|-------|------|
| `app.py:414–428` OpenAI key → Responses else recording | **Adapt:** resolve via interview port; recording ≠ substitute for unset provider |
| `providers/` worker registry | **Orthogonal** — do not extend for interview |
| REQ-11 dual-confirm / tool-intent | Keep; provider swap must not bypass Send permission |
| REQ-13 roles | Call shared interview port when Present |

---

## 6) Open questions

- DeepSeek model string after live confirm (L12-2); orient / example `deepseek-v4-pro`.  
- Typed fail-reason string catalog.  
- Ops live evidence windows per provider.  
- Future in-session provider flip (out of v1).

**Locked env (L12-3):** `AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY` · `AIBRIDGE_INTERVIEW_DEEPSEEK_BASE_URL` · `AIBRIDGE_INTERVIEW_DEEPSEEK_MODEL` (+ selector L12-1). See [`01-…`](./01-interview-port-env-fail-closed.md) · [`.env.example`](../../../.env.example) §4b.

---

## 7) Explicit “Not in this doc”

- NEW STORY / pkg / P3 / product code (backlog package separate)  
- Worker brief/poster ports · gateway stash · telegram transport · GPT-48 bodies  

**Method notes:** inputs (REQ) ≠ target tech arch ≠ new work items · packaging N/A · recommendation advisory; operator decided in interview + L12-3 env lock 2026-11-01.
