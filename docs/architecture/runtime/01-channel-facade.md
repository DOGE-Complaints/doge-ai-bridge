# Channel HTTP façade (n8n ↔ aibridge)

**Parent REQ:** [REQ-01 §6–§7](../../requirements/REQ-01-doge-ai-bridge-runtime.md)  
**Contract SSOT:** [docs/openapi/aibridge-channel-v1.openapi.yaml](../../openapi/aibridge-channel-v1.openapi.yaml)  
**Overview:** [00-overview.md](./00-overview.md)  
**n8n ops template:** [docs/ops/n8n-channel-workflow/README.md](../../ops/n8n-channel-workflow/README.md)

---

## 1. Role

Versioned **server-to-server** API for n8n. Not Story Intake wire ([story-intake-actions.openapi.yaml](../../openapi/story-intake-actions.openapi.yaml)).

| Endpoint | Purpose |
|----------|---------|
| `POST /v1/channel/turns` | Ordinary Telegram message → interview turn |
| `POST /v1/channel/actions` | Inline callback with opaque `action_token` |
| `GET /healthz` / `GET /readyz` | Liveness / readiness |
| `GET /metrics` | Prometheus-compatible (private only) |

Runtime must contract-test live ASGI schemas against the committed channel OpenAPI (not against gateway wire OAS).

---

## 2. Authentication (mode C)

- Every `/v1/channel/*` request: `Authorization: Bearer <token>`.
- Validate `AIBRIDGE_CHANNEL_BEARER_TOKEN` (+ optional previous during rotation).
- Must differ from `DOGESTONIA_API_BEARER_TOKEN` or readiness fails.
- n8n: Header Auth credential only — **never** gateway Bearer or OpenAI key.
- Private Railway hostname; reject missing Bearer even on private interface.

---

## 3. Callback acknowledgement (pilot contract)

**Problem solved:** façade latency must not delay Telegram’s UX ack.

Required n8n order:

1. On `callback_query`: immediately `answerCallbackQuery` with **neutral local text or empty**.
2. Then `POST /v1/channel/actions` with opaque `action_token` + principal.
3. Then `Send Message` / `Edit Message` from aibridge `reply_text` / `actions`.

- **Do not** use aibridge fields for the *primary* Telegram acknowledgement.
- `callback_ack_text` is **removed** from channel v1 success envelope (not in OpenAPI).
- n8n must **not** make security decisions before aibridge responds; only aibridge decides action outcome.

---

## 4. Trust at the boundary

- Telegram IDs as decimal strings; unknown fields rejected; size-bounded bodies; no CORS.
- Timestamp, node/pack/operation/origin are **server-owned**.
- Duplicate `event_id` returns stored response (no second OpenAI call).
- aibridge does **not** call Telegram Bot API.

---

## 5. n8n mapping (no fork)

```text
Telegram Trigger
  → Switch
      message
        → HTTP POST /v1/channel/turns
        → Telegram Send Message (+ inline actions from response.actions)
      callback_query
        → Telegram Answer Callback Query (neutral/empty, immediate)
        → HTTP POST /v1/channel/actions
        → Telegram Send/Edit Message (+ replacement actions)
```

Import the versioned template from [n8n-channel-workflow](../../ops/n8n-channel-workflow/README.md); per node change only Bot credential, private aibridge URL/channel credential, optional labels.

---

## 6. Contract version compatibility

- Additive optional response fields: backward compatible within `/v1`.
- Breaking changes: new major path prefix (e.g. `/v2`), not silent `/v1` mutation.
- n8n workflow artifact records compatible `aibridge-channel-v1` version; smoke must fail closed on mismatch.

---

## 7. Wave 1 live proof

1. Private networking + channel Bearer configured.  
2. `/readyz` + unauthenticated → 401.  
3. Live n8n → `POST /v1/channel/turns` → bounded response.  
4. Interview or `AIBRIDGE_DRY_RUN` — **no** `POST /story-drafts`.
