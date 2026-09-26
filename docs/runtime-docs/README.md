# doge-ai-bridge — runtime docs

Человекочитаемая документация runtime по **фактическому коду**. Machine contracts — в OpenAPI.

| Doc | Focus |
|-----|--------|
| [01-api.md](./01-api.md) | HTTP routes, auth, envelopes, `/healthz` `/readyz` `/metrics` |

## Related

- REQ: [REQ-01](../requirements/REQ-01-doge-ai-bridge-runtime.md)
- Architecture: [runtime/00-overview.md](../architecture/runtime/00-overview.md) · [01-channel-facade](../architecture/runtime/01-channel-facade.md)
- OpenAPI channel: [aibridge-channel-v1.openapi.yaml](../openapi/aibridge-channel-v1.openapi.yaml)
- OpenAPI wire: [story-intake-actions.openapi.yaml](../openapi/story-intake-actions.openapi.yaml)
- Code gap vs REQ-01: [analysis/req-01-runtime-code-gap-2026-09-13.md](../analysis/req-01-runtime-code-gap-2026-09-13.md) (local analysis zone)
- Validator disagreements: [analysis/req-01-gap-validator-disagreements-2026-09-13.md](../analysis/req-01-gap-validator-disagreements-2026-09-13.md)
- Ops n8n: [ops/n8n-channel-workflow/README.md](../ops/n8n-channel-workflow/README.md)
