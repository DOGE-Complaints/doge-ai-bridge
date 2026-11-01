# doge-ai-bridge — requirements

**Проект:** [`doge-ai-bridge`](https://github.com/DOGE-Complaints/doge-ai-bridge) · builder_project: `aibridge`  
**Protocol parent (GPT UI):** [REQ-47](../../../GPT%20UI/docs/requirements/REQ-47-responses-api-https-bearer-bridge.md)

| № | Файл |
|---|------|
| 01 | [REQ-01-doge-ai-bridge-runtime.md](./REQ-01-doge-ai-bridge-runtime.md) — Responses → Story Intake runtime (v0.4.1) |
| 02 | [REQ-02-DOGE-AI-BRIDGE-POST-PILOT-EVOLUTION.md](./REQ-02-DOGE-AI-BRIDGE-POST-PILOT-EVOLUTION.md) — post-pilot backlog |
| 03 | [REQ-03-RUNTIME-REMEDIATION-AGREED.md](./REQ-03-RUNTIME-REMEDIATION-AGREED.md) — согласованные доработки (v0.2.2 · **Ready for implementation**) |
| 04 | [REQ-04-RUNTIME-SAFETY-AND-CONFIRMATION-HARDENING.md](./REQ-04-RUNTIME-SAFETY-AND-CONFIRMATION-HARDENING.md) — readiness / Send / interpretation hardening (Draft) |
| 05 | [REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md](./REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) — content Phase A full flat dump (v0.2.0 · **Ready for implementation**) |
| 06 | [REQ-06-CONTENT-PHASE-B-SCALABLE-PACKAGING.md](./REQ-06-CONTENT-PHASE-B-SCALABLE-PACKAGING.md) — content Phase B scalable packaging (v0.1.1 · Draft after REQ-05) |
| 07 | [REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md](./REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) — OpenAI strict-schema compat projection |
| 08 | [REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md](./REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) — REQ9 ops parity + gateway naming hard cut (**Draft — awaiting PA.2**) |
| 09 | [REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md](./REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) — REQ13 sense brief + civic poster worker · siblings gateway `57`, spa `23` |
| 10 | [REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md](./REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) — AI provider selection + mock mode (**Draft · locks 2026-10-16**) · worker-only; text+image ports; OpenAI text live / image mock; sibling gateway `58` |
| 11 | [REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md](./REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) — REQ15 dual confirm / gateway stash / SPA (**Draft · T1 · tech-arch · backlog 56…58 Todo** → [`../architecture/req15-dual-confirm-handoff/00-overview.md`](../architecture/req15-dual-confirm-handoff/00-overview.md) · [`../tasks/backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md`](../tasks/backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md)) |
| 12 | [REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md](./REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) — REQ15 interview DeepSeek \| OpenAI (**Draft · T1 Present · target tech-arch Present** → [`../architecture/req15-interview-providers/00-overview.md`](../architecture/req15-interview-providers/00-overview.md)) |
| 13 | [REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md](./REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) — REQ15 semantic state / roles / hybrid C (**Draft · T1 Present · ready for Architect Studio**; ≠ product REQ13 sense-brief) |

**Parent product (REQ15):** [REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md](../../../docs/requirements%20backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md)  
**REQ15 T1:** [req15-t1-keep-adapt-replace-2026-11-01.md](../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md)  
**REQ15 aibridge wave readiness:** [req15-aibridge-wave-readiness-2026-11-01.md](../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md) — Architect Studio order **11 → 12 → 13**; stories only after each arch

**Architecture:** [runtime/00-overview.md](../architecture/runtime/00-overview.md) · [sense-brief-poster-worker](../architecture/sense-brief-poster-worker/00-overview.md) · [ai-provider-selection](../architecture/ai-provider-selection/00-overview.md) · platform [req9-ops-naming](../../../docs/architecture/req9-ops-naming/00-overview.md)  
**Runtime API (code):** [runtime-docs/01-api.md](../runtime-docs/01-api.md)  
**OpenAPI:** [channel v1](../openapi/aibridge-channel-v1.openapi.yaml) · [Story Intake wire](../openapi/story-intake-actions.openapi.yaml)  
**Tech-arch interview:** [zeya888.req-tech-arch-interview-REQ-01-doge-ai-bridge-runtime-2026-09-12.md](../analysis/zeya888.req-tech-arch-interview-REQ-01-doge-ai-bridge-runtime-2026-09-12.md)  
**Pilot recommendations:** [ARCH-RECOMMENDATIONS-REQ-01-PILOT-AND-NODE-SCALING.md](../analysis/ARCH-RECOMMENDATIONS-REQ-01-PILOT-AND-NODE-SCALING.md)  
**Code gap vs REQ-01:** [req-01-runtime-code-gap-2026-09-13.md](../analysis/req-01-runtime-code-gap-2026-09-13.md) (analysis zone)  
**Module-1 → aibridge content options:** [module1-instructions-custom-gpt-to-aibridge-organization-2026-09-16.md](../analysis/module1-instructions-custom-gpt-to-aibridge-organization-2026-09-16.md)

**Версия index:** 2026-11-01 (+ REQ-11/12/13 renumber for exec order 11→12→13 · T1 · wave readiness).
