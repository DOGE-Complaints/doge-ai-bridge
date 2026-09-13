# Runbook — privacy (pilot / first node)

**Service:** `doge-ai-bridge` + n8n Telegram UI  
**Related:** [REQ-01 §14, §19](../requirements/REQ-01-doge-ai-bridge-runtime.md) · [04-ops-security.md](../architecture/runtime/04-ops-security.md)  
**As-of:** 2026-09-13

Complete this before inviting real residents (wave 2). Organizational processors/controllers are recorded outside this file; do not invent legal entity names here.

---

## 1. Data path (who sees narrative)

| Hop | What may contain resident text | Control |
|-----|--------------------------------|---------|
| Telegram | Messages, callbacks | Telegram as processor; short privacy notice before interview |
| n8n | Execution payloads if saved | Minimize/disable success retention; short error retention; no pinning real data; no narrative in custom logs |
| aibridge Postgres | Session narrative + Responses items | ≤7 days sliding; early delete after stash/Cancel; operator delete |
| OpenAI Responses | Prompt/history for the call | `store: false`; still processed ephemerally — do not claim “no AI processing” |
| Logs / `/metrics` | Must not | Redaction tests |
| Gateway stash | Draft body after Send | Gateway policies; not aibridge log dump |

Channel `user_id`/`chat_id` is a **Telegram principal**, not DOGEstonia Identity.

---

### Ops residual before residents (G-03 / STORY-16 audit)

The unchecked items below (n8n retention evidence, early delete after stash/Cancel,
backup vs delete agreement) are **ops-before-residents** residuals — not inventing
PASS in CI. Code Target AC for R3-P1-10 (TTL, minimize, ops-delete authz, consumed
invariant, no channel OAS invent) is covered by automated tests; close these
checkboxes with operator evidence before inviting real residents.

## 2. aibridge checklist

- [x] Session narrative TTL = 7 days from last activity (slides on activity) — default `AIBRIDGE_SESSION_TTL_SECONDS=604800` (code)
- [ ] Early narrative delete after `stashed` or `cancelled` when continuation unused *(ops-before-residents residual)*
- [x] Audit metadata retained without full text (code: `audit_event` redaction)
- [x] Operator session-delete mechanism exists and is tested (ops CLI + library)
- [ ] Backup retention documented; delete vs backup restore behavior agreed *(ops-before-residents residual)*
- [x] stdout and `/metrics` free of narrative/PII/secrets (test with unique phrase) — covered in ops wave tests

### Operator session-delete (ops-only — HTTP path Unknown)

**Do not** invent a channel OpenAPI delete route. Until an explicit operator decision sets an HTTP path:

1. Authz: present `AIBRIDGE_OPS_BEARER_TOKEN` (distinct from channel Bearer). Empty/mismatch → **fail-closed**.
2. CLI surface: `DATABASE_URL=postgres://… AIBRIDGE_OPS_BEARER_TOKEN=… python -m aibridge.ops_session_delete --session-id <id> --ops-bearer <token>`
3. Library: `aibridge.privacy_retention.ops_delete_session(...)` — minimizes narrative to tombstone, invalidates pending tokens, drops confirm binding; **consumed tokens stay non-usable**.
4. Audit: redacted `ops_session_delete` event (no narrative body).

n8n execution retention (section 3) is verified **separately** before residents.

---

## 3. n8n checklist

> **G-03 residual:** verify before residents (ops evidence). Unchecked ≠ code regression.

- [ ] Success executions: save minimized or disabled for production workflow
- [ ] Error executions: short retention; purge schedule configured
- [ ] No pinned executions containing real resident data
- [ ] No custom nodes logging full Telegram payload / aibridge reply narrative
- [ ] Credentials store only Bot token + channel Bearer (never gateway Bearer / OpenAI key)
- [ ] After retention window, unique test phrase absent from success execution records

---

## 4. Resident-facing notice (before substantive interview)

Must cover, in plain language:

- Communication via Telegram
- Processing with AI (OpenAI) to draft the complaint
- Purpose: prepare a draft for DOGEstonia review (stash ≠ published Story)
- Telegram identity is not verified DOGEstonia Identity in this release

Do not promise publication after stash.

---

## 5. Proof before go-live

1. Run scripted unique phrase through n8n → aibridge turn.  
2. Confirm phrase absent from logs/metrics.  
3. After n8n retention window, confirm absent from success executions.  
4. Delete session via operator path; confirm narrative gone (audit metadata may remain redacted).
