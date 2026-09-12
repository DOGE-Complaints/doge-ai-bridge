# Ops, security & privacy

**Parent REQ:** [REQ-01 §7, §17–§19, §22](../../requirements/REQ-01-doge-ai-bridge-runtime.md)  
**Overview:** [00-overview.md](./00-overview.md)  
**Runbook:** [channel-bearer-rotation.md](../../runbooks/channel-bearer-rotation.md)

---

## 1. Startup & health

Fail `/readyz` when any invariant in [REQ-01 §18 AIB-OPS-01](../../requirements/REQ-01-doge-ai-bridge-runtime.md) fails (DB, Bearers distinct, `OPENAI_STORE_RESPONSES=false`, content hashes, tool strictness, pack, HTTPS origin, 201 contract, redirect base).

- `GET /healthz` — process up; no config dump.
- Graceful shutdown: no automatic gateway resend after restart.

---

## 2. Metrics & logs (interview T7 / T9)

| Signal | Rule |
|--------|------|
| Logs | Structured, redacted ([REQ-01 §19](../../requirements/REQ-01-doge-ai-bridge-runtime.md)) |
| `/metrics` | Request volume, errors, latency, confirm states, OpenAI/gateway calls, prompt-cache telemetry |
| PII / narrative / Bearer / raw nonce | Forbidden in metrics and default logs |
| Exposure | Railway **private networking only** (pilot). Future external monitor → **separate** metrics token (not channel Bearer) |
| APM SaaS | Not required for pilot |

---

## 3. Secrets

| Secret | Where |
|--------|--------|
| `AIBRIDGE_CHANNEL_BEARER_TOKEN` (+ previous for overlap) | Railway secret; n8n Header Auth only |
| `DOGESTONIA_API_BEARER_TOKEN` | Bridge only — never n8n |
| `OPENAI_API_KEY` | Bridge only |

Rotation sequence: see [channel-bearer-rotation.md](../../runbooks/channel-bearer-rotation.md).

---

## 4. Privacy (interview T9 = P1)

- Narrative + Responses items: max **7 days** from last activity (sliding with new activity).
- After stash or Cancel: may delete narrative earlier if not needed for continuation.
- Longer-lived: redacted audit metadata only.
- Channel principal ≠ Identity authentication.

---

## 5. Wave gates (operator checklist)

**Wave 1 done when:**

- [ ] Image + migrations deployed  
- [ ] `/readyz` ready  
- [ ] Smoke: channel without Bearer → 401  
- [ ] Live n8n → `POST /v1/channel/turns` over private net with Bearer → response  
- [ ] No real gateway stash (dry-run/interview)  
- [ ] `/metrics` reachable privately without PII  

**Wave 2 residual:** full Telegram dual-confirm → gateway → SPA.
