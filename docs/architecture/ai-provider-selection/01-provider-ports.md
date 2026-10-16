# Provider ports — AI provider selection + mock mode

| Field | Value |
|-------|--------|
| **Parent overview** | [`00-overview.md`](./00-overview.md) |
| **Parent REQ** | [`../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md`](../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) |
| **Recorded** | 2026-10-16T10:23:21Z |
| **Mode** | Target technical architecture — not STORY/pkg |

---

## 1) Concern

How the REQ-09 worker resolves **text-brief** and **image-poster** backends via selectable ports (`mock` | `openai`), without changing accept/bind HTTP and without silent OpenAI fallback (AC-10-01…05, L10-2…5).

---

## 2) Target components & trust boundaries

| Component | Role | Trust |
|-----------|------|-------|
| Provider registry (Settings-backed) | Resolve provider id per slot from env | Ops-controlled; fail-closed on unknown id |
| TextBriefProviderPort | Produce L2 brief from corpus | Mock: no vendor HTTP · openai: vendor HTTP |
| ImagePosterProviderPort | Produce poster bytes | Mock: deterministic PNG · live image deferred |
| REQ-09 accept orchestration | Calls ports then storage/bind | Unchanged external contracts |
| Channel / interview client | OOS | Must not share this registry in v1 (L10-1) |

**Flow (logical)**

1. Accept authorized (Present worker S2S).  
2. Resolve text + image providers independently.  
3. Enforce allow-mock policy (see `02-…`) before serving mock.  
4. Text port → L2 (or honest `corpus_insufficient` / mapped fail).  
5. Image port → bytes → Present upload port → bind.

---

## 3) Nest with Present model slots (interview lock)

| Layer | Rule |
|-------|------|
| Provider selector | `mock` \| `openai` (unknown → fail-closed, AC-10-05) |
| Model-id slot | Present `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` / `…_IMAGE_POSTER_MODEL` |
| Nest | Model-id **required only when** that slot’s provider = `openai` |
| Mock | Model-id ignored / not required for fail-closed |

Unset provider → default **`mock`** (interview); still subject to allow-mock gate.

---

## 4) Backend mapping (REQ locks)

| Slot | Provider | Backend |
|------|----------|---------|
| text-brief | `mock` | Present corpus-grounded / fixture path (`sense_brief/pipeline.py`) — L10-3 |
| text-brief | `openai` | Live OpenAI text extract from gateway `{stories:[…]}` → L2 (L10-5, L10-6, AC-10-10) |
| image-poster | `mock` | Present deterministic PNG (`poster/image.py`) — L10-4 |
| image-poster | `openai` | **Deferred** until later explicit live-image lock (L10-5); v1 default image = `mock` even if text = `openai` |

No third parallel fake path: mock **is** the Present deterministic implementation behind the port.

---

## 5) Contracts (logical; no invent beyond inputs + interview)

| Contract | Source |
|----------|--------|
| Accept JSON / bind payloads | REQ-09 as-built (sibling arch) — unchanged |
| Corpus shape | Gateway `{stories:[…]}` (L10-6); worker extracts L2 |
| Fail mapping | Existing worker `reason_class` set for generation failures; mock-without-allow token **Open** (overview §6) |
| Flip mock↔live | Config/env only (AC-10-04) |

---

## 6) Ownership

| Actor | Owns |
|-------|------|
| aibridge | Port interfaces, mock adapters, openai text adapter, registry |
| Vendor OpenAI | Live text HTTP when selected |
| gateway | Corpus content on regenerate / nudge — not provider selection |

---

## 7) Not in this doc

NEW STORY/pkg; Anthropic/Gemini; channel registry; exact OpenAI request wire beyond «live text extract L2».
