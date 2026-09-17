# AI Bridge — backlog stories INDEX

**Профиль:** `aibridge` · **Focus:** `doge-ai-bridge/`  
**Bullrun:** [bullrun-launch-index.md](../bullrun-launch-index.md)  
**Requirement SSOT:** [REQ-01](../../requirements/REQ-01-doge-ai-bridge-runtime.md) · [REQ-03](../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) · [REQ-05](../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2.0 · Parent protocol [GPT UI REQ-47](../../../../GPT%20UI/docs/requirements/REQ-47-responses-api-https-bearer-bridge.md) · QA [inbound/outbound guide](../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)  
**Architecture:** [runtime/00-overview.md](../../architecture/runtime/00-overview.md)  
**Dashboard:** [aibridge-mvp-dashboard.md](../aibridge-mvp-dashboard.md)  
**Updated:** 2026-09-17T14:30:00Z

## Packages

| Package | Progress | Notes |
|---------|----------|-------|
| [req-01-runtime](req-01-runtime/INDEX.md) | 6/6 core Done · 07/08 Superseded | REQ-01 pilot |
| [req-03-runtime-remediation](req-03-runtime-remediation/INDEX.md) | 9/9 active Done · Deferred 18 | REQ-03 |
| [req-05-content-phase-a-flat-launch](req-05-content-phase-a-flat-launch/INDEX.md) | 0/4 Todo | REQ-05 v0.2.0 |
| [qa-inbound-outbound-data-flow](qa-inbound-outbound-data-flow/INDEX.md) | 0/13 Todo | QA guide statement · matrix 186 IDs · **next QA** |

## Stories (flat)

| Status | Key | Package |
|--------|-----|---------|
| Done | [STORY-AIBRIDGE-01-channel-facade-auth](req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md) | req-01-runtime |
| Done | [STORY-AIBRIDGE-02-content-bundle-registry](req-01-runtime/STORY-AIBRIDGE-02-content-bundle-registry.md) | req-01-runtime |
| Done | [STORY-AIBRIDGE-03-responses-tool-budgets](req-01-runtime/STORY-AIBRIDGE-03-responses-tool-budgets.md) | req-01-runtime |
| Done | [STORY-AIBRIDGE-04-dual-confirm-tokens](req-01-runtime/STORY-AIBRIDGE-04-dual-confirm-tokens.md) | req-01-runtime |
| Done | [STORY-AIBRIDGE-05-gateway-outcomes](req-01-runtime/STORY-AIBRIDGE-05-gateway-outcomes.md) | req-01-runtime |
| Done | [STORY-AIBRIDGE-06-ops-wave1-proof](req-01-runtime/STORY-AIBRIDGE-06-ops-wave1-proof.md) | req-01-runtime |
| Superseded | [STORY-AIBRIDGE-07-replayable-history-postgres](req-01-runtime/STORY-AIBRIDGE-07-replayable-history-postgres.md) | → AIBRIDGE-09 |
| Superseded | [STORY-AIBRIDGE-08-confirm-token-persistence](req-01-runtime/STORY-AIBRIDGE-08-confirm-token-persistence.md) | → AIBRIDGE-09 |
| Done | [STORY-AIBRIDGE-09-postgres-ssot-migrations](req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md) | req-03-runtime-remediation |
| Done | [STORY-AIBRIDGE-10-responses-adapter-tools](req-03-runtime-remediation/STORY-AIBRIDGE-10-responses-adapter-tools.md) | req-03-runtime-remediation |
| Done | [STORY-AIBRIDGE-11-coordinator-pause-resume-send](req-03-runtime-remediation/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md) | req-03-runtime-remediation |
| Done | [STORY-AIBRIDGE-12-readyz-env-dryrun-gate](req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md) | req-03-runtime-remediation |
| Done | [STORY-AIBRIDGE-13-wave1-asgi-e2e](req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md) | req-03-runtime-remediation |
| Done | [STORY-AIBRIDGE-14-p1-ops-schema-restart](req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md) | req-03-runtime-remediation |
| Done | [STORY-AIBRIDGE-15-n8n-telegram-gate](req-03-runtime-remediation/STORY-AIBRIDGE-15-n8n-telegram-gate.md) | req-03-runtime-remediation |
| Done | [STORY-AIBRIDGE-16-privacy-retention](req-03-runtime-remediation/STORY-AIBRIDGE-16-privacy-retention.md) | req-03-runtime-remediation |
| Done | [STORY-AIBRIDGE-17-spa-https-continuation-e2e](req-03-runtime-remediation/STORY-AIBRIDGE-17-spa-https-continuation-e2e.md) | req-03-runtime-remediation (spa evidence BLOCKED) |
| Deferred | [STORY-AIBRIDGE-18-p2-replicas-observability](req-03-runtime-remediation/STORY-AIBRIDGE-18-p2-replicas-observability.md) | req-03-runtime-remediation |
| Todo | [STORY-AIBRIDGE-19-assembled-instructions-engine-wire](req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md) | req-05-content-phase-a-flat-launch |
| Todo | [STORY-AIBRIDGE-20-full-instructions-manifest](req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md) | req-05-content-phase-a-flat-launch |
| Todo | [STORY-AIBRIDGE-21-oas-image-env-docs](req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-21-oas-image-env-docs.md) | req-05-content-phase-a-flat-launch |
| Todo | [STORY-AIBRIDGE-22-content-phase-a-proof](req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-22-content-phase-a-proof.md) | req-05-content-phase-a-flat-launch |
| Todo | [STORY-AIBRIDGE-23-qa-auth-ops-boundaries](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md) | qa-inbound-outbound-data-flow |
| Todo | [STORY-AIBRIDGE-24-qa-json-schema-boundary](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-24-qa-json-schema-boundary.md) | qa-inbound-outbound-data-flow |
| Todo | [STORY-AIBRIDGE-25-qa-n8n-telegram-mapping](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md) | qa-inbound-outbound-data-flow |
| Todo | [STORY-AIBRIDGE-26-qa-idempotency-concurrency](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-26-qa-idempotency-concurrency.md) | qa-inbound-outbound-data-flow |
| Todo | [STORY-AIBRIDGE-27-qa-openai-prompt-behavior](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md) | qa-inbound-outbound-data-flow |
| Todo | [STORY-AIBRIDGE-28-qa-tool-call-validation](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-28-qa-tool-call-validation.md) | qa-inbound-outbound-data-flow |
| Todo | [STORY-AIBRIDGE-29-qa-action-token-fsm](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-29-qa-action-token-fsm.md) | qa-inbound-outbound-data-flow |
| Todo | [STORY-AIBRIDGE-30-qa-gateway-continuation](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-30-qa-gateway-continuation.md) | qa-inbound-outbound-data-flow |
| Todo | [STORY-AIBRIDGE-31-qa-restart-lifecycle-retention](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md) | qa-inbound-outbound-data-flow |
| Todo | [STORY-AIBRIDGE-32-qa-privacy-logs-observability](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-32-qa-privacy-logs-observability.md) | qa-inbound-outbound-data-flow |
| Todo | [STORY-AIBRIDGE-33-qa-readiness-configuration](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-33-qa-readiness-configuration.md) | qa-inbound-outbound-data-flow |
| Todo | [STORY-AIBRIDGE-34-qa-product-journey-scenarios](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-34-qa-product-journey-scenarios.md) | qa-inbound-outbound-data-flow |
| Todo | [STORY-AIBRIDGE-35-qa-gates-layers-dod](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-35-qa-gates-layers-dod.md) | qa-inbound-outbound-data-flow |

## Build order

**REQ-01 (Done):** `01 → 02 → 03 → 04 → 05 → 06`

**REQ-03:** `09 → 10 → 11 ∥ 12 → 13 → 14 ∥ 15 → 16 → 17` · Deferred `18` after first node

**REQ-05:** `19 ∥ 20 ∥ 21 → 22`

**QA inbound/outbound:** `23 → 24 → 25 ∥ 26 → 27 → 28 → 29 → 30 → 31 ∥ 32 → 33 → 34 → 35`

Out of this INDEX active set: [REQ-02](../../requirements/REQ-02-DOGE-AI-BRIDGE-POST-PILOT-EVOLUTION.md), [REQ-06](../../requirements/REQ-06-CONTENT-PHASE-B-SCALABLE-PACKAGING.md) (after REQ-05), ADMIN/*, mockups, optional token-hash UX.
