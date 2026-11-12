# AI Bridge · scope dashboard

> **Scope-Id:** mvp  
> **Scope:** MVP  
> **SSOT:** [backlog-stories/INDEX.md](backlog-stories/INDEX.md) · [req-01-runtime](backlog-stories/req-01-runtime/INDEX.md) · [req-03-runtime-remediation](backlog-stories/req-03-runtime-remediation/INDEX.md) · [req-05-content-phase-a-flat-launch](backlog-stories/req-05-content-phase-a-flat-launch/INDEX.md) · [qa-inbound-outbound-data-flow](backlog-stories/qa-inbound-outbound-data-flow/INDEX.md) · [req-07-openai-strict-schema-compat](backlog-stories/req-07-openai-strict-schema-compat/INDEX.md) · [req-08-req9-ops-parity-gateway-naming](backlog-stories/req-08-req9-ops-parity-gateway-naming/INDEX.md) · [req-09-req13-sense-brief-poster-worker](backlog-stories/req-09-req13-sense-brief-poster-worker/INDEX.md) · [req-10-ai-provider-selection-and-mock-mode](backlog-stories/req-10-ai-provider-selection-and-mock-mode/INDEX.md) · [req-11-req15-dual-confirm-gateway-submit-spa-handoff](backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md) · [req-12-req15-interview-deepseek-openai-providers](backlog-stories/req-12-req15-interview-deepseek-openai-providers/INDEX.md) · [req-13-req15-semantic-state-roles-instruction-assembly](backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md) · [REQ-01](../requirements/REQ-01-doge-ai-bridge-runtime.md) · [REQ-03](../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) · [REQ-05](../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) · [REQ-07](../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) · [REQ-08](../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) · [REQ-09](../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) · [REQ-10](../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) · [REQ-11](../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) · [REQ-12](../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) · [REQ-13](../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md)  
> **Architecture:** [runtime/00-overview.md](../architecture/runtime/00-overview.md) · [TECH-ARCH-REQ-07](../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) · [req9-ops-naming](../../../docs/architecture/req9-ops-naming/00-overview.md) · [sense-brief-poster-worker](../architecture/sense-brief-poster-worker/00-overview.md) · [ai-provider-selection](../architecture/ai-provider-selection/00-overview.md) · [req15-dual-confirm-handoff](../architecture/req15-dual-confirm-handoff/00-overview.md) · [req15-interview-providers](../architecture/req15-interview-providers/00-overview.md) · [req15-semantic-state-roles](../architecture/req15-semantic-state-roles/00-overview.md)  
> **Updated:** 2026-11-02T08:32:08Z  
> **Last change:** REQ-13 backlog STORY-62…64 Todo · recount req-12 59–61 Done · §Now → REQ-13 · AC-05 Partial lock (Q1).

## Summary

| Metric | Value |
|--------|-------|
| Backlog packages | 11 |
| Active work items | 65 |
| Done / Implemented | 60 |
| Scaffolded | 1 (AIBRIDGE-33 on package INDEX) |
| Todo | 3 (AIBRIDGE-62…64) |
| Residual mid-pipeline (not Todo) | 1 (AIBRIDGE-55 — package INDEX P5 APPLY / story P7) |
| Deferred | 1 (AIBRIDGE-18) |
| Superseded (excl.) | 2 (07/08) |
| **Overall progress (active)** | **92%** `███████████░` |

*Active = Done+Implemented+Scaffolded+Todo + mid-pipeline 55. Deferred 18 and Superseded 07/08 вне %.*  
*Done bucket = 60 (prior 57 + req-12 STORY-59…61 P8); open for % = Scaffolded 1 + Todo 3 + residual 55 = 5; 60/65 → filled = round(12×60/65)=11.*  
*REQ-07 story 45 counted Done with deferred_live AC-09 residual.*  
*REQ-11 AC-07 / REQ-12 AC-04 live Explicit Partial do not remove stories from Done (gate/docs scope).*

## By package

| Package | Stories | Done/Impl | Scaffolded | Todo | Deferred | Progress |
|---------|---------|-----------|------------|------|----------|----------|
| [req-01-runtime](backlog-stories/req-01-runtime/INDEX.md) | 6 core (+2 Superseded) | 6 | 0 | 0 | 0 | **100%** core |
| [req-03-runtime-remediation](backlog-stories/req-03-runtime-remediation/INDEX.md) | 10 | 9 | 0 | 0 | 1 | **100%** of active (9/9) |
| [req-05-content-phase-a-flat-launch](backlog-stories/req-05-content-phase-a-flat-launch/INDEX.md) | 4 | 4 | 0 | 0 | 0 | **100%** |
| [qa-inbound-outbound-data-flow](backlog-stories/qa-inbound-outbound-data-flow/INDEX.md) | 18 | 17 | 1 | 0 | 0 | **94%** `███████████░` |
| [req-07-openai-strict-schema-compat](backlog-stories/req-07-openai-strict-schema-compat/INDEX.md) | 5 | 5 | 0 | 0 | 0 | **100%** (AC-09 live residual) |
| [req-08-req9-ops-parity-gateway-naming](backlog-stories/req-08-req9-ops-parity-gateway-naming/INDEX.md) | 4 | 4 | 0 | 0 | 0 | **100%** (next P7) |
| [req-09-req13-sense-brief-poster-worker](backlog-stories/req-09-req13-sense-brief-poster-worker/INDEX.md) | 5 | 5 | 0 | 0 | 0 | **100%** (49/50 next P7) |
| [req-10-ai-provider-selection-and-mock-mode](backlog-stories/req-10-ai-provider-selection-and-mock-mode/INDEX.md) | 5 | 4 | 0 | 0 | 0 | **80%** `██████████░░` (55 residual) |
| [req-11-req15-dual-confirm-gateway-submit-spa-handoff](backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md) | 3 | 3 | 0 | 0 | 0 | **100%** (AC-07 live Partial) |
| [req-12-req15-interview-deepseek-openai-providers](backlog-stories/req-12-req15-interview-deepseek-openai-providers/INDEX.md) | 3 | 3 | 0 | 0 | 0 | **100%** (AC-04 live Partial) |
| [req-13-req15-semantic-state-roles-instruction-assembly](backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md) | 3 | 0 | 0 | 3 | 0 | **0%** `░░░░░░░░░░░░` |

## Remaining

| Pri | Story | Package | Status | Essence |
|-----|-------|---------|--------|---------|
| 1 | [AIBRIDGE-62](backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-62-semantic-state-store-invalidation.md) | req-13… | Todo | Semantic store + L13-3 invalidation |
| 2 | [AIBRIDGE-63](backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md) | req-13… | Todo | Roles + coordinator + fixture assembly |
| 3 | [AIBRIDGE-64](backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-64-content-parity-stub-live-evidence.md) | req-13… | Todo | Volume/parity gates · AC-05 Partial OK |
| 4 | [AIBRIDGE-55](backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-55-provider-docs-verify-matrix.md) | req-10… | Residual | Docs/verify matrix |
| 5 | [AIBRIDGE-49](backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-49-gateway-bind-fail-version.md) | req-09… | P5 Done · next P7 | Bind residual P7 |
| 6 | [AIBRIDGE-50](backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-50-worker-isolation-harness.md) | req-09… | P6 Done · next P7 | Harness residual P7 |
| 7 | [AIBRIDGE-45](backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-45-compat-live-telegram-verify.md) | req-07… | Done deferred_live | AC-09 live Telegram BLOCKED |
| 8 | [AIBRIDGE-33](backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-33-qa-readiness-configuration.md) | qa-… | Scaffolded | QA readiness INDEX residual |

## §Wave-2 residents gate

| Gate | Status | Pointer |
|------|--------|---------|
| R3-P1-08 SPA HTTPS continuation | **BLOCKED** — spa evidence missing | [checklist](../ops/r3-p1-08-spa-https-continuation-gate.md) · [BLOCKED](../ops/spa-https-continuation-evidence-BLOCKED-20260913.md) |

**Rule:** treat **wave-2 / real residents** as **blocked** until spa evidence is linked (do not invent spa PASS).

## §Deferred

| Story | Notes |
|-------|--------|
| [AIBRIDGE-18](backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-18-p2-replicas-observability.md) | P2 replicas/observability — after first node |

## Requirements (intake)

| REQ | Title | Status | Notes |
|-----|-------|--------|-------|
| [REQ-13](../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) | REQ15 semantic state / roles / C | **Draft · §Now · STORY-62…64 Todo** | Arch Present · fixture isolation · AC-05 Partial |
| [REQ-12](../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) | REQ15 interview DeepSeek \| OpenAI | **Draft · 59–61 P8 Done** | AC-04 live Partial |
| [REQ-11](../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) | REQ15 dual confirm / stash / SPA | **EPIC-09 · 56–58 P8 Done** | AC-07 live Partial · wave exhausted |
| [REQ-10](../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) | AI provider selection + mock mode | Draft · 51…54 P8 · 55 residual | Tech-arch Present |
| [REQ-09](../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) | REQ13 — sense brief + civic poster worker | Draft · 46…50 Done | 49/50 next P7 |
| [REQ-08](../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) | REQ9 ops parity + gateway naming | Stories Done | REQ9-01…04 · next P7 |

## §Now

1. **REQ-13:** `62 → 63 → 64` ([package INDEX](backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md)).  
2. Residual: REQ-10 **55**; REQ-09 **49/50** next P7; REQ-07 **AC-09** live; spa HTTPS wave-2 BLOCKED.  
3. Parallel peer: GPT UI **REQ-48** (blocks live AC-05 Pass only). Optional: QA **33**; Deferred **18**.

## Done (recent)

- REQ-13 backlog materialized · STORY-AIBRIDGE-62…64 · 2026-11-02T08:32:08Z · Q1 AC-05 Partial  
- Dashboard recount: req-12 59–61 Done (was stale Todo) · §Now → REQ-13  
- REQ-13 tech-arch Present · `req15-semantic-state-roles/`  
- REQ-12 STORY-59…61 P8 Done · AC-04 live Partial  
- REQ-11 package wave exhausted · AC-07 live Partial  
- REQ-10 / REQ-09 / REQ-08 / REQ-07 as prior
