# Ops, security & privacy

**Parent REQ:** [REQ-01 §7, §17–§19, §22](../../requirements/REQ-01-doge-ai-bridge-runtime.md)  
**Overview:** [00-overview.md](./00-overview.md)  
**Runbooks:** [channel-bearer-rotation.md](../../runbooks/channel-bearer-rotation.md) · [privacy-pilot.md](../../runbooks/privacy-pilot.md) · [unknown-outcome-reconciliation.md](../../runbooks/unknown-outcome-reconciliation.md)

---

## 1. Startup & health

Fail `/readyz` when invariants in REQ-01 §18 fail (DB/migrations, Bearers distinct, `OPENAI_STORE_RESPONSES=false`, content hashes, tool strictness, pack, HTTPS origin, 201 contract, redirect base, **current** bundle registered).

- `GET /healthz` — process up; no config dump.
- Graceful shutdown: no automatic gateway resend after restart.
- Security-relevant rows carry server-owned `deployment_id` / `node_id` (never client-routed).

---

## 2. LLM budget policy (required knobs)

Exact pilot numbers are **Unknown** until measured; architecture requires these env knobs and bounded breach behavior:

| Variable | Meaning |
|----------|---------|
| `AIBRIDGE_MAX_INPUT_TOKENS` | Cap input context |
| `AIBRIDGE_MAX_OUTPUT_TOKENS` | Cap model output |
| `AIBRIDGE_MAX_RESPONSES_CALLS_PER_TURN` | Cap OpenAI calls per Telegram event/turn |
| `AIBRIDGE_MAX_TOOL_CALLS_PER_TURN` | Cap tool calls per turn |
| `AIBRIDGE_OPENAI_TIMEOUT_MS` | Hard timeout for Responses |
| `AIBRIDGE_MAX_SESSION_TURNS` | Cap turns per session |
| `AIBRIDGE_PRINCIPAL_RATE_LIMIT` | Per channel principal |
| `AIBRIDGE_GLOBAL_RATE_LIMIT` | Per channel credential / deployment |

On breach: bounded fail, resident-safe text, no gateway side effect, last confirmed state kept, redacted metric with reason ([03-confirm-gateway.md](./03-confirm-gateway.md)).

---

## 3. Metrics & logs

| Signal | Rule |
|--------|------|
| Logs | Structured, redacted |
| `/metrics` | RPS, errors, latency, confirm states, OpenAI/gateway calls, prompt-cache, **budget-stop reasons** |
| PII / narrative / Bearer / raw nonce | Forbidden |
| Exposure | Private networking only (pilot). Future scrape → separate metrics token (not channel Bearer) |
| APM SaaS | Not required for pilot |

---

## 4. Secrets

| Secret | Where |
|--------|--------|
| `AIBRIDGE_CHANNEL_BEARER_TOKEN` (+ previous) | Railway; n8n Header Auth |
| `DOGESTONIA_API_BEARER_TOKEN` | Bridge only |
| `OPENAI_API_KEY` | Bridge only |

Rotation: [channel-bearer-rotation.md](../../runbooks/channel-bearer-rotation.md). Also summarized in Operator README (REQ deliverable).

---

## 5. Privacy

See [privacy-pilot.md](../../runbooks/privacy-pilot.md).

- Narrative + Responses items ≤ **7 days** sliding; early delete after stash/Cancel when unused.
- Redacted audit metadata may live longer.
- n8n must not retain full success payloads indefinitely; channel principal ≠ Identity.
- `store: false` limits OpenAI Conversation storage — it does **not** mean “no AI processing.”
- Backup retention vs session delete: define operationally in privacy runbook before real residents.

---

## 6. Wave & node release checklists

**Wave 1 done when:**

- [ ] Image + migrations + current bundle registered  
- [ ] `/readyz` ready  
- [ ] Smoke: no Bearer → 401  
- [ ] Live n8n → `/v1/channel/turns` (private + Bearer)  
- [ ] No real gateway stash  
- [ ] `/metrics` private, no PII  
- [ ] Budget env present (numbers may be provisional)

**Wave 2 / real residents additionally:**

- [ ] Dual-confirm E2E (RU/ET/EN as required)  
- [ ] User-reachable **HTTPS** SPA continuation URL (mobile Telegram test)  
- [ ] n8n privacy settings verified  
- [ ] Privacy notice before substantive interview  
- [ ] `unknown_outcome` runbook practiced  
- [ ] Narrative delete path tested  

**New node release (same image):**

1. Manifest/OAS/pack hashes verified  
2. Migrations  
3. `/readyz`  
4. Unauthenticated façade → 401  
5. Live n8n → `/turns` with channel Bearer  
6. No real stash in wave-1 style smoke  
7. Separate wave-2 E2E when enabling residents  
8. n8n privacy check  
9. SPA URL check on real device  
