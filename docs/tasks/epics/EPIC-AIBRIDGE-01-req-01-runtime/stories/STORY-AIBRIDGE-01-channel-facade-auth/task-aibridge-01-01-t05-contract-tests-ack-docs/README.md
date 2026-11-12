# Task: tests — Channel OAS contract tests + ack-order docs

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md`  
**Parent story:** [`STORY-AIBRIDGE-01-channel-facade-auth.md`](../STORY-AIBRIDGE-01-channel-facade-auth.md)

## Purpose

Contract tests request/response vs committed `aibridge-channel-v1.openapi.yaml`; document operator ack order (n8n `answerCallbackQuery` → `/v1/channel/actions` → Send/Edit) without inventing JSON (align ops/arch — do not invent new schemas).

**Out of this task:** full `/metrics` series (story 06); inventing n8n workflow JSON.

## Code Facts (verified exists)

1. Channel OAS SSOT — `doge-ai-bridge/docs/openapi/aibridge-channel-v1.openapi.yaml`.
2. Ack order described — `docs/architecture/runtime/01-channel-facade.md`; OAS description mentions `answerCallbackQuery`.
3. n8n ops (no invented JSON) — `doge-ai-bridge/docs/ops/n8n-channel-workflow/README.md`.

## AC/DoD

- [x] Contract tests: request/response vs committed channel OAS — story AC #4.
- [x] Operator ack order documented (answerCallbackQuery → `/v1/channel/actions` → Send/Edit).
- [x] No invented JSON schemas beyond committed OAS / existing ops docs.
- [x] `Skill declared: python-pro` present.

## Where to change

- Test files under `doge-ai-bridge/` (once pytest scaffolded in t01 wave).
- Ops/docs touch only if ack-order gap vs story Scope #6.

## Verification commands

```bash
# After implement: pytest targeting channel OAS
rg -n 'answerCallbackQuery' doge-ai-bridge/docs/ops doge-ai-bridge/docs/architecture/runtime
```
