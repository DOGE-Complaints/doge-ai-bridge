# R3-P1-09 — Live n8n / Telegram integration gate checklist

**Story:** STORY-AIBRIDGE-15-n8n-telegram-gate  
**REQ:** [REQ-03 §6.1](../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md)  
**Ops contract:** [README.md](./README.md)  
**Channel OpenAPI SSOT:** [aibridge-channel-v1.openapi.yaml](../../openapi/aibridge-channel-v1.openapi.yaml)  
**As-of:** 2026-09-13T17:31:50Z  

Executable checklist. Checkboxes are for **live** operator proof. Simulated/contract coverage lives in `tests/test_story_15_n8n_gate_contract.py` (no Bot tokens).

**Do not invent** channel OpenAPI fields. **Do not** commit Bot / channel / gateway / OpenAI secrets.

---

## A. Routing shape (Scope #1–#3)

| # | Check | Live | Contract/docs |
|---|-------|------|---------------|
| A1 | Telegram ordinary message → n8n → `POST /v1/channel/turns` | [ ] | README §2 flow |
| A2 | Every returned `actions[]` rendered as inline buttons | [ ] | README §3 response→Telegram |
| A3 | `callback_data` = `actions[].token` only (≤64 bytes) | [ ] | README §1 / §3 |
| A4 | On `callback_query`: immediate Telegram `answerCallbackQuery` (neutral/empty) **before** aibridge | [ ] | README §2 |
| A5 | Then `POST /v1/channel/actions` with opaque token + principal | [ ] | README §2–§3 |
| A6 | Then Send Message / Edit Message from aibridge `reply_text` / `actions` | [ ] | README §2 |

## B. Secrets & anti-patterns (Scope #4)

| # | Check | Live | Contract/docs |
|---|-------|------|---------------|
| B1 | n8n secrets = Telegram Bot token + channel Bearer only | [ ] | README §4 |
| B2 | OpenAI API key **absent** from n8n credentials/nodes | [ ] | README §4 |
| B3 | Gateway Bearer / gateway base URL **absent** from n8n | [ ] | README §2 hard rules |
| B4 | No n8n node calls `/story-drafts` | [ ] | README §2 / smoke §5 |

## C. Field mapping & binding (Scope #5–#9)

| # | Check | Live | Contract/docs |
|---|-------|------|---------------|
| C1 | `channel` always constant `telegram` | [ ] | README §3 · OAS · `test_story_15_*` |
| C2 | `event_id` = Telegram **update id** (decimal string) for messages | [ ] | README §3 · derivation § below |
| C3 | `event_id` for callbacks = same Telegram **update id** (not a random UUID) | [ ] | README §3 |
| C4 | HTTP Request **retry** of the same update reuses the **same** `event_id` (no mint) | [ ] | § D · Target AC #2 · tests |
| C5 | `principal.user_id` ← `from.id` (decimal string) | [ ] | README §3 · tests |
| C6 | `principal.chat_id` ← `chat.id` / `message.chat.id` (decimal string) | [ ] | README §3 · tests |
| C7 | `session_id` stable across turns for the active interview (same principal) | [ ] | façade behavior · tests |
| C8 | `/actions` callback principal matches token binding (wrong owner → 403) | [ ] | story 13/15 contract tests |

## D. `event_id` derivation (retry-safe)

Documented formula (n8n expression must implement this — not invent UUIDs):

```text
event_id = String(telegram_update.update_id)
```

For `callback_query` paths, still use the enclosing update's `update_id` as `event_id`.  
`callback_query_id` is a **separate** field (`callback_query.id`) — never substitute it for `event_id`.

**Retry rule (REQ-03 §6.1):** if n8n HTTP Request node retries the same Telegram update, the body must keep the **identical** `event_id`. Aibridge dedupe then returns the stored response; a new id would falsely re-run the interview.

## E. Live evidence pack (Target #1)

| Artifact | Status |
|----------|--------|
| Screenshots / n8n execution logs (redacted) | see [live-evidence-BLOCKED-20260913.md](./live-evidence-BLOCKED-20260913.md) |
| Recorded integration test (no live Bot) | `tests/test_story_15_n8n_gate_contract.py` |
| Credential-stripped workflow JSON | **Out of story scope** (P2-04); do not invent |

## F. Cross-links

- Wave-1 façade smoke (partial): [wave1-gate-checklist.md](../wave1-gate-checklist.md)  
- This file is the **§6.1 / R3-P1-09** SSOT for STORY-AIBRIDGE-15.

---

## N8N-WF-001 pinned export smoke (out of CI)

<a id="n8n-wf-001-pinned-export-smoke-out-of-ci"></a>

**Story:** STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty  
**Pin pointer:** package `fixtures/meta/n8n-wf-001-pin-pointer.json` → promote copy `tests/fixtures/meta/`  
**Export path (operator):** `docs/ops/n8n-channel-workflow/exports/aibridge-telegram-channel-v1.json`  
**Default CI / pytest:** **NO** — this section is **out-of-CI only**. Do not invent Railway SUCCESS or live Telegram PASS in CI.

| # | Check | Live (ops) | Notes |
|---|-------|------------|-------|
| W1 | Credential-stripped export present at path above | [ ] | Do **not** invent JSON body |
| W2 | `sha256` recorded in pin pointer matches file on disk | [ ] | Update pointer + promote=copy after place |
| W3 | Layer E docs still label `tests/n8n/` as **adapter-contract** | [ ] | TECH §5.1 · package INDEX |
| W4 | Optional dry-run smoke against pinned workflow (dedicated test bot) | [ ] | Secrets never committed; Gate-5 ownership → STORY-37 |

When export is absent, pin pointer `payload.status=deferred` remains honest coverage until operator places the file.

---

## Gate-5 — live channel pilot (out of CI)

<a id="gate-5-live-channel-pilot-out-of-ci"></a>

**Story:** STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence  
**Guide:** §15 Gate-5 · Layer F  
**Evidence index:** package `fixtures/meta/gate5-evidence-index.json` → promote copy `tests/fixtures/meta/`  
**Default CI / pytest:** **NO** — out-of-CI only. Do **not** invent Railway SUCCESS or live Telegram PASS. UC-01…10 (STORY-34) are **not** Gate-5.

| # | Check (guide §15) | Live (ops) | Notes |
|---|-------------------|------------|-------|
| G1 | Real Telegram → n8n → private aibridge → response works in **dry-run** | [ ] | Dedicated test bot/chat; secrets never committed |
| G2 | Callback acknowledged immediately (`answerCallbackQuery` before `/actions`) | [ ] | See ops README §2 ack order |
| G3 | One authorized **staging** stash returns SPA continuation URL | [ ] | After dry-run; no production Story submit |
| G4 | Resident-facing text never claims the draft is published | [ ] | No claim_published wording |

**If pilot env absent:** leave checks unchecked; keep `gate5-evidence-index.json` `status=deferred` + `defer_reason`; Gate-5 TRACEABILITY / fixture-index program stay `deferred_live`. Do **not** fake screenshots/logs.
