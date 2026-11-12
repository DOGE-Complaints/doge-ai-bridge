# req-12-req15-interview-deepseek-openai-providers — INDEX

> **Пакет:** REQ-12 — REQ15 interview DeepSeek \| OpenAI providers  
> **Parent REQ:** [`REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md`](../../../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md)  
> **Parent product:** [`REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md`](../../../../../docs/requirements%20backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md)  
> **Tech-arch:** [`../../../architecture/req15-interview-providers/00-overview.md`](../../../architecture/req15-interview-providers/00-overview.md) (`01`–`03`) · ≠ worker [`../../../architecture/ai-provider-selection/00-overview.md`](../../../architecture/ai-provider-selection/00-overview.md)  
> **Interview:** [`../../../analysis/zeya888.target-tech-arch-interview-req15-interview-providers-2026-11-01.md`](../../../analysis/zeya888.target-tech-arch-interview-req15-interview-providers-2026-11-01.md)  
> **T1 / readiness:** [`../../../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md`](../../../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md) · [`req15-aibridge-wave-readiness-2026-11-01.md`](../../../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md)  
> **Emitted:** 2026-11-01T19:38:04Z · materialize from REQ→backlog plan (operator env lock L12-3 + dashboard recount)  
> **Tech subtasks:** Present in STORY-59/60/61; **61 Done · Product Done** → EPIC-10 · `pkg-000064` · P8 `05609c2`/`d45d872`/`a8b064c` · residual AC-04 live Explicit Partial  
> **Dashboard:** [`../../aibridge-mvp-dashboard.md`](../../aibridge-mvp-dashboard.md)  
> **Operator locks:** L12-1 selector · L12-2 model orient · **L12-3** DeepSeek nest names · D2 fail-closed unset · D3 Keep Engine · D4 wire/start only · D5 stub/live split  
> **Env template:** [`../../../../.env.example`](../../../../.env.example) §4b  
> **Honesty:** stub ≠ AC-AIB-12-04 / Product Done; stub harness ≠ live Done; live Pass per provider only when ops window open + recorded path; this wave live = **Explicit Partial**; **no invent** Railway / live SUCCESS · runtime: [`../../../runtime-docs/08-ac04-interview-stub-live-evidence-gates.md`](../../../runtime-docs/08-ac04-interview-stub-live-evidence-gates.md)

## Stories

| Status | Key | Title | Depends |
|--------|-----|-------|---------|
| **Done** · Product Done · pkg-000062 | STORY-AIBRIDGE-59-interview-port-env-fail-closed | [Interview port + env fail-closed](STORY-AIBRIDGE-59-interview-port-env-fail-closed.md) · [pipeline](../../epics/EPIC-AIBRIDGE-10-req-12-req15-interview-deepseek-openai-providers/stories/STORY-AIBRIDGE-59-interview-port-env-fail-closed/STORY-AIBRIDGE-59-interview-port-env-fail-closed.md) | — |
| **Done** · Product Done · pkg-000063 | STORY-AIBRIDGE-60-openai-deepseek-interview-adapters | [OpenAI + DeepSeek interview adapters](STORY-AIBRIDGE-60-openai-deepseek-interview-adapters.md) · [pipeline](../../epics/EPIC-AIBRIDGE-10-req-12-req15-interview-deepseek-openai-providers/stories/STORY-AIBRIDGE-60-openai-deepseek-interview-adapters/STORY-AIBRIDGE-60-openai-deepseek-interview-adapters.md) | 59 |
| **Done** · Product Done · pkg-000064 · live Explicit Partial residual | STORY-AIBRIDGE-61-interview-provider-stub-live-evidence | [Stub + live evidence gates](STORY-AIBRIDGE-61-interview-provider-stub-live-evidence.md) · [pipeline](../../epics/EPIC-AIBRIDGE-10-req-12-req15-interview-deepseek-openai-providers/stories/STORY-AIBRIDGE-61-interview-provider-stub-live-evidence/STORY-AIBRIDGE-61-interview-provider-stub-live-evidence.md) · [runtime 08](../../../runtime-docs/08-ac04-interview-stub-live-evidence-gates.md) · [p7 reaudit](../../../analysis/p7-reaudit-STORY-AIBRIDGE-61-interview-provider-stub-live-evidence-20261101.md) | 59 · soft 60 |

## Build order

`59 → 60 → 61`

## Out of package

- Worker REQ-10 / `AIBRIDGE_WORKER_*_PROVIDER`
- REQ-11 confirm/stash (Keep peer)
- REQ-13 roles body / GPT-48 instructions
- telegram transport · gateway redesign · NEW ADMIN / mockups
