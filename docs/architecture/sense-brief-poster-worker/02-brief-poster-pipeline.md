# Brief + poster pipeline — sense brief + civic poster worker

| Field | Value |
|-------|--------|
| **Parent overview** | [`00-overview.md`](./00-overview.md) |
| **Parent REQ** | [`../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md`](../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) |
| **Recorded** | 2026-10-14T11:23:06Z |
| **Mode** | Target technical architecture — not STORY/pkg |

---

## 1) Concern

How the worker turns Issue corpus into a **structured sense brief** and a **civic poster image**, under REQ13 L2 / L5 / L11 and AC-09-02 / AC-09-05 — without freezing exact JSON keys or model IDs as SSOT.

---

## 2) Target behavior

### Accept inputs (logical)

- Issue id  
- Corpus: Stories text/metadata needed for brief (shape Open; must be sufficient or fail `corpus_insufficient`)  
- Optional locale hints  
- Generation-version (for idempotency / bind)

### Brief — logical L2 field set (DP4, AC-09-02)

**Required outcomes (logical, not wire names):**

| Logical field | Rule |
|---------------|------|
| title | Plain text, ≤80 |
| summary | i18n: et / ru / en |
| problem / context / severity / audience / desired_outcome / evidence_refs | Present in logical model to satisfy REQ13 L2; exact keys Open |

**Policy (AC-09-05, L11):**

- System/instructions language: **EN**  
- Outputs may be et/ru/en as required  
- Civic, non-metaphor, non-toxic tone for poster-facing content  
- **No invented** civic facts (addresses, agencies, events) beyond corpus — refuse or omit rather than fabricate  
- Gateway public wire does **not** expose raw brief blob (gateway DP4); brief feeds bind apply → title/summary (and related apply fields Open)

### Poster (AC-09-03)

- Generated **from** the brief (not from unrelated interview templates)  
- Civic poster image bytes → handed to storage upload (sibling `03`)  
- Regenerate with new version → new asset (AC-09-06)

### Models — capability slots (DP6)

| Slot | Role | Binding |
|------|------|---------|
| text-brief | LLM for structured brief | Model/vendor id via env/config only |
| image-poster | Image generation for poster | Model/vendor id via env/config only |

No model catalog SSOT in this package. Worker enabled ⇒ both slots configured or **fail-closed**.

### Prompts — dedicated module (DP7)

- Separate package/files for sense-brief + poster instructions  
- **Must not** use Telegram interview / content-launch templates as the civic SSOT  
- Shared generic safety helpers allowed only if already Present and do not pull interview corpus  
- On-disk path inside image — **Open**

---

## 3) Ownership

| Actor | Owns |
|-------|------|
| aibridge worker | Brief JSON production, poster bytes, prompt module, slot invocation |
| Gateway | Whether applied brief becomes public title/summary; board status |
| Ops | Concrete model ids / rate limits (outside arch SSOT) |

---

## 4) Verify (logical)

- Golden / fixture brief satisfies logical L2 (title≤80, summary et/ru/en present).  
- Prompt path used is worker module, not interview templates.  
- Policy tests: invented-fact refusal behavior (fixture corpus).  
- Mapping: AC-09-02, AC-09-05.

---

## 5) Explicit not in this doc

- Exact JSON Schema file path or key spellings  
- Exact OpenAI (or other) model string IDs  
- Prompt body text  
- Multi-provider abstraction v1  
