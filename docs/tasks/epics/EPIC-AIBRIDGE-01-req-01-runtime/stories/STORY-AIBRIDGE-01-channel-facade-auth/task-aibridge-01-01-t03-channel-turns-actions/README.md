# Task: implement — Channel turns/actions + validation envelope

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md`  
**Parent story:** [`STORY-AIBRIDGE-01-channel-facade-auth.md`](../STORY-AIBRIDGE-01-channel-facade-auth.md)

## Purpose

`POST /v1/channel/turns` and `POST /v1/channel/actions` per channel OpenAPI; Telegram IDs as decimal strings; reject unknown fields; size bounds; **no CORS**; response envelope fields per OAS (**no** `callback_ack_text`). Accept `action_token` **shape** only — dual-confirm FSM = story 04 (out of scope).

**Out of this task:** event store/dedupe (t04); OpenAPI contract-test harness (t05).

## Code Facts (verified exists)

1. Paths `/v1/channel/turns`, `/v1/channel/actions`; omits `callback_ack_text` — `doge-ai-bridge/docs/openapi/aibridge-channel-v1.openapi.yaml`.
2. Façade protocol — REQ-01 §6; `docs/architecture/runtime/01-channel-facade.md`.
3. Do not mix with Story Intake wire OAS — `00-overview.md` §2; wire = `story-intake-actions.openapi.yaml` (story 05).
4. Handler module path: **Unknown** until t01 scaffold.

## AC/DoD

- [x] Valid Bearer + turn request → 200 envelope fields per channel OAS (no `callback_ack_text`) — story AC #2.
- [x] Telegram IDs as decimal strings; unknown fields rejected; size bounds enforced; no CORS.
- [x] `action_token` accepted as opaque shape only (no dual-confirm FSM).
- [x] `Skill declared: python-pro` present.

## Where to change

- Route handlers + request validation models on ASGI app.
- Wire Bearer from t02.

## Verification commands

```bash
# After implement: ASGI client tests turns/actions happy + validation
rg -n 'callback_ack_text' doge-ai-bridge  # must not appear in product responses
```
