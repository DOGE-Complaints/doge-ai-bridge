# REQ-12 — REQ15: Interview DeepSeek / OpenAI providers

Parent: [docs/requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md](<../../../docs/requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md>) §3 L5–L7, §4 O2, §7, AC-04–05, AC-10  
Parent-id: REQ15-interview-deepseek-telegram  
**T1 audit:** [`../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md`](../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md) (2026-11-01T12:30:40Z)  
**Wave readiness / arch after REQ-11:** [`../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md`](../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md) — §5.2 copy-paste  
**Renumber (2026-11-01):** was aibridge REQ-11 (providers); ids `AC-AIB-11-*`/`L11-*` → `AC-AIB-12-*`/`L12-*`  
Siblings:
- [`REQ-13`](./REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) (roles call providers via this port)
- [`REQ-11`](./REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) (no provider keys on telegram/gateway path)
- [`REQ-10`](./REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) (**worker** brief/poster — **orthogonal**; do not reuse as interview switch)
- [GPT UI REQ-48](<../../../GPT UI/docs/requirements/REQ-48-req15-role-oriented-instruction-line-and-export.md>) (instruction text SSOT — not this REQ)
Status: Draft — **T1 Present** · **target tech-arch Present** · product locks Q1–Q2 2026-11-01  
Дата: 2026-10-31 · T1/hygiene: 2026-11-01 · Locks: 2026-11-01 · Renumber: 2026-11-01 · Arch: 2026-11-01  

**Architecture:** [`../architecture/req15-interview-providers/00-overview.md`](../architecture/req15-interview-providers/00-overview.md) (≠ worker [`../architecture/ai-provider-selection/00-overview.md`](../architecture/ai-provider-selection/00-overview.md))  
**Tech-arch interview:** [`../analysis/zeya888.target-tech-arch-interview-req15-interview-providers-2026-11-01.md`](../analysis/zeya888.target-tech-arch-interview-req15-interview-providers-2026-11-01.md)

---

## Целевое состояние (простыми словами)

Для **интервью** (разговор с человеком) bridge умеет явно выбрать модель: по умолчанию цель — **DeepSeek**, альтернатива — **OpenAI**. Выбор в конфиге, без тихой подмены.

Это **не** тот же переключатель, что для worker sense-brief/poster (REQ-10). Ключи моделей только на bridge. Одинаковый «порт» для ролей: отдал задачу → получил нормализованный ответ/ошибку. Особенности DeepSeek vs OpenAI прячутся в адаптерах.

---

## 1) Goal

Selectable interview providers `deepseek` (primary) | `openai`; shared port for role calls; adapters hide transport quirks; evidence per provider.

## 2) Scope / Out of scope

**In scope**

- Interview provider config + fail-closed incomplete/unknown.  
- DeepSeek adapter (Chat Completions + `base_url` where docs confirm; model id confirm at implement — brief orient `deepseek-v4-pro`).  
- OpenAI adapter (Present Responses path may remain; no forced fake unification).  
- Usage/error classification; mid-conversation switch policy = restore from canonical state + re-validate (parent L).  
- Docs: boundary vs `AIBRIDGE_WORKER_*_PROVIDER` / REQ-10.

**Out of scope**

- Worker brief/poster providers (REQ-10).  
- Instruction authoring (GPT UI REQ-48).  
- Telegram transport.  
- Gateway stash implementation (REQ-11).  
- Fine-tunes / hosted agent platforms.  
- Inventing exact env var names as SSOT before operator lock / Architect Studio.

## 3) Verified current state (T1)

| Fact | Path / note |
|------|-------------|
| Interview/channel OpenAI Responses | [`app.py`](../../src/aibridge/app.py) wires `ProductionResponsesClient` when `OPENAI_API_KEY` Present (~414–426); [`responses_client.py`](../../src/aibridge/responses_client.py) |
| Interview DeepSeek / selectable interview provider id | **Absent** in `src/` (T1) |
| Worker provider ports | REQ-10 / `AIBRIDGE_WORKER_*_PROVIDER` — separate; must not become interview switch |
| T1 verdict for this focus | OpenAI Responses path **Keep** as openai adapter; interview selector + DeepSeek **Replace** (new) |

## 4) Target behavior

1. Explicit interview provider id via **`AIBRIDGE_INTERVIEW_PROVIDER`** (`deepseek`\|`openai`); primary DeepSeek when enabled (L12-1).  
2. Role runtime calls only the shared port — **all five REQ-13 roles** (`communication_setup` · `interviewer` · `extractor` · `normalizer` · `checker`) invoke models **only** through this interview port (`interview_providers/` · `bind_role_interview_engine`); never worker `AIBRIDGE_WORKER_*_PROVIDER`.  
3. No silent fallback to paid OpenAI when DeepSeek selected.  
4. Stub + live evidence recorded **per** provider (parent AC-10). Provider comparison / parity claims must cite the **same** exported role bundle + session pin (REQ-13 assembly); otherwise DeepSeek vs OpenAI evidence is not role-outcome parity.  
5. Mid-conversation switch: controlled restore from canonical state + re-validate (not silent flip).

## 5) Acceptance criteria

| ID | Criterion | Parent map |
|----|-----------|------------|
| **AC-AIB-12-01** | Config selects `deepseek` \| `openai` for interview only | AC-REQ15-04 |
| **AC-AIB-12-02** | Worker REQ-10 env **cannot** act as interview provider switch | AC-REQ15-05 |
| **AC-AIB-12-03** | Both adapters produce usable role outcomes under harness | AC-REQ15-04 / O2 |
| **AC-AIB-12-04** | Live evidence path documented per provider (when live enabled) | AC-REQ15-10 |
| **AC-AIB-12-05** | Unknown/incomplete provider config → fail-closed | AC-REQ15-04 spirit |

## 6) Interview locks (operator 2026-11-01)

| ID | Lock |
|----|------|
| **L12-1** | Interview provider env name family: **`AIBRIDGE_INTERVIEW_PROVIDER`** ∈ {`deepseek`,`openai`} (≠ `AIBRIDGE_WORKER_*_PROVIDER`) |
| **L12-2** | DeepSeek **model id** not frozen for live Pass — confirm availability before live claim; brief orient / `.env.example` default: `deepseek-v4-pro` |
| **L12-3** | DeepSeek nest env **names** (operator 2026-11-01): **`AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY`**, **`AIBRIDGE_INTERVIEW_DEEPSEEK_BASE_URL`** (example default `https://api.deepseek.com`), **`AIBRIDGE_INTERVIEW_DEEPSEEK_MODEL`**. Required when provider=`deepseek`. OpenAI nest Keep: **`OPENAI_API_KEY`** + **`OPENAI_MODEL`**. Template: [`.env.example`](../../.env.example) §4b |

## 7) Open (residual)

| Item | Class | Next |
|------|-------|------|
| Adapter module layout, HTTP client reuse | **Locked in arch (D1/D3)** | Package `req15-interview-providers/`; Keep Engine; port supplies backend; ≠ worker `providers/` |
| Fail reason strings | **Open (implement)** | Typed classes in arch `02`; literals not SSOT here |
| Mid-conversation switch | **Locked v1 (D4)** | Wire/start only; in-session flip = future product+arch |
| Concrete DeepSeek model string after live check | **Product / ops** | After L12-2 confirm; orient `deepseek-v4-pro` |
| DeepSeek key/base_url/model env **names** | **Locked L12-3** | See §6; `.env.example` §4b Present |

## 8) Functional vs tech split

| Layer | Lives in |
|-------|----------|
| Product / AC | This REQ + parent REQ15 |
| Target tech | [`../architecture/req15-interview-providers/00-overview.md`](../architecture/req15-interview-providers/00-overview.md) |
| Work items | [`STORY-AIBRIDGE-59…61`](../tasks/backlog-stories/req-12-req15-interview-deepseek-openai-providers/INDEX.md) Present · P8 Done · AC-04 live Partial |

**Next process step (operator):** REQ-13 STORY-62…64 Product Done (ASGI residual WAIVED) · peer **GPT UI REQ-48** for export/consume · residual live **AC-AIB-12-04** per provider when ops window (joint with AC-AIB-11-07 for full AC-REQ15-10).
