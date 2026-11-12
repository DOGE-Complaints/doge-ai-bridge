# EPIC-AIBRIDGE-10 — REQ-12 / REQ15 interview DeepSeek | OpenAI providers

> **ID:** `EPIC-AIBRIDGE-10-req-12-req15-interview-deepseek-openai-providers` · **Статус:** 🟡 In Progress (**STORY-61** P3 Done · gate PASS · live Explicit Partial · next **P4**)  
> **P3 (story 61):** 2026-11-01T21:18:31Z · active `pkg-000064` · **REUSE** epic  
> **Package:** [`backlog-stories/req-12-req15-interview-deepseek-openai-providers/INDEX.md`](../../backlog-stories/req-12-req15-interview-deepseek-openai-providers/INDEX.md)  
> **Parent REQ:** [`REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md`](../../../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md)  
> **Tech:** [`docs/architecture/req15-interview-providers/`](../../../architecture/req15-interview-providers/) (`00`–`03`) · ≠ worker [`ai-provider-selection`](../../../architecture/ai-provider-selection/00-overview.md)  
> **Does not modify:** EPIC-08 REQ-10 · EPIC-09 REQ-11 bodies · merge interview into `providers/`

## Назначение

REQ-12 / REQ15: interview port + env fail-closed (59 Done) · adapters (60 Done) · stub/live evidence (61). Build order `59 → 60 → 61`.

**Не** invent epic-level AC — AC живут в story-файлах.  
**Не** invent live SUCCESS / Railway Pass without ops window → Explicit Partial OK.

## Stories

| Status | Key | Path |
|--------|-----|------|
| 🟢 Done · pkg-000062 · P8 | STORY-AIBRIDGE-59-interview-port-env-fail-closed | [pipeline](stories/STORY-AIBRIDGE-59-interview-port-env-fail-closed/STORY-AIBRIDGE-59-interview-port-env-fail-closed.md) · [backlog](../../backlog-stories/req-12-req15-interview-deepseek-openai-providers/STORY-AIBRIDGE-59-interview-port-env-fail-closed.md) |
| 🟢 Done · pkg-000063 · P8 | STORY-AIBRIDGE-60-openai-deepseek-interview-adapters | [pipeline](stories/STORY-AIBRIDGE-60-openai-deepseek-interview-adapters/STORY-AIBRIDGE-60-openai-deepseek-interview-adapters.md) · [backlog](../../backlog-stories/req-12-req15-interview-deepseek-openai-providers/STORY-AIBRIDGE-60-openai-deepseek-interview-adapters.md) |
| 🟡 P3 Done · gate PASS · live Explicit Partial · pkg-000064 · next P4 | STORY-AIBRIDGE-61-interview-provider-stub-live-evidence | [pipeline](stories/STORY-AIBRIDGE-61-interview-provider-stub-live-evidence/STORY-AIBRIDGE-61-interview-provider-stub-live-evidence.md) · [backlog](../../backlog-stories/req-12-req15-interview-deepseek-openai-providers/STORY-AIBRIDGE-61-interview-provider-stub-live-evidence.md) |

## Порядок

`59 → 60 → 61`. Active wave: **STORY-61** (`pkg-000064`) — P3 Done · gate **PASS** · live **Explicit Partial** · next **P4**.

## Non-goals этой волны

- Opening ops window · invent Railway / live SUCCESS.
- Re-implement adapters (60 Done) · port/env invent (59 Done).
