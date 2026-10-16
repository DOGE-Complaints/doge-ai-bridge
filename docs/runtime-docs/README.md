# doge-ai-bridge — runtime docs

Человекочитаемая документация runtime по **фактическому коду**. Machine contracts — в OpenAPI.

| Doc | Focus |
|-----|--------|
| [01-api.md](./01-api.md) | HTTP routes (channel + worker), auth, envelopes, probes |
| [02-ai-provider-selection.md](./02-ai-provider-selection.md) | Worker provider list + mock-first ops (AC-10-07 / REQ-10) |
| [03-provider-verify-matrix.md](./03-provider-verify-matrix.md) | Verify surfaces → pytest map (STORY-55) |

## Related

- REQ: [REQ-01](../requirements/REQ-01-doge-ai-bridge-runtime.md) · [REQ-09](../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) · [REQ-10](../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md)
- Architecture: [runtime/00-overview.md](../architecture/runtime/00-overview.md) · [01-channel-facade](../architecture/runtime/01-channel-facade.md) · [sense-brief-poster-worker](../architecture/sense-brief-poster-worker/00-overview.md) · [ai-provider-selection](../architecture/ai-provider-selection/00-overview.md)
- Gateway sibling (cite): [REQ-58 backfill](../../../doge-complaints-gateway/docs/requirements/58-req13-existing-issues-sense-brief-backfill-via-regenerate.md)
- OpenAPI channel: [aibridge-channel-v1.openapi.yaml](../openapi/aibridge-channel-v1.openapi.yaml)
- OpenAPI worker: [aibridge-worker-sense-brief-v1.openapi.yaml](../openapi/aibridge-worker-sense-brief-v1.openapi.yaml)
- OpenAPI wire: [story-intake-actions.openapi.yaml](../openapi/story-intake-actions.openapi.yaml)
- Code gap vs REQ-01: [analysis/req-01-runtime-code-gap-2026-09-13.md](../analysis/req-01-runtime-code-gap-2026-09-13.md) (local analysis zone)
- Validator disagreements: [analysis/req-01-gap-validator-disagreements-2026-09-13.md](../analysis/req-01-gap-validator-disagreements-2026-09-13.md)
- Ops n8n: [ops/n8n-channel-workflow/README.md](../ops/n8n-channel-workflow/README.md)
