# AI Bridge — backlog stories INDEX

**Профиль:** `aibridge` · **Focus:** `doge-ai-bridge/`  
**Bullrun:** [bullrun-launch-index.md](../bullrun-launch-index.md)  
**Requirement SSOT:** [REQ-01](../../requirements/REQ-01-doge-ai-bridge-runtime.md) · [REQ-03](../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) · [REQ-05](../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) · [REQ-07](../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) · [REQ-08](../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) · [REQ-09](../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) · [REQ-10](../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) · [REQ-11](../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) · [REQ-12](../../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) · [REQ-13](../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) · Parent protocol [GPT UI REQ-47](../../../../GPT%20UI/docs/requirements/REQ-47-responses-api-https-bearer-bridge.md) · QA [inbound/outbound guide](../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)  
**Architecture:** [runtime/00-overview.md](../../architecture/runtime/00-overview.md) · [TECH-ARCH-REQ-07](../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) · [req9-ops-naming](../../../../docs/architecture/req9-ops-naming/00-overview.md) · [sense-brief-poster-worker](../../architecture/sense-brief-poster-worker/00-overview.md) · [ai-provider-selection](../../architecture/ai-provider-selection/00-overview.md) · [req15-dual-confirm-handoff](../../architecture/req15-dual-confirm-handoff/00-overview.md) · [req15-interview-providers](../../architecture/req15-interview-providers/00-overview.md) · [req15-semantic-state-roles](../../architecture/req15-semantic-state-roles/00-overview.md)  
**Dashboard:** [aibridge-mvp-dashboard.md](../aibridge-mvp-dashboard.md)  
**Updated:** 2026-11-02T08:32:08Z

## Packages

| Package | Progress | Notes |
|---------|----------|-------|
| [req-01-runtime](req-01-runtime/INDEX.md) | 6/6 core Done · 07/08 Superseded | REQ-01 pilot |
| [req-03-runtime-remediation](req-03-runtime-remediation/INDEX.md) | 9/9 active Done · Deferred 18 | REQ-03 |
| [req-05-content-phase-a-flat-launch](req-05-content-phase-a-flat-launch/INDEX.md) | 4/4 Implemented | REQ-05 Phase A |
| [qa-inbound-outbound-data-flow](qa-inbound-outbound-data-flow/INDEX.md) | 17 Done/Implemented · 1 Scaffolded (33) | QA guide · EPIC-04 |
| [req-07-openai-strict-schema-compat](req-07-openai-strict-schema-compat/INDEX.md) | 5/5 Done (45 deferred_live AC-09) | REQ-07 · live residual |
| [req-08-req9-ops-parity-gateway-naming](req-08-req9-ops-parity-gateway-naming/INDEX.md) | 4/4 Done (P5/P6 · next P7) | REQ-08 / REQ9 |
| [req-09-req13-sense-brief-poster-worker](req-09-req13-sense-brief-poster-worker/INDEX.md) | 5/5 Done (P5/P6/P8 · 49/50 next P7) | REQ-09 / REQ13 Wave 2 |
| [req-10-ai-provider-selection-and-mock-mode](req-10-ai-provider-selection-and-mock-mode/INDEX.md) | 4/5 P8 Done · 55 residual (package INDEX P5 APPLY / story P7) | REQ-10 |
| [req-11-req15-dual-confirm-gateway-submit-spa-handoff](req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md) | 3/3 Done (56–58) · wave exhausted · AC-07 live Partial | REQ-11 · pkg-000061 |
| [req-12-req15-interview-deepseek-openai-providers](req-12-req15-interview-deepseek-openai-providers/INDEX.md) | 3/3 Done (59–61) · AC-04 live Partial | REQ-12 · pkg-000064 |
| [req-13-req15-semantic-state-roles-instruction-assembly](req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md) | 62–64 Done · **65–67 Todo** (ASGI wire / cutover / volume) | REQ-13 · residual G-02 · gap-closure MVP/Track B |
| [req15-tg-channel-interviewer-ux](req15-tg-channel-interviewer-ux/INDEX.md) | 68 Done · 69 P1 scaffold · pkg-000072 | REQ15 TG interviewer UX residual · EPIC-12 · [triage](../../../../docs/analysis/req15-tg-interviewer-ux-gap-triage-2026-11-06.md) |

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
| Done | [STORY-AIBRIDGE-17-spa-https-continuation-e2e](req-03-runtime-remediation/STORY-AIBRIDGE-17-spa-https-continuation-e2e.md) | req-03-runtime-remediation |
| Deferred | [STORY-AIBRIDGE-18-p2-replicas-observability](req-03-runtime-remediation/STORY-AIBRIDGE-18-p2-replicas-observability.md) | req-03-runtime-remediation |
| Implemented | [STORY-AIBRIDGE-19-assembled-instructions-engine-wire](req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md) | req-05-content-phase-a-flat-launch |
| Implemented | [STORY-AIBRIDGE-20-full-instructions-manifest](req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md) | req-05-content-phase-a-flat-launch |
| Implemented | [STORY-AIBRIDGE-21-oas-image-env-docs](req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-21-oas-image-env-docs.md) | req-05-content-phase-a-flat-launch |
| Implemented | [STORY-AIBRIDGE-22-content-phase-a-proof](req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-22-content-phase-a-proof.md) | req-05-content-phase-a-flat-launch |
| Implemented | [STORY-AIBRIDGE-23-qa-auth-ops-boundaries](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md) | qa-inbound-outbound-data-flow |
| Implemented | [STORY-AIBRIDGE-24-qa-json-schema-boundary](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-24-qa-json-schema-boundary.md) | qa-inbound-outbound-data-flow |
| Implemented | [STORY-AIBRIDGE-25-qa-n8n-telegram-mapping](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md) | qa-inbound-outbound-data-flow |
| Implemented | [STORY-AIBRIDGE-26-qa-idempotency-concurrency](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-26-qa-idempotency-concurrency.md) | qa-inbound-outbound-data-flow |
| Implemented | [STORY-AIBRIDGE-27-qa-openai-prompt-behavior](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md) | qa-inbound-outbound-data-flow |
| Implemented | [STORY-AIBRIDGE-28-qa-tool-call-validation](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-28-qa-tool-call-validation.md) | qa-inbound-outbound-data-flow |
| Implemented | [STORY-AIBRIDGE-29-qa-action-token-fsm](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-29-qa-action-token-fsm.md) | qa-inbound-outbound-data-flow |
| Implemented | [STORY-AIBRIDGE-30-qa-gateway-continuation](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-30-qa-gateway-continuation.md) | qa-inbound-outbound-data-flow |
| Implemented | [STORY-AIBRIDGE-31-qa-restart-lifecycle-retention](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md) | qa-inbound-outbound-data-flow |
| Implemented | [STORY-AIBRIDGE-32-qa-privacy-logs-observability](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-32-qa-privacy-logs-observability.md) | qa-inbound-outbound-data-flow |
| Scaffolded | [STORY-AIBRIDGE-33-qa-readiness-configuration](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-33-qa-readiness-configuration.md) | qa-inbound-outbound-data-flow |
| Implemented | [STORY-AIBRIDGE-34-qa-product-journey-scenarios](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-34-qa-product-journey-scenarios.md) | qa-inbound-outbound-data-flow |
| Done | [STORY-AIBRIDGE-35-qa-gates-layers-dod](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-35-qa-gates-layers-dod.md) | qa-inbound-outbound-data-flow |
| Done | [STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md) | qa-inbound-outbound-data-flow |
| Done | [STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md) | qa-inbound-outbound-data-flow |
| Done | [STORY-AIBRIDGE-38-qa-oai-channel-error-outcome](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md) | qa-inbound-outbound-data-flow |
| Done | [STORY-AIBRIDGE-39-qa-char008-send-edit-capture](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md) | qa-inbound-outbound-data-flow |
| Done | [STORY-AIBRIDGE-40-qa-suite-assert-hygiene](qa-inbound-outbound-data-flow/STORY-AIBRIDGE-40-qa-suite-assert-hygiene.md) | qa-inbound-outbound-data-flow |
| Done | [STORY-AIBRIDGE-41-openai-schema-projection](req-07-openai-strict-schema-compat/STORY-AIBRIDGE-41-openai-schema-projection.md) | req-07-openai-strict-schema-compat |
| Done | [STORY-AIBRIDGE-42-canonical-uniqueitems-validation](req-07-openai-strict-schema-compat/STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md) | req-07-openai-strict-schema-compat |
| Done | [STORY-AIBRIDGE-43-validation-context-bind-readyz](req-07-openai-strict-schema-compat/STORY-AIBRIDGE-43-validation-context-bind-readyz.md) | req-07-openai-strict-schema-compat |
| Done | [STORY-AIBRIDGE-44-compat-merge-gate-proof](req-07-openai-strict-schema-compat/STORY-AIBRIDGE-44-compat-merge-gate-proof.md) | req-07-openai-strict-schema-compat |
| Done (deferred_live) | [STORY-AIBRIDGE-45-compat-live-telegram-verify](req-07-openai-strict-schema-compat/STORY-AIBRIDGE-45-compat-live-telegram-verify.md) | req-07-openai-strict-schema-compat |
| P6 Done · pkg-000045 | [STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack](req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md) | req-08-req9-ops-parity-gateway-naming |
| P6 Done · pkg-000046 | [STORY-AIBRIDGE-REQ9-02-health-ready-aliases](req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md) | req-08-req9-ops-parity-gateway-naming |
| P6 Done · pkg-000047 | [STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut](req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md) | req-08-req9-ops-parity-gateway-naming |
| P5 Done · pkg-000048 | [STORY-AIBRIDGE-REQ9-04-local-railway-verify](req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-04-local-railway-verify.md) | req-08-req9-ops-parity-gateway-naming |
| P8 Done · pkg-000049 | [STORY-AIBRIDGE-46-worker-entry-s2s-idempotency](req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md) | req-09-req13-sense-brief-poster-worker |
| P8 Done · pkg-000050 | [STORY-AIBRIDGE-47-sense-brief-prompts-policy](req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-47-sense-brief-prompts-policy.md) | req-09-req13-sense-brief-poster-worker |
| P8 Done · pkg-000051 | [STORY-AIBRIDGE-48-poster-storage-https-url](req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-48-poster-storage-https-url.md) | req-09-req13-sense-brief-poster-worker |
| P5 Done · next P7 · pkg-000052 | [STORY-AIBRIDGE-49-gateway-bind-fail-version](req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-49-gateway-bind-fail-version.md) | req-09-req13-sense-brief-poster-worker |
| P6 Done · next P7 · pkg-000053 | [STORY-AIBRIDGE-50-worker-isolation-harness](req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-50-worker-isolation-harness.md) | req-09-req13-sense-brief-poster-worker |
| P8 Done · pkg-000054 | [STORY-AIBRIDGE-51-provider-ports-env-registry](req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-51-provider-ports-env-registry.md) | req-10-ai-provider-selection-and-mock-mode |
| P8 Done · pkg-000055 | [STORY-AIBRIDGE-52-mock-providers-accept-pipe](req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-52-mock-providers-accept-pipe.md) | req-10-ai-provider-selection-and-mock-mode |
| P8 Done · pkg-000056 | [STORY-AIBRIDGE-53-readyz-allow-mock-refuse](req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md) | req-10-ai-provider-selection-and-mock-mode |
| P8 Done · pkg-000057 | [STORY-AIBRIDGE-54-openai-text-live-port](req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-54-openai-text-live-port.md) | req-10-ai-provider-selection-and-mock-mode |
| P5 APPLY · next P7 · TASKED=0 · pkg-000058 | [STORY-AIBRIDGE-55-provider-docs-verify-matrix](req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-55-provider-docs-verify-matrix.md) | req-10-ai-provider-selection-and-mock-mode |
| Done | [STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify](req-11-req15-dual-confirm-gateway-submit-spa-handoff/STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify.md) | req-11-req15-dual-confirm-gateway-submit-spa-handoff · P8 8a4774e/db5f5ac/22bccc3 |
| Done | [STORY-AIBRIDGE-57-l11-invalidation-seam](req-11-req15-dual-confirm-gateway-submit-spa-handoff/STORY-AIBRIDGE-57-l11-invalidation-seam.md) | req-11-req15-dual-confirm-gateway-submit-spa-handoff · P8 pkg-000060 |
| Done | [STORY-AIBRIDGE-58-stub-live-evidence-gates](req-11-req15-dual-confirm-gateway-submit-spa-handoff/STORY-AIBRIDGE-58-stub-live-evidence-gates.md) | req-11-req15-dual-confirm-gateway-submit-spa-handoff · P8 pkg-000061 · AC-07 live Partial |
| Done | [STORY-AIBRIDGE-59-interview-port-env-fail-closed](req-12-req15-interview-deepseek-openai-providers/STORY-AIBRIDGE-59-interview-port-env-fail-closed.md) | req-12-req15-interview-deepseek-openai-providers · pkg-000062 |
| Done | [STORY-AIBRIDGE-60-openai-deepseek-interview-adapters](req-12-req15-interview-deepseek-openai-providers/STORY-AIBRIDGE-60-openai-deepseek-interview-adapters.md) | req-12-req15-interview-deepseek-openai-providers · pkg-000063 |
| Done | [STORY-AIBRIDGE-61-interview-provider-stub-live-evidence](req-12-req15-interview-deepseek-openai-providers/STORY-AIBRIDGE-61-interview-provider-stub-live-evidence.md) | req-12-req15-interview-deepseek-openai-providers · pkg-000064 · AC-04 live Partial |
| Done | [STORY-AIBRIDGE-62-semantic-state-store-invalidation](req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-62-semantic-state-store-invalidation.md) | req-13 · Product Done |
| Done | [STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures](req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md) | req-13 · Product Done |
| Done | [STORY-AIBRIDGE-64-content-parity-stub-live-evidence](req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-64-content-parity-stub-live-evidence.md) | req-13 · Product Done · AC-05 Partial |
| Done | [STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire](req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md) | req-13 · Product Done · pkg-000068 · G-02 Lifted |
| Done | [STORY-AIBRIDGE-66-roles-schema-channel-cutover](req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-66-roles-schema-channel-cutover.md) | req-13 · Product Done · pkg-000069 · residual 67 |
| Todo | [STORY-AIBRIDGE-67-consume-parity-volume-evidence](req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-67-consume-parity-volume-evidence.md) | req-13 · gap V8 Track B |
| 🟢 Product Done · Code Done · pkg-000071 | [STORY-AIBRIDGE-68-channel-seam-send-actions-always](req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-68-channel-seam-send-actions-always.md) | req15-tg-channel-interviewer-ux |
| 🟡 P1 scaffold · pkg-000072 · next P2 | [STORY-AIBRIDGE-69-session-language-pick-actions](req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-69-session-language-pick-actions.md) | req15-tg-channel-interviewer-ux |

## Build order

**REQ-01 (Done):** `01 → 02 → 03 → 04 → 05 → 06`

**REQ-03:** `09 → 10 → 11 ∥ 12 → 13 → 14 ∥ 15 → 16 → 17` · Deferred `18`

**REQ-05 (Implemented):** `19 ∥ 20 ∥ 21 → 22`

**QA inbound/outbound:** `23…40` · residual Scaffolded **33** on package INDEX

**REQ-07 (Done · AC-09 live residual):** `41 ∥ 42 → 43 → 44 → 45`

**REQ-08 / REQ9 (Done · next P7):** `REQ9-01 ∥ REQ9-02 → REQ9-03 → REQ9-04`

**REQ-09 / REQ13 Wave 2 (Done · 49/50 next P7):** `46 → 47 → 48 → 49 → 50`

**REQ-10 (51–54 P8 Done · 55 residual):** `51 → 52 → 53 → 54 → 55`

**REQ-11 (Done · AC-07 live Partial):** `56 → 57 → 58`

**REQ-12 (Done · AC-04 live Partial):** `59 → 60 → 61`

**REQ-13:** `62 → 63 → 64` Done · residual `65 → 66 → 67`

**REQ15 TG interviewer UX residual:** `68` Done · `69` P1 scaffold (pkg-000072 · next P2) · [`req15-tg-channel-interviewer-ux`](req15-tg-channel-interviewer-ux/INDEX.md) · EPIC-12

Out of this INDEX active set: [REQ-02](../../requirements/REQ-02-DOGE-AI-BRIDGE-POST-PILOT-EVOLUTION.md), [REQ-06](../../requirements/REQ-06-CONTENT-PHASE-B-SCALABLE-PACKAGING.md), ADMIN/*, mockups.
