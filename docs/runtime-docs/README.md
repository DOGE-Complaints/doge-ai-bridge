# doge-ai-bridge — runtime docs

Человекочитаемая документация runtime по **фактическому коду**. Machine contracts — в OpenAPI.

| Doc | Focus |
|-----|--------|
| [01-api.md](./01-api.md) | HTTP routes (channel + worker), auth, envelopes, probes |
| [02-ai-provider-selection.md](./02-ai-provider-selection.md) | Worker provider list + mock-first ops (AC-10-07 / REQ-10) |
| [03-provider-verify-matrix.md](./03-provider-verify-matrix.md) | Verify surfaces → pytest map (STORY-55) |
| [04-confirm-gateway-keep-pipe.md](./04-confirm-gateway-keep-pipe.md) | Dual-confirm + stash + SPA Keep pipe (STORY-56 / REQ-11) |
| [05-l11-invalidation-seam.md](./05-l11-invalidation-seam.md) | L11-1 invalidate_send_permission seam · AC-02 Partial vs Done (STORY-57) |
| [06-ac07-stub-live-evidence-gates.md](./06-ac07-stub-live-evidence-gates.md) | AC-07 stub matrix + live Explicit Partial (STORY-58) · no invent live SUCCESS |
| [07-interview-provider-port-env.md](./07-interview-provider-port-env.md) | Interview port + env fail-closed (STORY-59 / REQ-12) · D4 wire |
| [08-ac04-interview-stub-live-evidence-gates.md](./08-ac04-interview-stub-live-evidence-gates.md) | AC-04 stub matrix + live Explicit Partial (STORY-61) · no invent live SUCCESS |
| [09-semantic-state-store-invalidation.md](./09-semantic-state-store-invalidation.md) | Semantic store ≠ History · L13-3 Target A + Transition C (STORY-62 / REQ-13) |
| [10-roles-coordinator-assembly.md](./10-roles-coordinator-assembly.md) | Five roles + policy + assembly fixtures · L13-1 / AC-07 (STORY-63 / REQ-13) |
| [11-content-volume-parity-stub-live-evidence.md](./11-content-volume-parity-stub-live-evidence.md) | Volume path · AC-06 fail-closed · AC-05 Explicit Partial · stub matrix 62/63 (STORY-64) |
| [12-asgi-channel-semantic-roles-wire.md](./12-asgi-channel-semantic-roles-wire.md) | Channel turns bind SemanticStateService + select/assemble · G-02 Lifted (STORY-65) |

## Related

- REQ: [REQ-01](../requirements/REQ-01-doge-ai-bridge-runtime.md) · [REQ-09](../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) · [REQ-10](../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) · [REQ-11](../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) · [REQ-12](../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) · [REQ-13](../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md)
- Architecture: [runtime/00-overview.md](../architecture/runtime/00-overview.md) · [01-channel-facade](../architecture/runtime/01-channel-facade.md) · [sense-brief-poster-worker](../architecture/sense-brief-poster-worker/00-overview.md) · [ai-provider-selection](../architecture/ai-provider-selection/00-overview.md) · [req15-dual-confirm-handoff](../architecture/req15-dual-confirm-handoff/00-overview.md) · [req15-interview-providers](../architecture/req15-interview-providers/00-overview.md)
- Gateway sibling (cite): [REQ-58 backfill](../../../doge-complaints-gateway/docs/requirements/58-req13-existing-issues-sense-brief-backfill-via-regenerate.md)
- OpenAPI channel: [aibridge-channel-v1.openapi.yaml](../openapi/aibridge-channel-v1.openapi.yaml)
- OpenAPI worker: [aibridge-worker-sense-brief-v1.openapi.yaml](../openapi/aibridge-worker-sense-brief-v1.openapi.yaml)
- OpenAPI wire: [story-intake-actions.openapi.yaml](../openapi/story-intake-actions.openapi.yaml)
- Code gap vs REQ-01: [analysis/req-01-runtime-code-gap-2026-09-13.md](../analysis/req-01-runtime-code-gap-2026-09-13.md) (local analysis zone)
- Validator disagreements: [analysis/req-01-gap-validator-disagreements-2026-09-13.md](../analysis/req-01-gap-validator-disagreements-2026-09-13.md)
- Ops n8n: [ops/n8n-channel-workflow/README.md](../ops/n8n-channel-workflow/README.md)
