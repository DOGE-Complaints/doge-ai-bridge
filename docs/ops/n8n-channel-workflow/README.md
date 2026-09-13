# n8n channel workflow — ops artifact

**Purpose:** Versioned, reproducible Telegram↔aibridge wiring **without** embedding business logic in n8n or secrets in Git.  
**Related:** [aibridge-channel-v1.openapi.yaml](../../openapi/aibridge-channel-v1.openapi.yaml) · [01-channel-facade.md](../../architecture/runtime/01-channel-facade.md) · [REQ-01 §6](../../requirements/REQ-01-doge-ai-bridge-runtime.md) · [REQ-03 §6.1 R3-P1-09 checklist](./r3-p1-09-live-gate-checklist.md)  
**As-of:** 2026-09-13

This directory holds the **ops contract** for the workflow. A full exported workflow JSON (without credentials) is added when an operator exports a verified workflow — **do not** invent a fake JSON body here.

**Live §6.1 gate checklist (STORY-AIBRIDGE-15):** [r3-p1-09-live-gate-checklist.md](./r3-p1-09-live-gate-checklist.md)  
**Live evidence status:** [live-evidence-BLOCKED-20260913.md](./live-evidence-BLOCKED-20260913.md)

---

## 1. What each node deploy imports

| Item | Rule |
|------|------|
| Workflow JSON | Export from verified n8n; **strip credentials**; no Telegram token, channel Bearer, gateway Bearer, OpenAI key |
| Compatible channel API | Pin `aibridge-channel-v1` `info.version` (currently `1.0.0`) |
| Field mapping | Telegram update → façade request (see below) |
| Action mapping | `response.actions[]` → inline keyboard; `callback_data` = `token` only (≤64 bytes) |
| n8n version | Record version used for verification |
| Smoke checklist | Same as wave-1 façade proof |

Per new node: import **same** template; change only Bot credential, private aibridge URL + channel Header Auth, optional display labels.

---

## 2. Required behavior (no-fork)

### Operator ack order (mandatory)

On every Telegram `callback_query`, n8n **must**:

1. Immediately call Telegram `answerCallbackQuery` with **neutral local text or empty** (primary UX ack — do **not** wait for aibridge).
2. Then `POST /v1/channel/actions` with opaque `action_token` + principal (channel Bearer).
3. Then `Send Message` / `Edit Message` using aibridge `reply_text` / `actions`.

`callback_ack_text` is **not** in channel v1 OAS — do not invent it. See [01-channel-facade.md §3](../../architecture/runtime/01-channel-facade.md).

```text
Telegram Trigger
  → Switch
      message → HTTP POST /v1/channel/turns → Send Message (+ actions)
      callback_query
        → Answer Callback Query (neutral/empty, immediate)
        → HTTP POST /v1/channel/actions
        → Send/Edit Message
```

Hard rules:

- Never call gateway `/story-drafts` from n8n.
- Never put gateway URL or gateway Bearer in the workflow.
- Security decisions only after aibridge response.

---

## 3. Mapping cheat-sheet

### turns request

| Façade field | Telegram source |
|--------------|-----------------|
| `channel` | constant `telegram` |
| `event_id` | **update id** as decimal string — `String(update.update_id)` |
| `principal.user_id` | from.id (decimal string) |
| `principal.chat_id` | chat.id (decimal string) |
| `message.message_id` | message.message_id |
| `message.text` | message.text |
| `message.language_code` | optional from language_code |

### actions request

| Façade field | Telegram source |
|--------------|-----------------|
| `event_id` | **same** update id as the enclosing Telegram update (not a new UUID; not `callback_query.id`) |
| `callback_query_id` | callback_query.id |
| `principal.*` | from / message.chat |
| `action_token` | callback_query.data (opaque) |

### `event_id` retry invariance (REQ-03 §6.1)

n8n **MUST NOT** mint a new `event_id` when an HTTP Request node retries the same Telegram update. Reuse `String(update.update_id)` so aibridge dedupe returns the stored envelope instead of re-running the interview.

### response → Telegram

| Façade field | Use |
|--------------|-----|
| `reply_text` | message body |
| `actions[].label` / `.token` / `.style` | inline buttons; data = token only |
| `outcome` / `draft_id` / `continuation_url` | only if `outcome=stashed`; resident-safe copy |

---

## 4. Credentials (names only)

| Credential | Holds |
|------------|--------|
| Telegram Bot | Bot token |
| aibridge Channel Header Auth | `AIBRIDGE_CHANNEL_BEARER_TOKEN` value |

Not stored in Git. Not interchangeable with gateway Bearer.

---

## 5. Smoke checklist (after import)

- [ ] Workflow active; correct Bot  
- [ ] Private aibridge URL + channel Bearer  
- [ ] Message → `/turns` returns 200 envelope  
- [ ] Callback → immediate answerCallbackQuery → `/actions`  
- [ ] Unauthenticated call to aibridge still 401  
- [ ] No node points at `/story-drafts`  

---

## 6. Artifact layout (when exported)

```text
docs/ops/n8n-channel-workflow/
  README.md                          # this file
  CHANGELOG.md                       # optional
  exports/
    aibridge-telegram-channel-v1.json  # credential-stripped export (add when ready)
  META.yaml                          # optional: n8n_version, channel_openapi_version, verified_at
```

Compatibility smoke/E2E should fail if workflow expects fields removed from channel OpenAPI (e.g. historical `callback_ack_text`).
