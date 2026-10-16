# Readyz / env / fail-closed — AI provider selection + mock mode

| Field | Value |
|-------|--------|
| **Parent overview** | [`00-overview.md`](./00-overview.md) |
| **Parent REQ** | [`../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md`](../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) |
| **Recorded** | 2026-10-16T10:23:21Z |
| **Mode** | Target technical architecture — not STORY/pkg |

---

## 1) Concern

Env SSOT for provider selectors + production refuse of mock; readiness that allows mock-first ops without `OPENAI_API_KEY` (AC-10-05/08/09, L10-7/8).

---

## 2) Env contract (interview SSOT)

| Variable | Values / rule |
|----------|----------------|
| `AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER` | `mock` \| `openai`; **unset → `mock`** |
| `AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER` | `mock` \| `openai`; **unset → `mock`**; v1 expected `mock` while live image deferred |
| `AIBRIDGE_ALLOW_MOCK_PROVIDERS` | Explicit allow for mock backends; absent/false → refuse mock |
| `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` | Required for fail-closed **only if** text provider = `openai` |
| `AIBRIDGE_WORKER_IMAGE_POSTER_MODEL` | Required for fail-closed **only if** image provider = `openai` |
| `OPENAI_API_KEY` (and related Present OpenAI settings) | Required for readiness **only if** a selected **worker** provider is `openai`, and/or channel path still requires OpenAI per Present rules |

Unknown provider id → fail-closed (AC-10-05). **No silent OpenAI fallback.**

---

## 3) Production / public board refuse (L10-8, AC-10-09)

| Signal | Rule |
|--------|------|
| Allow flag | `AIBRIDGE_ALLOW_MOCK_PROVIDERS` must be truthy to serve `mock` |
| Default | Without flag → **refuse** mock (public board must not enable flag) |
| Enforce points | **`/readyz` (not ready)** **and** **worker accept** (defense in depth) |

Exact readiness reason / accept fail-class **string** — Open (overview §6); must be explicit and ops-visible, not silent success.

---

## 4) Slot-gated OpenAI presence (L10-7, AC-10-08)

Present as-is always calls `openai_presence_ok()` in `evaluate_readiness` (`readiness.py:138–139`).

**Target:**

| Worker text | Worker image | Channel still live OpenAI? | `OPENAI_API_KEY` for worker readiness |
|-------------|--------------|----------------------------|----------------------------------------|
| `mock` | `mock` | no / N/A for worker gate | **Not required** for worker mock path |
| `openai` | `mock` | — | **Required** (text live) |
| any | `openai` | — | **Required** (when image live exists) |
| `mock` | `mock` | yes (same process) | Channel gate remains Present; worker mock path must not force key solely for worker slots |

Channel/interview registry stays OOS (L10-1); do not break REQ-01/07 interview readiness semantics beyond the conditional worker gate above.

---

## 5) Model-slot fail-closed coexistence

Present `worker_text_brief_fail_closed` / `worker_image_poster_fail_closed` treat empty model as not ready when worker enabled.

**Target nest:** those checks apply when the corresponding provider is `openai`. For `mock`, empty model-id must **not** block readiness solely for that slot.

Other Present worker gates (S2S, storage creds when upload required, enable flag) unchanged by this focus.

---

## 6) Ownership

| Actor | Owns |
|-------|------|
| aibridge Settings / readiness | Parsing env, matrix above, refuse reasons |
| Ops / Railway | Setting selectors + **never** allow-mock on public board |
| gateway | Calls accept only when aibridge ready — does not own provider env |

---

## 7) Not in this doc

NEW STORY; inventing channel env; live image vendor lock date.
