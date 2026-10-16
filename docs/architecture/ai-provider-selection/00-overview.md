# AI provider selection + mock mode (aibridge worker) — target technical architecture (overview)

| Field | Value |
|-------|--------|
| **Focus** | Selectable text-brief / image-poster provider ports + mock mode for REQ-09 worker |
| **Parent REQ** | [`../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md`](../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) |
| **Sibling worker arch** | [`../sense-brief-poster-worker/00-overview.md`](../sense-brief-poster-worker/00-overview.md) (REQ-09 accept/bind Present) |
| **Sibling gateway ops** | [`doge-complaints-gateway/…/58-…-backfill-via-regenerate`](../../../../doge-complaints-gateway/docs/requirements/58-req13-existing-issues-sense-brief-backfill-via-regenerate.md) (mock-first dry run) |
| **Story scope** | none (0 STORY files) |
| **Interview** | [`../../analysis/zeya888.target-tech-arch-interview-ai-provider-selection-2026-10-16.md`](../../analysis/zeya888.target-tech-arch-interview-ai-provider-selection-2026-10-16.md) |
| **Recorded** | 2026-10-16T10:23:21Z |
| **Mode** | Target technical architecture of the focus — not implementation tasks |
| **Slug** | `ai-provider-selection` |
| **Layout** | system (`archDocMode=auto` → ≥3 concerns) |

**Levels:** functional = REQ-10 (AC-10-01…10, L10-1…8) · this folder = how ports / mock / fail-closed are realized in `doge-ai-bridge` · work items = **other prompts** (not here).

---

## 1) Context & functional vs tech split

| Layer | Lives in | Content |
|-------|----------|---------|
| Product | REQ-10 | Goal, OOS, AC, interview locks L10-1…8 |
| Target tech (this package) | `docs/architecture/ai-provider-selection/` | Ports, env SSOT, readyz/accept enforce, verify, coexistence |
| Work items | backlog STORY (other prompts) | **Not here** |

**Use case:** Make worker AI backends an explicit config flip (`mock` ↔ first live `openai` text) so gateway REQ-58 can dry-run / backfill without vendor spend, without rewriting accept/bind HTTP or channel/interview.

**Packaging:** same deployable image as aibridge runtime (`aibridge.app:app`). **Packaging seam N/A** for this focus (no new non-src FS ownership; Git tree = runtime modules under `src/aibridge/`).

---

## 2) Target technical architecture (summary)

```
                    env: TEXT/IMAGE *_PROVIDER + ALLOW_MOCK + model slots
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Settings / provider registry (worker-only; channel OOS)    │
└────────────────────────────┬────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
   TextBriefPort        ImagePosterPort     Readyz + accept
   mock | openai        mock (| openai later)  mock-without-allow refuse
         │                   │
         ▼                   ▼
   Present sense_brief/   Present poster/
   (+ live OpenAI text    (+ deterministic PNG)
    behind openai port)
         │                   │
         └─────────┬─────────┘
                   ▼
            REQ-09 accept → bind (unchanged contracts)
```

**Siblings in this package**

| Doc | Concern |
|-----|---------|
| [`01-provider-ports.md`](./01-provider-ports.md) | Ports, backends, nest with model slots |
| [`02-readyz-env-fail-closed.md`](./02-readyz-env-fail-closed.md) | Env SSOT, allow-mock, slot-gated OpenAI |
| [`03-verify-coexistence.md`](./03-verify-coexistence.md) | Verify surfaces, as-is coexistence, packaging N/A |

---

## 3) Ownership / contracts (decided)

| Artifact class | Owner | Note |
|----------------|-------|------|
| Provider selector env | aibridge ops / Settings | See `02-…` |
| Model-id slots | aibridge (Present REQ-09) | Required **only** when provider=`openai` |
| Mock brief/poster impl | aibridge modules Present | Promote behind port (L10-3/4) |
| Accept / bind HTTP | REQ-09 as-built | Unchanged by this focus |
| Channel / interview OpenAI | REQ-01 / runtime | **OOS** (L10-1) |
| Gateway Issue SSOT | gateway | Unchanged |

---

## 4) Runtime / packaging / verify / env / deploy-residual

| Theme | Decision |
|-------|----------|
| Runtime | Same ASGI process; worker path Present |
| Packaging | **N/A** (same image; no new Git≠image seam) |
| Env | Nested providers + allow-mock — `02-…` |
| Verify | Unit ports + readyz matrix + 1× worker-accept smoke — `03-…` |
| Deploy residual | Public board must **not** set allow-mock; local/CI may |

---

## 5) Coexistence with as-is

| As-is | Cite | Seam |
|-------|------|------|
| Corpus-grounded brief; LLM reserved | `sense_brief/pipeline.py` (module header) | `mock` = Present path; `openai` = first live invoke behind port |
| Deterministic PNG | `poster/image.py` | `mock` image behind port; live image deferred (L10-5) |
| Model slots always fail-closed when worker on | `config.py` / `readiness.py` worker_*_fail_closed | Nest: model-id gate only if provider=`openai` |
| Always `openai_presence_ok()` | `readiness.py:138–139` | Slot-gated when worker providers are mock |
| No multi-provider registry | REQ-10 §3 | **Introduce** worker-only registry |

---

## 6) Open questions

1. Exact **readiness reason** / accept **fail class** token for mock-without-allow (map to existing set or add one — implement / PA.2; not invented as SSOT here beyond «явный»).
2. When to lock live **image** vendor (REQ-10 residual).
3. Channel readiness detail when one process hosts live channel OpenAI + worker mock (coexistence matrix in `02-…`; channel registry still OOS).

---

## 7) Explicit «Not in this doc»

- NEW work items / NEW STORY keys / pkg YAML / P3  
- Product code, stub paths, sample packs  
- Anthropic / Gemini / other live vendors  
- Channel/interview provider registry refactor  
- Gateway bind/nudge contract changes · SPA provider calls  

**Method:** inputs (REQ) ≠ target tech arch ≠ new work items.
