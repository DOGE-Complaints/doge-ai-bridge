# Channel HTTP façade (n8n ↔ aibridge)

**Parent REQ:** [REQ-01 §6–§7](../../requirements/REQ-01-doge-ai-bridge-runtime.md)  
**Overview:** [00-overview.md](./00-overview.md)

---

## 1. Role

Expose a **versioned server-to-server API** for n8n. Not a second Story Intake wire contract ([REQ-01 §4](../../requirements/REQ-01-doge-ai-bridge-runtime.md)).

| Endpoint | Purpose |
|----------|---------|
| `POST /v1/channel/turns` | Ordinary Telegram message → interview turn |
| `POST /v1/channel/actions` | Inline callback with opaque `action_token` |
| `GET /healthz` | Liveness |
| `GET /readyz` | Readiness (fail-closed invariants) |
| `GET /metrics` | Prometheus-compatible metrics (private only) |

Committed SSOT (when created): `docs/openapi/aibridge-channel-v1.openapi.yaml` — **named in REQ, not on disk yet**.

---

## 2. Authentication (mode C)

- Every `/v1/channel/*` request: `Authorization: Bearer <token>`.
- Bridge validates against `AIBRIDGE_CHANNEL_BEARER_TOKEN` (+ optional previous during rotation).
- Must differ from `DOGESTONIA_API_BEARER_TOKEN` or readiness fails ([REQ-01 §7, §15](../../requirements/REQ-01-doge-ai-bridge-runtime.md)).
- n8n stores the channel token only in Header Auth credential — **never** the gateway Bearer.
- n8n calls Railway **private** hostname; façade rejects missing Bearer even on private interface.
- Public domain for aibridge is **not** required for pilot.

---

## 3. Trust at the boundary

- Telegram IDs as decimal strings; unknown JSON fields rejected; size-bounded bodies; no CORS.
- Timestamp, node/pack/operation/origin are **server-owned** — not accepted from n8n ([REQ-01 §6 AIB-CH-02](../../requirements/REQ-01-doge-ai-bridge-runtime.md)).
- Duplicate `event_id` returns stored response (no second OpenAI call).
- n8n answers Telegram `answerCallbackQuery`; aibridge does **not** call Telegram.

---

## 4. n8n mapping (no fork)

```text
Telegram Trigger
  → Switch
      message → HTTP POST /v1/channel/turns → Telegram Send (+ actions)
      callback_query → Answer Callback Query → HTTP POST /v1/channel/actions → Send/Edit
```

([REQ-01 §6 AIB-CH-06](../../requirements/REQ-01-doge-ai-bridge-runtime.md))

---

## 5. Wave 1 live proof

Minimum to close infrastructure wave:

1. aibridge deployed with private networking + channel Bearer.
2. `/readyz` ready + smoke (unauthenticated → 401).
3. **Live** n8n HTTP Request to `POST /v1/channel/turns` with Bearer → bounded response.
4. Mode: interview or `AIBRIDGE_DRY_RUN` — **no** gateway `POST /story-drafts`.

Full Telegram → dual-confirm → stash → SPA = wave 2.
