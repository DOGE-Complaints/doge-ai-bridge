# EPIC-AIBRIDGE-08 — REQ-10 AI provider selection + mock mode

> **ID:** `EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode` · **Статус:** 🟡 In Progress (**STORY-55** P5 APPLY · next **P7**)  
> **Package:** [`backlog-stories/req-10-ai-provider-selection-and-mock-mode/INDEX.md`](../../backlog-stories/req-10-ai-provider-selection-and-mock-mode/INDEX.md)  
> **P5 (story 55):** 2026-10-16T11:59:34Z · TASKED=0 · activation **none** · next **P7**  
> **P4 (story 55):** 2026-10-16T11:57:23Z · AC PASS · OPEN G-01 Info  
> **P3 (story 55):** 2026-10-16T11:55:32Z · gate PASS · `pkg-000058` · tests 573  
> **P1.3 (story 55):** 2026-10-16T11:52:24Z · active `pkg-000058` · **REUSE** epic  
> **P8 (story 54):** 2026-10-16T11:48:21Z · SHAs e5cde7a/489a428/e187871  
> **P5 (story 54):** 2026-10-16T11:44:26Z · TASKED=0 · activation **none** · next **P7**  
> **P4 (story 54):** 2026-10-16T11:40:58Z · AC PASS · OPEN G-01 Info  
> **P3 (story 54):** 2026-10-16T11:37:56Z · gate PASS · `pkg-000057` · residual live SUCCESS Unknown  
> **P1.3 (story 54):** 2026-10-16T11:33:17Z · active `pkg-000057` · **REUSE** epic  
> **P5 (story 53):** 2026-10-16T11:28:42Z · TASKED=0 · activation **none** · next **P7**  
> **P3 (story 53):** 2026-10-16T11:23:50Z · gate PASS · `pkg-000056`  
> **P1.3 (story 53):** 2026-10-16T11:18:56Z · active `pkg-000056` · **REUSE** epic  
> **P6 (story 52):** 2026-10-16T11:13:36Z · t09 Done · next **P7**  
> **P5 (story 52):** 2026-10-16T11:11:33Z · TASKED=1 · `run_mode=aibridge_52_audit_20261016`  
> **P3 (story 52):** 2026-10-16T11:05:47Z · gate PASS · `pkg-000055`  
> **P1.3 (story 52):** 2026-10-16T11:03:46Z · active `pkg-000055` · **REUSE** epic  
> **P6 (story 51):** 2026-10-16T10:58:46Z · t09 Done · next **P7**  
> **P5 (story 51):** 2026-10-16T10:56:55Z · TASKED=1 · `run_mode=aibridge_51_audit_20261016`  
> **P3 (story 51):** 2026-10-16T10:49:56Z · gate PASS · `pkg-000054`  
> **P1.3 (story 51):** 2026-10-16T10:46:25Z · active `pkg-000054` · **NEW** epic  
> **Parent REQ:** [`REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md`](../../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md)  
> **Tech:** [`docs/architecture/ai-provider-selection/`](../../../architecture/ai-provider-selection/) (`00`–`03`)  
> **Does not modify:** EPIC-07 REQ-09 bodies · channel/interview registry (L10-1)

## Назначение

REQ-10: worker-only selectable text/image providers (`mock`|`openai`), env nest, mock-first, fail-closed unknown, allow-mock refuse, OpenAI text live later. Build order `51 → 52 → 53 → 54 → 55`.

**Не** invent epic-level AC — AC живут в story-файлах.  
**Не** invent exact module path / fail-class string SSOT while Open.

## Stories

| Status | Key | Path |
|--------|-----|------|
| 🟢 P8 Done · pkg-000054 | STORY-AIBRIDGE-51-provider-ports-env-registry | [pipeline](stories/STORY-AIBRIDGE-51-provider-ports-env-registry/STORY-AIBRIDGE-51-provider-ports-env-registry.md) · [backlog](../../backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-51-provider-ports-env-registry.md) |
| 🟢 P8 Done · pkg-000055 | STORY-AIBRIDGE-52-mock-providers-accept-pipe | [pipeline](stories/STORY-AIBRIDGE-52-mock-providers-accept-pipe/STORY-AIBRIDGE-52-mock-providers-accept-pipe.md) · [backlog](../../backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-52-mock-providers-accept-pipe.md) |
| 🟢 P8 Done · pkg-000056 | STORY-AIBRIDGE-53-readyz-allow-mock-refuse | [pipeline](stories/STORY-AIBRIDGE-53-readyz-allow-mock-refuse/STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md) · [backlog](../../backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md) |
| 🟢 P8 Done · pkg-000057 | STORY-AIBRIDGE-54-openai-text-live-port | [pipeline](stories/STORY-AIBRIDGE-54-openai-text-live-port/STORY-AIBRIDGE-54-openai-text-live-port.md) · [backlog](../../backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-54-openai-text-live-port.md) |
| 🟡 P5 APPLY · next P7 · TASKED=0 · pkg-000058 | STORY-AIBRIDGE-55-provider-docs-verify-matrix | [pipeline](stories/STORY-AIBRIDGE-55-provider-docs-verify-matrix/STORY-AIBRIDGE-55-provider-docs-verify-matrix.md) · [backlog](../../backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-55-provider-docs-verify-matrix.md) |

## Порядок

`51 → 52 → 53 → 54 → 55`. Active wave: **STORY-55** (`pkg-000058`) — P5 APPLY · next **P7** (skip P6).

## Non-goals этой волны (P1)

- Product runtime code в P1 (только task queue).
- Invent live OpenAI SUCCESS without credentials (residual OK) · live image · STORY-55.
- Materialize 55 in this pkg.
