# Operator pilot README — stubs (REQ-01 deliverables / story 06)

**Service:** `doge-ai-bridge`  
**Do not** paste secrets here — use Railway / local `.env` (gitignored).

## Private networking

- Expose channel façade (`/v1/channel/*`) only on the private network path used by n8n.
- `/metrics` is **private-only** for pilot scrape (no channel Bearer; do not publish publicly).
- `/healthz` / `/readyz` for platform health checks.

See [04-ops-security.md](../architecture/runtime/04-ops-security.md) §1 / §3.

## n8n mapping

- Import / smoke contract: [n8n-channel-workflow/README.md](./n8n-channel-workflow/README.md)
- Channel Bearer Auth only in n8n → aibridge (never gateway Bearer / OpenAI key in n8n).
- `answerCallbackQuery` immediately; then `/v1/channel/actions`.

## Rotation

- Channel Bearer rotation: [channel-bearer-rotation.md](../runbooks/channel-bearer-rotation.md)

## Privacy & unknown outcome

- [privacy-pilot.md](../runbooks/privacy-pilot.md)
- [unknown-outcome-reconciliation.md](../runbooks/unknown-outcome-reconciliation.md)

## Wave-1 gate

Executable checklist: [wave1-gate-checklist.md](./wave1-gate-checklist.md)
