# REQ-11 — REQ15: Dual confirm, gateway stash, SPA handoff (server pipe)

Parent: [docs/requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md](<../../../docs/requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md>) §3 L4, L11–L12, §4 O7, §5 seq-03, AC-07–08  
Parent-id: REQ15-interview-deepseek-telegram  
**T1 audit:** [`../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md`](../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md) (2026-11-01T12:30:40Z)  
**Wave readiness / next arch (first):** [`../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md`](../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md) — order **11 → 12 → 13**; §5.1 copy-paste  
**Renumber (2026-11-01):** was aibridge REQ-13 (dual-confirm); ids `AC-AIB-13-*`/`L13-1` → `AC-AIB-11-*`/`L11-1`  
Siblings:
- [`REQ-13`](./REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) (state/roles; prompts must **not** own this pipe)
- [`REQ-12`](./REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) (interview providers/keys on bridge; submit path does not depend on DeepSeek vs OpenAI except evidence recording)
- [GPT UI REQ-48](<../../../GPT UI/docs/requirements/REQ-48-req15-role-oriented-instruction-line-and-export.md>) (new instruction line strips model-owned stash/redirect)
- [gateway 59](../../../doge-complaints-gateway/docs/requirements/59-req15-story-draft-stash-channel-parity-verify.md) (stash contract verify)
- [spa 25](../../../spa-app/docs/requirements/25-req15-story-submit-handoff-continuity-verify.md) (`#/story/submit?draft_id=` verify)
- [doge-telegram REQ-01](../../../doge-telegram/docs/requirements/REQ-01-REQ15-TELEGRAM-CHANNEL-TRANSPORT.md) (delivers link text only; no gateway write)
Status: Draft — **T1 Present** · **target tech-arch Present** · product lock Q5 2026-11-01  
Дата: 2026-10-31 · T1/hygiene: 2026-11-01 · Locks: 2026-11-01 · Renumber: 2026-11-01 · Arch: 2026-11-01  

**Architecture:** [`../architecture/req15-dual-confirm-handoff/00-overview.md`](../architecture/req15-dual-confirm-handoff/00-overview.md) (delta; Keep SSOT [`../architecture/runtime/03-confirm-gateway.md`](../architecture/runtime/03-confirm-gateway.md))  
**Tech-arch interview:** [`../analysis/zeya888.target-tech-arch-interview-req15-dual-confirm-handoff-2026-11-01.md`](../analysis/zeya888.target-tech-arch-interview-req15-dual-confirm-handoff-2026-11-01.md)

---

## Целевое состояние (простыми словами)

Раньше Custom GPT через Actions **сам** вызывал `POST /story-drafts` и говорил человеку открыть SPA.  
Теперь это делает **сервер aibridge** в пайпе с агентами/ролями:

1. человек подтверждает, что **понимание** верное;  
2. отдельно — что **эту** версию черновика можно отправить;  
3. код (не модель) бьёт в gateway по URL из **конфига**;  
4. успех только если gateway реально ответил успехом;  
5. человеку уходит ссылка продолжения в SPA (`#/story/submit?draft_id=…`); публикация истории по-прежнему в браузере под сессией.

Смена смысла или текста черновика сбрасывает зависимые проверки и право на отправку. Telegram-сервис только доставляет сообщения/кнопки — **без** ключей моделей и **без** записи в gateway.

**T1:** ядро этого пайпа в коде уже **Present (Keep)** — Architect Studio mainly coexistence + hooks from REQ-13 semantic invalidation + evidence.

---

## 1) Goal

Preserve dual human confirms + factual gateway stash + SPA continuation as **application/server** responsibilities between roles; model never chooses submit URL or holds Bearer.

## 2) Scope / Out of scope

**In scope**

- Distinct confirms: (1) understanding OK, (2) send **this** draft version (versions/hashes/tokens).  
- Invalidation when meaning or draft text changes (L13) — including hooks when REQ-13 semantic state changes (not only EDIT action).  
- Gateway client: config URL; success only on actual success response; stash ≠ publication.  
- Build continuation URL for SPA hash route with `draft_id`.  
- Wire outcomes back through coordinator → telegram channel for user-visible link/errors (no blind resend).  
- Content/PII checks beyond schema-only where parent O7 requires (coordinate with role Checker; enforcement in code gates).  
- Re-verify Present bridge stash/handoff mechanisms against Custom GPT era behavior (parity of **outcome**, new **owner**).

**Out of scope**

- Rewriting gateway stash schema or inventing new draft API (gateway 59 verify-first).  
- SPA submit UX redesign (spa 25 verify-first).  
- Instruction markdown authoring (GPT UI REQ-48).  
- Provider adapters (REQ-12).  
- Sense-brief/poster worker.  
- Inventing new confirm storage schemas as SSOT before Architect Studio.

## 3) Verified current state (T1)

| Fact | Path / note |
|------|-------------|
| Bridge stash + continuation | [`gateway.py`](../../src/aibridge/gateway.py) `execute_stash` · `build_continuation_url` → `{SPA}/#/story/submit?draft_id=` (~L118–120) |
| Channel turns/actions | [`app.py`](../../src/aibridge/app.py) `/v1/channel/turns` · `/v1/channel/actions` |
| Dual-confirm FSM + guard | [`confirm_fsm.py`](../../src/aibridge/confirm_fsm.py) · [`confirm.py`](../../src/aibridge/confirm.py) |
| Custom GPT model-owned path | GPT UI [`api-orchestrator.md`](<../../../GPT UI/instructions/api-orchestrator.md>) Actions `postStoryDraftStash` + §5.2.B redirect |
| T1 verdict | Dual confirm + stash + SPA **Keep**; semantic-driven invalidation **Partial**; live E2E evidence **Unknown** |

## 4) Target behavior

1. After Checker/gates: understanding confirm ≠ send confirm.  
2. Only code performs HTTPS stash with service credentials.  
3. On factual success: emit SPA continuation; telegram delivers it.  
4. On failure: clear error; no assuming success; no silent duplicate send policy without explicit design.  
5. Instruction modules no longer describe model HTTP to gateway (REQ-48/13).  
6. **L11-1 / Q5:** When REQ-13 semantic state is Present, meaning change invalidates send permission **without** requiring Telegram EDIT (target A). Until then, Present EDIT/revision path remains the enforce point (transition C).

## 5) Acceptance criteria

| ID | Criterion | Parent map |
|----|-----------|------------|
| **AC-AIB-11-01** | Two distinct confirm stages enforced in process | AC-REQ15-07 |
| **AC-AIB-11-02** | Meaning/draft change invalidates dependent send permission; with semantic state Present, meaning change does so **without** requiring EDIT (L11-1 target A); pre-state = EDIT/revision (transition C) | AC-REQ15-07 · L13 · L11-1 |
| **AC-AIB-11-03** | Submit URL from bridge config only; model cannot supply arbitrary gateway URL | L4 · AC-REQ15-08 |
| **AC-AIB-11-04** | User-visible success only after factual gateway success | AC-REQ15-08 |
| **AC-AIB-11-05** | Continuation link uses Present SPA hash contract with `draft_id` | spa 25 |
| **AC-AIB-11-06** | Telegram service never performs stash (secrets stay on bridge) | AC-REQ15-03 |
| **AC-AIB-11-07** | Evidence: stub + at least one live path Telegram→bridge→gateway→SPA open (when live window) | AC-REQ15-10 |

## 6) Interview locks (operator 2026-11-01)

| ID | Lock |
|----|------|
| **L11-1** | **Q5 accepted:** target **A** (semantic meaning change → invalidate send) + transition **C** (until state Present, EDIT/revision only). Same as REQ-13 **L13-3**. |

## 7) Open (residual)

| Item | Class | Next |
|------|-------|------|
| Exact confirm token/hash storage beyond Present | **Locked in arch (D3)** | Reuse Present ActionToken/`draft_hash`; Adapt only if REQ-13 proves gap |
| Whether Responses tool loop remains internal vs pure role chat | **Locked in arch (D4)** | Keep internal tool-intent as transition; hard-cut = REQ-13/48 later |
| When live evidence window is mandatory for Done | **Locked policy (D5) + ops calendar Open** | Stub required; live Pass only with window; else AC-07 Partial |
| Sensitivity: which state updates = meaning change | **REQ-13** + thin product | Under L11-1 / L13-3; named seam in arch `02-l11-invalidation-seam.md` |

## 8) Functional vs tech split

| Layer | Lives in |
|-------|----------|
| Product / AC | This REQ + parent REQ15 |
| Target tech | [`../architecture/req15-dual-confirm-handoff/00-overview.md`](../architecture/req15-dual-confirm-handoff/00-overview.md) |
| Work items | backlog STORY (later) |

**Backlog stories:** [`../tasks/backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md`](../tasks/backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md) — STORY-AIBRIDGE-56…58 Todo (2026-11-01T14:15:37Z)  

**Next process step (operator):** optional PA.3 refine stories · P1.3 per story when go-ahead · next aibridge arch wave = **REQ-12**.
