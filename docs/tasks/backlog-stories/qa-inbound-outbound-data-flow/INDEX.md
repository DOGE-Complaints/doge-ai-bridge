# qa-inbound-outbound-data-flow — INDEX

> **Пакет:** QA automated coverage — inbound/outbound data flow (statement only)
> **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) (2026-09-17)
> **Channel OAS:** `docs/openapi/aibridge-channel-v1.openapi.yaml` · **Gateway OAS:** `docs/openapi/story-intake-actions.openapi.yaml`
> **Traceability:** [`TRACEABILITY-MATRIX.md`](./TRACEABILITY-MATRIX.md) · **Coverage check:** [`MATRIX-COVERAGE-VERIFICATION.md`](./MATRIX-COVERAGE-VERIFICATION.md)
> **Emitted:** 2026-09-17 · operator ask: постановка + юзкейсы + матрица; **без реализации**
> **Does not modify:** REQ-01/03/05 bodies; no epic pipeline materialize

## Stories

| Status | Key | Title | Matrix |
|--------|-----|-------|--------|
| Todo | `STORY-AIBRIDGE-23-qa-auth-ops-boundaries` | [QA — Authentication and operational boundaries](STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md) | 12 IDs |
| Todo | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | [QA — JSON and schema boundary](STORY-AIBRIDGE-24-qa-json-schema-boundary.md) | 18 IDs |
| Todo | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | [QA — n8n and Telegram mapping](STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md) | 18 IDs |
| Todo | `STORY-AIBRIDGE-26-qa-idempotency-concurrency` | [QA — Idempotency and concurrency](STORY-AIBRIDGE-26-qa-idempotency-concurrency.md) | 10 IDs |
| Todo | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | [QA — OpenAI and prompt behavior](STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md) | 16 IDs |
| Todo | `STORY-AIBRIDGE-28-qa-tool-call-validation` | [QA — Tool-call validation](STORY-AIBRIDGE-28-qa-tool-call-validation.md) | 14 IDs |
| Todo | `STORY-AIBRIDGE-29-qa-action-token-fsm` | [QA — Action token and dual-confirm FSM](STORY-AIBRIDGE-29-qa-action-token-fsm.md) | 18 IDs |
| Todo | `STORY-AIBRIDGE-30-qa-gateway-continuation` | [QA — Gateway and SPA continuation](STORY-AIBRIDGE-30-qa-gateway-continuation.md) | 20 IDs |
| Todo | `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention` | [QA — Restart, lifecycle, and retention](STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md) | 12 IDs |
| Todo | `STORY-AIBRIDGE-32-qa-privacy-logs-observability` | [QA — Privacy, logs, and observability](STORY-AIBRIDGE-32-qa-privacy-logs-observability.md) | 10 IDs |
| Todo | `STORY-AIBRIDGE-33-qa-readiness-configuration` | [QA — Readiness and configuration](STORY-AIBRIDGE-33-qa-readiness-configuration.md) | 15 IDs |
| Todo | `STORY-AIBRIDGE-34-qa-product-journey-scenarios` | [QA — Product-journey scenarios (UC-01…10)](STORY-AIBRIDGE-34-qa-product-journey-scenarios.md) | 10 IDs |
| Todo | `STORY-AIBRIDGE-35-qa-gates-layers-dod` | [QA — Test layers, gates, fixtures, characterization DoD](STORY-AIBRIDGE-35-qa-gates-layers-dod.md) | 13 IDs |

## Build order (statement / future automation waves)

`23 → 24 → 25 ∥ 26 → 27 → 28 → 29 → 30 → 31 ∥ 32 → 33 → 34 → 35`

## Out of package

- Implementing pytest/n8n/live suites (later waves)
- Nested `task-*` / epic folders until explicit P1
- REQ-06 / ADMIN / mockups
