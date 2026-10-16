# Verify / coexistence — AI provider selection + mock mode

| Field | Value |
|-------|--------|
| **Parent overview** | [`00-overview.md`](./00-overview.md) |
| **Parent REQ** | [`../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md`](../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) |
| **Recorded** | 2026-10-16T10:23:21Z |
| **Mode** | Target technical architecture — not STORY/pkg |

---

## 1) Concern

What to prove for REQ-10 without inventing gateway e2e as this focus’s gate; how this package coexists with Present REQ-09 worker and packaging.

---

## 2) Verify surfaces (interview)

| Surface | What it proves | Maps to |
|---------|----------------|---------|
| **Unit — ports** | mock text/image adapters; openai text adapter contract (no silent fallback; unknown provider refuse) | AC-10-01…05 |
| **Readyz matrix** | mock/mock without `OPENAI_API_KEY` → ready (other Present gates ok); mock without allow → not ready; openai text without key → not ready | AC-10-08/09, L10-7/8 |
| **Worker-accept smoke** | One integration through **production worker entry** (`POST …/sense-brief/accept` Present path) with providers=`mock`, fixture corpus, peer mocks as needed — accept→brief→poster→bind path without live vendor HTTP | AC-10-03/06 |
| **Out of this focus** | Full gateway board e2e / Railway public board live proof | gateway REQ-58 / ops; cite only |

Story-50 isolation harness mocks peers; it does **not** replace runtime selectable provider flip — this verify set adds the flip matrix.

**Production entry named:** worker accept route + shared ASGI `aibridge.app:app` (not src-only unit as sole DoD).

---

## 3) Packaging

| Question | Answer |
|----------|--------|
| Git ownership ≠ image packaging? | **N/A** for this focus — ports live under `src/aibridge/` already shipped with Present image |
| New FS assets / non-JS in image? | No additional packaging theme beyond existing worker modules |
| Method note | packaging N/A (see interview report) |

---

## 4) Coexistence / migration seams

| Seam | From → To |
|------|-----------|
| No provider env | Unset → `mock` + allow-flag for non-prod |
| Always-required model slots | Nested: model only if `openai` |
| Always OpenAI in readyz | Slot-gated (`02-…`) |
| Pipeline «LLM reserved» | Becomes openai-port responsibility when selected |
| Accept/bind HTTP | Unchanged (REQ-09 as-built) |
| Channel OpenAI | Untouched registry (L10-1) |

**As-is cite anchors (Present after STORY-51…54):**

- `providers/` — ports + registry + `openai_text_live.py` (mocked SUCCESS in tests; live vendor residual Unknown)  
- `readiness.py` — slot-gated OpenAI presence + `AIBRIDGE_ALLOW_MOCK_PROVIDERS` refuse  
- `sense_brief/pipeline.py` — corpus-grounded mock path  
- `poster/image.py` — deterministic PNG  
- REQ-09 arch `sense-brief-poster-worker/` — accept/bind SSOT  
- Runtime verify map: [`../../runtime-docs/03-provider-verify-matrix.md`](../../runtime-docs/03-provider-verify-matrix.md)  

---

## 5) Deploy residual

| Gate | Local / CI substitute | Live proof |
|------|----------------------|------------|
| Mock-first ops | allow-mock + mock/mock + readyz/accept smoke | Public board: providers live text as needed; **allow-mock off** |
| Gateway backfill order | Documented with REQ-58 (AC-10-07) — docs elsewhere | One Issue live text after mock dry-run (ops) |

---

## 6) Not in this doc

NEW STORY/pkg/task lists; scaffolding empty test files; inventing gateway paths.
