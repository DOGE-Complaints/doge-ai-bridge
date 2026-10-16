# REQ-10 — AI provider selection and mock mode (sense-brief / poster)

Parent product context: [REQ13](../../../docs/requirements%20backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md) (worker compute; vendor not locked at root)  
Sibling worker: [`REQ-09`](./REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) (accept + brief + poster + bind Present)  
Sibling gateway ops: [`58-…-backfill-via-regenerate`](../../../doge-complaints-gateway/docs/requirements/58-req13-existing-issues-sense-brief-backfill-via-regenerate.md) (regenerate/backfill; mock-first dry run)  
Related — style pack (future image input): [REQ14](../../../docs/requirements%20backlog/REQ14-DOGEstonia-Civic-Poster-Style-Pack-And-Image-Instructions.md) — style bible + visual refs / design system; mount when live image enabled (does not expand this REQ’s scope)  
Related channel runtime: [`REQ-01`](./REQ-01-doge-ai-bridge-runtime.md) (interview stays OpenAI-only in this REQ — lock §6)  
Architecture: [`../architecture/ai-provider-selection/00-overview.md`](../architecture/ai-provider-selection/00-overview.md) · interview [`../analysis/zeya888.target-tech-arch-interview-ai-provider-selection-2026-10-16.md`](../analysis/zeya888.target-tech-arch-interview-ai-provider-selection-2026-10-16.md)  
**Related — Backlog:** [`../tasks/backlog-stories/req-10-ai-provider-selection-and-mock-mode/INDEX.md`](../tasks/backlog-stories/req-10-ai-provider-selection-and-mock-mode/INDEX.md) (STORY-AIBRIDGE-51…55)  
Status: Draft — **interview locks closed** 2026-10-16 · tech-arch + backlog materialized 2026-10-16 · awaiting PA.2  
Дата: 2026-10-15 · Locks: 2026-10-16 · Arch: 2026-10-16T10:23:21Z · Backlog: 2026-10-16T10:29:41Z

---

## 1) Goal

Сделать выбор **AI-провайдера** явной конфигурацией aibridge (не «вшит только OpenAI»), и среди провайдеров иметь **mock-режим**: тот же worker pipe (accept → brief → poster → bind), но **без** вызова платного vendor API — чтобы отладить backfill и интеграцию gateway↔aibridge без траты токенов.

Долгосрочно: добавить/сменить live-провайдера (text и/или image) без переписывания worker entry и bind contracts.

## 2) Scope / Out of scope

**In scope**

- Provider **ports** for REQ-09 worker only: **text-brief** and **image-poster** as **separate** selectors (`TEXT_PROVIDER` / `IMAGE_PROVIDER` — exact env names PA.2).
- Selectable backends per slot: at least **`mock`** and first live **`openai`** (text); image live may lag (lock §6).
- Mock = promote Present deterministic paths (corpus-grounded brief extraction + minimal PNG) behind the port — not a third parallel fake.
- Live text: receive gateway `{stories:[…]}` corpus and extract L2 brief (paired with gateway REQ-58 L58-3).
- Config flip mock↔live without changing accept/bind HTTP; fail-closed on unknown/incomplete config; **no silent OpenAI fallback**.
- `/ready`: mock mode allowed **without** `OPENAI_API_KEY`.
- Production safety: refuse `mock` on production/public board unless explicit override flag.
- Docs: mock-first ops order with gateway REQ-58.

**Out of scope**

- Refactoring channel/interview onto the same registry in this REQ (stays OpenAI Responses as today).
- Implementing Anthropic/Gemini/etc. in v1 — only **port + mock + first OpenAI live text** (image live optional later).
- Changing gateway bind/nudge contracts.
- SPA calling providers.
- Defaulting Railway public board to mock without override.

## 3) Verified current state

| Fact | Path / note |
|------|-------------|
| Channel / interview OpenAI | [`app.py`](../../src/aibridge/app.py) wires `ProductionResponsesClient` when `OPENAI_API_KEY` Present; env `OPENAI_*` in [`config.py`](../../src/aibridge/config.py) |
| Worker sense-brief text | [`sense_brief/pipeline.py`](../../src/aibridge/sense_brief/pipeline.py): corpus-grounded extraction; **live LLM invoke reserved for later**; `text_brief_model` slot required |
| Worker poster image | [`poster/image.py`](../../src/aibridge/poster/image.py): deterministic minimal PNG; **live image-vendor invoke reserved for later**; `image_poster_model` slot required |
| Storage mockability | [`poster/storage.py`](../../src/aibridge/poster/storage.py): injectable `PosterUploadPort` / HTTPS mint for fixtures |
| Isolation harness | Story-50 tests mock peers; **not** runtime selectable mock provider for local-five/ops |
| Multi-provider registry | **Absent** as first-class worker config |

**Implication:** This REQ introduces ports + mock as first-class config, and plugs **first live text** invoke behind the same port so mock↔live is a flip. Live image may remain mock/deterministic longer.

## 4) Target behavior

1. Operator sets **text** and **image** provider ids independently (e.g. `mock` | `openai`).
2. **`mock` text:** L2 from Present corpus-grounded / fixture strategy for `{stories}` or L2-shaped corpus; no vendor HTTP.
3. **`mock` image:** Present deterministic PNG (or equivalent under port); upload/bind still real where possible.
4. **`openai` text:** live extract L2 from `{stories:[…]}`; failures map to existing `reason_class`.
5. **Image live:** deferred until explicit later lock; v1 default image provider = `mock` even when text = `openai` (spot-check quality on brief first).
6. Misconfig → fail-closed; production + `mock` without override → refuse.
7. Channel/interview unchanged by this REQ.
8. Gateway REQ-58: dry-run/backfill against mock → one Issue with live text → batch.

## 5) Acceptance criteria

| ID | Criterion |
|----|-----------|
| **AC-10-01** | Worker text slot resolves via selectable provider port |
| **AC-10-02** | Worker image slot resolves via selectable provider port (independent of text) |
| **AC-10-03** | `mock` text + `mock` image: accept→brief→poster→bind without live vendor HTTP |
| **AC-10-04** | Switching text mock↔openai is config/env only; same accept API |
| **AC-10-05** | Unknown / incomplete provider config fail-closed (no silent OpenAI fallback) |
| **AC-10-06** | Mock outputs L2-valid + poster HTTPS bindable |
| **AC-10-07** | Docs: provider list + mock-first order with gateway REQ-58 |
| **AC-10-08** | With both slots `mock`, `/ready` does not require `OPENAI_API_KEY` |
| **AC-10-09** | Production/public refuses `mock` unless explicit override |
| **AC-10-10** | Live text accepts gateway `{stories:[…]}` and produces L2 (or honest `corpus_insufficient`) |

## 6) Interview locks (closed 2026-10-16)

Operator accepted architect recommendations.

| ID | Lock |
|----|------|
| **L10-1** | Ports scope = **worker only** (channel/interview not in this REQ) |
| **L10-2** | Granularity = separate **text** + **image** provider selectors |
| **L10-3** | Mock text = Present corpus-grounded / fixture path behind the port |
| **L10-4** | Mock image = Present deterministic PNG (or equivalent) behind the port |
| **L10-5** | First live = **OpenAI text**; **image stays mock** until a later explicit live-image lock |
| **L10-6** | Corpus = gateway `{stories:[…]}`; worker extracts L2 (with REQ-58 L58-3) |
| **L10-7** | Readyz = mock mode **OK without** `OPENAI_API_KEY` |
| **L10-8** | Production = **refuse mock** unless explicit override flag |

**Residual Open (PA.2 / ops naming only):** exact env var names; override flag name; when to add live image vendor.

## 7) Dependencies

- REQ-09 worker entry, bind client, reason_class set.
- Gateway REQ-58 (corpus on regenerate + CLI batch; mock-first order).
- Orthogonal: REQ-01/07 channel OpenAI — do not break interview.
- Storage/CDN ids remain ops Open (upload port already injectable).
