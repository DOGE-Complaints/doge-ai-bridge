# Runbook — privacy (pilot / first node)

**Service:** `doge-ai-bridge` + n8n Telegram UI  
**Related:** [REQ-01 §14, §19](../requirements/REQ-01-doge-ai-bridge-runtime.md) · [04-ops-security.md](../architecture/runtime/04-ops-security.md)  
**As-of:** 2026-09-12

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

## 2. aibridge checklist

- [ ] Session narrative TTL = 7 days from last activity (slides on activity)
- [ ] Early narrative delete after `stashed` or `cancelled` when continuation unused
- [ ] Audit metadata retained without full text
- [ ] Operator session-delete mechanism exists and is tested
- [ ] Backup retention documented; delete vs backup restore behavior agreed
- [ ] stdout and `/metrics` free of narrative/PII/secrets (test with unique phrase)

---

## 3. n8n checklist

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
