# REQ15 gaps — triage into 3 pipes (2026-11-03)

**Method:** [`.cursor/rules/analysis.mdc`](../../.cursor/rules/analysis.mdc) · Hard HIT rubric [`lightweight-followup.md` §3](../methodology/Zeya888-builder-queue/guides/lightweight-followup.md).  
**Source gaps:** [`req15-target-state-code-gap-audit-2026-11-03.md`](./req15-target-state-code-gap-audit-2026-11-03.md) (V1–V8 + AC Partial).  
**Parent:** [`../requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md`](<../requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md>).

**This document = triage classification only.** Does **not** materialize STORY/pkg, does **not** author LF dual plans / LAUNCH, does **not** change product code.  
Claim «all children completed» remains **rejected** (gap audit §1).

**Pipes:**

1. **Backlog STORY** — Builder Queue / residual stories  
2. **Lightweight follow-up** — after PASS → [`lightweight-followup-author.md`](../methodology/Zeya888-builder-queue/prompts/operator/lightweight-followup-author.md)  
3. **Accumulative simple** — batch of smallest docs/config hygiene (`req15-ops-docs-hygiene-batch`)

---

## 0. Master table

| Gap / residual | Pipe | Hard HIT (why) | builder_project | Next label |
|----------------|------|----------------|-----------------|------------|
| **V1** SPA `continuation_url` drop | **2** LF | PASS narrowed — HIT 1–10 clear under locks below | `telegram` | `telegram-continuation-url-delivery` |
| **V2** ASGI semantic/roles wire | **1** STORY | HIT 2/3/7 | `aibridge` | `aibridge-asgi-role-semantic-wire` |
| **V3** roles-schema channel cutover | **1** STORY | HIT 2/3 | `aibridge` | `roles-schema-channel-cutover` |
| **V4** live TG + Railway | **1** STORY | HIT 2/5/6 (STORY-05 unfinished + infra) | `telegram` | `telegram-story-05-live-railway` |
| **V5** Bearer env name pairing | **3** Accum | Docs/ops note only | docs (both) | in `req15-ops-docs-hygiene-batch` |
| **V6** DeepSeek primary vs `.env.example` | **3** Accum | Config/comment honesty | `aibridge` docs/env | in batch |
| **V7** gateway 59 / spa 25 no packages | **1** STORY | HIT 1/6 | `gateway` / `spa` | `gateway-59-spa-25-verify-packages` |
| **V8** export≠consume + volume | **1** STORY | HIT 2/4/7 | `aibridge` (+ ops) | `consume-parity-pass-volume` |
| Live Partial AC-04/07/08/10 | **1** STORY/ops | Evidence windows; not LF | `aibridge` / `telegram` | residual evidence gates |
| Index/dashboard Todo lag | **3** Accum | Docs cascade | `aibridge` | in batch |
| OpenAPI «n8n client» framing | **3** Accum | Docs honesty | `aibridge` | in batch |

---

## 1. Pipe 1 — Stories in backlog

Ordered for dependency honesty (not a schedule commit):

| Order | Label | Gap | Intent (no invent AC) |
|-------|-------|-----|------------------------|
| 1 | `aibridge-asgi-role-semantic-wire` | **V2** | Lift REQ-13 G-02; bind `SemanticStateService` + role select/assembly into channel turns path |
| 2 | `roles-schema-channel-cutover` | **V3** | Point channel/ready at roles-schema; retire dual `files[]` as live SSOT (pairs with V2) |
| 3 | `consume-parity-pass-volume` | **V8** | Consume Pass vs GPT-48 export inventory; hybrid C volume evidence (AC-13/14) |
| 4 | `telegram-story-05-live-railway` | **V4** | Unblock **existing** STORY-TELEGRAM-05; Railway packaging additive STORY if still Absent |
| 5 | `gateway-59-spa-25-verify-packages` | **V7** | PA.2 → `req-to-backlog-stories` for gateway 59 + spa 25 verify children |
| 6 | Live evidence residuals | AC-04/07/08/10 Partial | Ops/evidence STORY or formal gate — not Pipe 2 |

**Route:** full Builder Queue (P1.3+). Do **not** force into lightweight.

---

## 2. Pipe 2 — Lightweight follow-up (simple plan)

### V1 — `continuation_url` → Telegram chat

| Field | Value |
|-------|--------|
| **Verdict** | **PASS** (narrowed; fail closed if locks broken) |
| **builder_project** | `telegram` |
| **$slug** | `telegram-continuation-url-delivery` |
| **Parent Done** | STORY-TELEGRAM-01…04 Done (package INDEX); gap outside STORY-05 live residual |
| **As-is** | Bridge may set `continuation_url` (aibridge `gateway`/`confirm`/`channel`). Telegram [`outbound.py`](../../doge-telegram/src/doge_telegram_channel/outbound.py) / [`delivery.py`](../../doge-telegram/src/doge_telegram_channel/delivery.py) use only `reply_text` + `actions` (`_RESPONSE_KEYS_USED`) |

**HIT clear (narrowed):**

| HIT | Clear reason |
|-----|----------------|
| 1 | No new STORY — follow-up after Done 01–04 |
| 2 | No new route/API — consume Present OpenAPI field |
| 3 | Append to existing send path when field non-null |
| 4 | Single concern: outbound delivery |
| 5 | Not auth/secrets redesign |
| 6 | Parent transport stories Done |
| 7 | No P2–P7 required for append correctness |
| 8 | **telegram-only** (no aibridge edits) |
| 9 | Copy locked below — no invent marketing |
| 10 | Touch set small: outbound/delivery (+ tests/stub if present) |

**Operator locks (required for PASS):**

1. When `continuation_url` is a non-empty string, append to the message text: `\n\n` + raw URL (no extra CTA invent).  
2. When null/absent/empty — behavior unchanged.  
3. **OOS:** editing aibridge `STASH_REPLY` / embedding URL in bridge prose → HIT 8 → **ESCALATE**.

**Next:** VAL may re-run [`lightweight-followup-triage.md`](../methodology/Zeya888-builder-queue/prompts/operator/lightweight-followup-triage.md) in chat; then author via [`lightweight-followup-author.md`](../methodology/Zeya888-builder-queue/prompts/operator/lightweight-followup-author.md) (implement + validate + LAUNCH). **Not authored in this triage wave.**

---

## 3. Pipe 3 — Accumulative plan (simplest gaps)

**Slug (later author):** `req15-ops-docs-hygiene-batch`  
**Shape:** one implement plan + one validate plan (LF dual shape); **docs/config only** — no multi-runtime code (HIT 8: cross-project markdown OK).

| # | Item | Candidate surfaces (verified) |
|---|------|-------------------------------|
| A | **V5** Bearer pairing note | Document: telegram `CHANNEL_BEARER` **value** = bridge `AIBRIDGE_CHANNEL_BEARER_TOKEN`. Cite `doge-ai-bridge/.env.example` L47; telegram `example.env` / runtime notes |
| B | **V6** DeepSeek primary honesty | `doge-ai-bridge/.env.example` L93 `AIBRIDGE_INTERVIEW_PROVIDER=openai` — add explicit product-primary comment (DeepSeek once enabled) or orient default; do not invent model id beyond Present brief |
| C | Index/dashboard lag | [`doge-ai-bridge/docs/requirements/README.md`](../../doge-ai-bridge/docs/requirements/README.md) still «56…58 Todo»; [`backlog-stories/INDEX.md`](../../doge-ai-bridge/docs/tasks/backlog-stories/INDEX.md) still «0/3 Todo (62–64)» while package INDEX Done — cascade status only |
| D | OpenAPI n8n framing | [`aibridge-channel-v1.openapi.yaml`](../../doge-ai-bridge/docs/openapi/aibridge-channel-v1.openapi.yaml) header/description still «n8n ↔ aibridge» — relabel target client `doge-telegram-channel` (Keep n8n as historical optional) |
| E | Stale export-Absent one-liners | Grep remaining «export Absent» / stitch S5 echoes after gap audit supersession — docs only |

**Not in batch:** V1 (Pipe 2), V2–V4/V7/V8 (Pipe 1).

---

## 4. What this triage does / does not claim

| Claims | Does not claim |
|--------|----------------|
| Classification of known V1–V8 + listed residuals | Product Done / AC Met flips |
| V1 PASS under locked append format | LF plans/LAUNCH Present |
| Pipe 1 needs STORY/BQ | STORY files created |
| Pipe 3 inventory for later batch author | Batch implement executed |

**Closure runbook:** [`req15-gap-closure-process-zeya888-2026-11-03.md`](./req15-gap-closure-process-zeya888-2026-11-03.md) — **MVP track first** (local E2E + OpenAI + real bot → gateway); Track B = full Product Done (A/C3/D+/E/F).

**STOP** — triage complete; implement/author only on explicit operator order per pipe.
