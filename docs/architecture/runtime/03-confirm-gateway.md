# Dual-confirm, validation & gateway

**Parent REQ:** [REQ-01 §10–§16](../../requirements/REQ-01-doge-ai-bridge-runtime.md)  
**Overview:** [00-overview.md](./00-overview.md)  
**Reconciliation:** [unknown-outcome-reconciliation.md](../../runbooks/unknown-outcome-reconciliation.md)

---

## 1. Dual-confirm

| Decision | Meaning |
|----------|---------|
| Interpretation confirm | “You understood my draft” — **never** authorizes gateway HTTPS |
| Send confirm | “Send to DOGEstonia” — only path that may call gateway |

n8n HITL approve/decline is **not** a substitute. Immediate Telegram `answerCallbackQuery` is UX-only ([01-channel-facade.md](./01-channel-facade.md)).

Canonical FSM: `interviewing` → `awaiting_interpretation_confirm` → `interpretation_confirmed` → `awaiting_send_confirm` → `executing` → `stashed` (plus `cancelled` / `unknown_outcome` / `failed`).

---

## 2. Action tokens

- Opaque; ≤64 UTF-8 bytes for Telegram `callback_data`.
- Store hash only; raw token once to n8n.
- Bind action, deployment, session, user/chat, operation, revision/hash, expiry, state.
- Edit invalidates old revision; Cancel cancels; replay must not re-hit gateway.
- Pilot TTL: **15 minutes**.

---

## 3. Tool intent vs permission

A model `function_call` is a **frozen intent** after validation — not permission to execute.  
Gateway runs only after Send token consume in the same transaction.

Three gates: strict tool args → pack payload → wire body (wire SSOT = [story-intake-actions.openapi.yaml](../../openapi/story-intake-actions.openapi.yaml)).

---

## 4. Pre-send safe failure (LLM budget / timeout)

When budget, timeout, cancel, or rate-limit stops a turn **before** authorized Send:

- Fail **bounded** (no infinite retry).
- Resident-safe message.
- Preserve last **confirmed** session state (do not silently advance).
- **No** gateway side effect.
- Emit redacted metric with stop reason ([04-ops-security.md](./04-ops-security.md)).

History summarization (if ever enabled) is a separate verified transform; it must **not** alter frozen draft, confirmation state, or pinned content version. **Pilot default: out of scope.**

---

## 5. Gateway

- Exact configured HTTPS origin; TLS verify; no redirects; fixed `POST /story-drafts`.
- Bearer only in `GatewayExecutor` from `DOGESTONIA_API_BEARER_TOKEN`.
- Success only on verified 201 + `draft_id` + `trace_id`.
- Ambiguous delivery → `unknown_outcome`; **no** automatic retry for that revision.
- Local best-effort at-most-once; do not claim strict distributed ≤1 without gateway idempotency.

### `unknown_outcome` state rules

- Terminal for automatic Send of the **same** revision.
- UI must not offer blind “Send again” for that revision.
- Operator follows [unknown-outcome-reconciliation.md](../../runbooks/unknown-outcome-reconciliation.md).
- Manual close must **not** invent `stashed` without evidence.

---

## 6. Wave 1 vs wave 2

| Wave | Gateway |
|------|---------|
| 1 | Dry-run / interview-only live turns — **no** real stash |
| 2 | Full Send → stash → `continuation_url` (HTTPS SPA reachable from Telegram mobile) |

Continuation URL only with `outcome=stashed`; copy must not claim Story published.
