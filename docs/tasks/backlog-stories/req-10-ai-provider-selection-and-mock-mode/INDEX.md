# req-10-ai-provider-selection-and-mock-mode — INDEX

> **Пакет:** REQ-10 — AI provider selection + mock mode (worker)  
> **Parent REQ:** [`REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md`](../../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md)  
> **Parent product:** [`REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md`](../../../../../docs/requirements%20backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md) (worker compute)  
> **Tech-arch:** [`../../../architecture/ai-provider-selection/00-overview.md`](../../../architecture/ai-provider-selection/00-overview.md) (`01`–`03`)  
> **Interview:** [`../../../analysis/zeya888.target-tech-arch-interview-ai-provider-selection-2026-10-16.md`](../../../analysis/zeya888.target-tech-arch-interview-ai-provider-selection-2026-10-16.md)  
> **Sibling worker:** [`req-09-req13-sense-brief-poster-worker`](../req-09-req13-sense-brief-poster-worker/INDEX.md) (STORY-46…50 Present)  
> **Sibling gateway ops:** [`58-…-backfill-via-regenerate`](../../../../../doge-complaints-gateway/docs/requirements/58-req13-existing-issues-sense-brief-backfill-via-regenerate.md)  
> **Emitted:** 2026-10-16T10:29:41Z · materialize from REQ→backlog plan (operator «запиши»)  
> **Code validation + startup:** [`../../../analysis/zeya888.req-10-stories-51-55-code-validation-and-startup-2026-10-16.md`](../../../analysis/zeya888.req-10-stories-51-55-code-validation-and-startup-2026-10-16.md) (2026-10-16T12:27:56Z)  
> **P5 note (2026-10-16T11:59:34Z):** STORY-55 P5 APPLY · TASKED=0 · next **P7** · [p5](../../run-reports/run-summary-20261016-1159-story-aibridge-55-p5-disposition.md)  
> **P1.3 note (2026-10-16T11:52:24Z):** STORY-55 pipeline materialized · **REUSE EPIC-08** · active `pkg-000058` · next **P2** · [p1](../../../../../.cursor/plans/p1_aibridge_55_scaffold_20261016T115046Z.plan.md)  
> **P5 note (2026-10-16T11:44:26Z):** STORY-54 P5 APPLY · TASKED=0 · next **P7** · [p5](../../run-reports/run-summary-20261016-1144-story-aibridge-54-p5-disposition.md)  
> **P1.3 note (2026-10-16T11:33:17Z):** STORY-54 pipeline materialized · **REUSE EPIC-08** · active `pkg-000057` · next **P2** · [p1](../../../../../.cursor/plans/p1_aibridge_54_scaffold_20261016T113216Z.plan.md)  
> **P5 note (2026-10-16T11:28:42Z):** STORY-53 P5 APPLY · TASKED=0 · next **P7** · [p5](../../run-reports/run-summary-20261016-1128-story-aibridge-53-p5-disposition.md)  
> **P3 note (2026-10-16T11:23:50Z):** STORY-53 P3 Done · t08 PASS · next **P4** · [p3](../../run-reports/run-summary-20261016-1123-story-aibridge-53-p3.md)  
> **P1.3 note (2026-10-16T11:18:56Z):** STORY-53 pipeline materialized · **REUSE EPIC-08** · active `pkg-000056` · next **P2** · [p1](../../../../../.cursor/plans/p1_aibridge_53_scaffold_20261016T111732Z.plan.md)  
> **P6 note (2026-10-16T11:13:36Z):** STORY-52 P6 Done · t09 PASS · next **P7** · [p6](../../run-reports/run-summary-20261016-1113-story-aibridge-52-p6.md)  
> **P5 note (2026-10-16T11:11:33Z):** STORY-52 P5 APPLY · TASKED=1 · next **P6** · `run_mode=aibridge_52_audit_20261016` · [p5](../../run-reports/run-summary-20261016-1111-story-aibridge-52-p5-disposition.md)  
> **P3 note (2026-10-16T11:05:47Z):** STORY-52 P3 Done · t08 PASS · next **P4** · [p3](../../run-reports/run-summary-20261016-1105-story-aibridge-52-p3.md)  
> **P1.3 note (2026-10-16T11:03:46Z):** STORY-52 pipeline materialized · **REUSE EPIC-08** · active `pkg-000055` · next **P2** · [p1](../../../../../.cursor/plans/p1_aibridge_52_scaffold_20261016T110222Z.plan.md)  
> **P6 note (2026-10-16T10:58:46Z):** STORY-51 P6 Done · t09 PASS · next **P7** · [p6](../../run-reports/run-summary-20261016-1058-story-aibridge-51-p6.md)  
> **P5 note (2026-10-16T10:56:55Z):** STORY-51 P5 APPLY · TASKED=1 · next **P6** · `run_mode=aibridge_51_audit_20261016` · [p5](../../run-reports/run-summary-20261016-1056-story-aibridge-51-p5-disposition.md)  
> **P3 note (2026-10-16T10:49:56Z):** STORY-51 P3 Done · t08 PASS · next **P4** · [p3](../../run-reports/run-summary-20261016-1049-story-aibridge-51-p3.md)  
> **P1.3 note (2026-10-16T10:46:25Z):** STORY-51 pipeline materialized · **NEW EPIC-08** · active `pkg-000054` · next **P2** · [p1](../../../../../.cursor/plans/p1_aibridge_51_scaffold_20261016T104516Z.plan.md)  
> **Dashboard:** [`../../aibridge-mvp-dashboard.md`](../../aibridge-mvp-dashboard.md)  
> **Operator locks (REQ L10 + arch):** worker-only ports; separate text+image; mock=Present paths; first live=OpenAI text; image mock v1; `{stories}` corpus; readyz mock OK without key; refuse mock without allow flag; env nest per arch `02-…`  
> **Open:** exact readiness/fail-class string for mock-without-allow

## Stories

| Status | Key | Title | Depends |
|--------|-----|-------|---------|
| P8 Done · pkg-000054 | STORY-AIBRIDGE-51-provider-ports-env-registry | [Provider ports + env registry](STORY-AIBRIDGE-51-provider-ports-env-registry.md) · [pipeline](../../epics/EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode/stories/STORY-AIBRIDGE-51-provider-ports-env-registry/STORY-AIBRIDGE-51-provider-ports-env-registry.md) | — |
| P8 Done · pkg-000055 | STORY-AIBRIDGE-52-mock-providers-accept-pipe | [Mock providers on accept pipe](STORY-AIBRIDGE-52-mock-providers-accept-pipe.md) · [pipeline](../../epics/EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode/stories/STORY-AIBRIDGE-52-mock-providers-accept-pipe/STORY-AIBRIDGE-52-mock-providers-accept-pipe.md) | 51 |
| P8 Done · pkg-000056 | STORY-AIBRIDGE-53-readyz-allow-mock-refuse | [Readyz + allow-mock refuse](STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md) · [pipeline](../../epics/EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode/stories/STORY-AIBRIDGE-53-readyz-allow-mock-refuse/STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md) | 51 |
| P8 Done · pkg-000057 | STORY-AIBRIDGE-54-openai-text-live-port | [OpenAI text live port](STORY-AIBRIDGE-54-openai-text-live-port.md) · [pipeline](../../epics/EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode/stories/STORY-AIBRIDGE-54-openai-text-live-port/STORY-AIBRIDGE-54-openai-text-live-port.md) | 51, 52 |
| P5 APPLY · next P7 · TASKED=0 · pkg-000058 | STORY-AIBRIDGE-55-provider-docs-verify-matrix | [Provider docs + verify matrix](STORY-AIBRIDGE-55-provider-docs-verify-matrix.md) · [pipeline](../../epics/EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode/stories/STORY-AIBRIDGE-55-provider-docs-verify-matrix/STORY-AIBRIDGE-55-provider-docs-verify-matrix.md) | 52, 53, 54 |

## Build order

`51 → 52 → 53 → 54 → 55` (53 may run in parallel with 52 after 51)

## Out of package

- Channel/interview provider registry (L10-1)
- Anthropic/Gemini / live image vendor
- Gateway bind/nudge contract changes · SPA provider calls
- Inventing fail-class string as SSOT while Open
- NEW ADMIN / mockups
