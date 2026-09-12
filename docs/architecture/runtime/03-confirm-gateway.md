# Dual-confirm, validation & gateway

**Parent REQ:** [REQ-01 §10–§16](../../requirements/REQ-01-doge-ai-bridge-runtime.md)  
**Overview:** [00-overview.md](./00-overview.md)

---

## 1. Dual-confirm

| Decision | Meaning |
|----------|---------|
| Interpretation confirm | “You understood my draft” — **never** authorizes gateway HTTPS |
| Send confirm | “Send to DOGEstonia” — only path that may call gateway |

n8n HITL approve/decline is **not** a substitute for this policy ([REQ-01 §13](../../requirements/REQ-01-doge-ai-bridge-runtime.md); interview context).

Canonical FSM states: `interviewing` → `awaiting_interpretation_confirm` → `interpretation_confirmed` → `awaiting_send_confirm` → `executing` → `stashed` (plus `cancelled` / `unknown_outcome` / `failed`).

---

## 2. Action tokens

- Opaque tokens; ≤64 UTF-8 bytes for Telegram `callback_data`.
- Store **hash** only; raw token returned once to n8n.
- Bind: action, deployment, session, user/chat, operation, revision/hash, expiry, state.
- Edit invalidates old revision tokens; Cancel cancels pending; replay must not re-hit gateway.

Pilot TTL: **15 minutes** (`AIBRIDGE_ACTION_TOKEN_TTL_SECONDS`).

---

## 3. Tool intent vs permission

A model `function_call` is a **frozen intent** after validation — not permission to execute.  
Gateway runs only after Send token consume in the same transaction ([REQ-01 §10 AIB-RSP-03](../../requirements/REQ-01-doge-ai-bridge-runtime.md)).

Three gates: strict tool args → pack payload → wire body ([REQ-01 §12](../../requirements/REQ-01-doge-ai-bridge-runtime.md)).

---

## 4. Gateway

- Exact configured HTTPS origin; TLS verify; no redirects; fixed `POST /story-drafts`.
- Bearer only inside `GatewayExecutor` from `DOGESTONIA_API_BEARER_TOKEN`.
- Success only on verified 201 + `draft_id` + `trace_id`.
- Ambiguous delivery → `unknown_outcome`; **no** automatic retry ([REQ-01 §15 AIB-HTTP-05](../../requirements/REQ-01-doge-ai-bridge-runtime.md)).
- Local best-effort at-most-once; do not claim strict distributed ≤1 without gateway idempotency.

---

## 5. Wave 1 vs wave 2

| Wave | Gateway |
|------|---------|
| 1 | `AIBRIDGE_DRY_RUN` and/or interview-only live turns — **no** real stash |
| 2 | Full Send → stash → `continuation_url` |

Continuation URL only with `outcome=stashed`; copy must not claim Story published ([REQ-01 §16](../../requirements/REQ-01-doge-ai-bridge-runtime.md)).
