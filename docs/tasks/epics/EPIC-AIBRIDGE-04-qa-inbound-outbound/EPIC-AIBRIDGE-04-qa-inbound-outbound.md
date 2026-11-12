# EPIC-AIBRIDGE-04 — QA inbound/outbound data flow

> **ID:** `EPIC-AIBRIDGE-04-qa-inbound-outbound` · **Статус:** 🟡 In Progress (**40** P3 Done · next **P4**)  
> **Package:** [`backlog-stories/qa-inbound-outbound-data-flow/INDEX.md`](../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)  
> **P3 (story 40):** 2026-09-18T14:28:02Z · active `pkg-000039` · next **P4**  
> **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)  
> **Tech:** [`TECHNICAL-ARCHITECTURE.md`](../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md)  
> **Does not modify:** REQ-01/03/05 bodies

## Назначение

QA automated coverage for inbound/outbound data-flow matrix (stories 23–36). Build order per package INDEX: `23 → 24 → … → 35`.

**Не** invent epic-level AC — AC живут в story-файлах (backlog / pipeline).

## Stories

| Status | Key | Path |
|--------|-----|------|
| 🟢 Implemented (P8 closed) | STORY-AIBRIDGE-23-qa-auth-ops-boundaries | [pipeline](stories/STORY-AIBRIDGE-23-qa-auth-ops-boundaries/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md) |
| 🟢 Implemented (P8 closed) | STORY-AIBRIDGE-24-qa-json-schema-boundary | [pipeline](stories/STORY-AIBRIDGE-24-qa-json-schema-boundary/STORY-AIBRIDGE-24-qa-json-schema-boundary.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-24-qa-json-schema-boundary.md) |
| 🟢 Implemented (P7 · next P8) | STORY-AIBRIDGE-25-qa-n8n-telegram-mapping | [pipeline](stories/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md) |
| 🟢 Implemented (P7 · next P8) | STORY-AIBRIDGE-26-qa-idempotency-concurrency | [pipeline](stories/STORY-AIBRIDGE-26-qa-idempotency-concurrency/STORY-AIBRIDGE-26-qa-idempotency-concurrency.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-26-qa-idempotency-concurrency.md) |
| 🟢 Implemented (P8 closed) | STORY-AIBRIDGE-27-qa-openai-prompt-behavior | [pipeline](stories/STORY-AIBRIDGE-27-qa-openai-prompt-behavior/STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md) |
| 🟢 Implemented (P8 closed) | STORY-AIBRIDGE-28-qa-tool-call-validation | [pipeline](stories/STORY-AIBRIDGE-28-qa-tool-call-validation/STORY-AIBRIDGE-28-qa-tool-call-validation.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-28-qa-tool-call-validation.md) |
| 🟢 Implemented (P8 closed) | STORY-AIBRIDGE-29-qa-action-token-fsm | [pipeline](stories/STORY-AIBRIDGE-29-qa-action-token-fsm/STORY-AIBRIDGE-29-qa-action-token-fsm.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-29-qa-action-token-fsm.md) |
| 🟢 Implemented (P3 · next P4) | STORY-AIBRIDGE-30-qa-gateway-continuation | [pipeline](stories/STORY-AIBRIDGE-30-qa-gateway-continuation/STORY-AIBRIDGE-30-qa-gateway-continuation.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-30-qa-gateway-continuation.md) |
| 🟡 Scaffolded (P1.3 · next P2) | STORY-AIBRIDGE-31-qa-restart-lifecycle-retention | [pipeline](stories/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md) |
| 🟢 Implemented (P3 · next P4) | STORY-AIBRIDGE-32-qa-privacy-logs-observability | [pipeline](stories/STORY-AIBRIDGE-32-qa-privacy-logs-observability/STORY-AIBRIDGE-32-qa-privacy-logs-observability.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-32-qa-privacy-logs-observability.md) |
| 🟢 Implemented (P8 closed) | STORY-AIBRIDGE-33-qa-readiness-configuration | [pipeline](stories/STORY-AIBRIDGE-33-qa-readiness-configuration/STORY-AIBRIDGE-33-qa-readiness-configuration.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-33-qa-readiness-configuration.md) |
| ✅ Done (P3 · next P4) | STORY-AIBRIDGE-34-qa-product-journey-scenarios | [pipeline](stories/STORY-AIBRIDGE-34-qa-product-journey-scenarios/STORY-AIBRIDGE-34-qa-product-journey-scenarios.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-34-qa-product-journey-scenarios.md) |
| 🟢 P3 Done (next P4) | STORY-AIBRIDGE-35-qa-gates-layers-dod | [pipeline](stories/STORY-AIBRIDGE-35-qa-gates-layers-dod/STORY-AIBRIDGE-35-qa-gates-layers-dod.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-35-qa-gates-layers-dod.md) |
| 🟢 Implemented (P3 Done · next P4) | STORY-AIBRIDGE-38-qa-oai-channel-error-outcome | [pipeline](stories/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md) |
| 🟢 Implemented (P3 Done · next P4) | STORY-AIBRIDGE-39-qa-char008-send-edit-capture | [pipeline](stories/STORY-AIBRIDGE-39-qa-char008-send-edit-capture/STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md) |
| 🟢 Implemented (P3 Done · next P4) | STORY-AIBRIDGE-40-qa-suite-assert-hygiene | [pipeline](stories/STORY-AIBRIDGE-40-qa-suite-assert-hygiene/STORY-AIBRIDGE-40-qa-suite-assert-hygiene.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-40-qa-suite-assert-hygiene.md) |
| 🟢 Implemented (P3 Done · next P4) | STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence | [pipeline](stories/STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence/STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md) |
| 🟢 Implemented (P7 wave complete) | STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty | [pipeline](stories/STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty/STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md) · [backlog](../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md) |

## Порядок

`23 → 24 → 25 → 26 → 27 → 28 → 29 → 30 → 31 → … → 40`. Active wave: **story 40** (`pkg-000039`) — P3 Done · next **P4**.

## Non-goals этой волны

- Delete/move package `fixtures/` originals (promote = copy only).
- Railway SUCCESS invent; live Telegram in default CI.
- Silent product invent for ACT-* (guide must-style).
- Moving FSM/OpenAI/gateway ownership into n8n.
