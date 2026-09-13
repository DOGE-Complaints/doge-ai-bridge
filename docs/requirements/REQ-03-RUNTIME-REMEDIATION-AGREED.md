# REQ-03: `doge-ai-bridge` — согласованные доработки после gap + validator

**Index key:** REQ-03  
**Service / repo:** `doge-ai-bridge`  
**Parent:** [REQ-01](./REQ-01-doge-ai-bridge-runtime.md) v0.4.1 (**не изменяется** этим документом)  
**Related analysis:** [req-01-runtime-code-gap-2026-09-13.md](../analysis/req-01-runtime-code-gap-2026-09-13.md) · [req-01-gap-validator-disagreements-2026-09-13.md](../analysis/req-01-gap-validator-disagreements-2026-09-13.md)  
**Related privacy:** [privacy-pilot.md](../runbooks/privacy-pilot.md)  
**Status:** Ready for implementation  
**Version:** 0.2.1 · 2026-09-13  
**Baseline code:** commit `55f4165` (validator) — pytest 100 passed, 1 skipped (live Postgres)

---

## 1. Цель

Зафиксировать **выявленные и согласованные с внешним валидатором** доработки runtime относительно REQ-01, **без правки текста REQ-01** и без смены HTTP-контракта channel v1.

Итог аудита: на baseline — протестированные модули + живой HTTP façade/Bearer; **сквозной продукт** `Telegram → Responses → dual-confirm → gateway` ещё **не собран**.

Этот документ должен быть достаточно точным, чтобы закрытие пунктов доказывалось **поведением**, а не наличием классов.

---

## 2. Wave boundary (wave 1 vs wave 2)

**Wave 1** требует полный **логический** code path и automated E2E через fake/dry-run transports.

- Live Railway wave-1 deployment uses **`AIBRIDGE_DRY_RUN=true`** and must perform **zero** real `POST /story-drafts`.
- Until **R3-P1-03** (full schema validation) is complete, **`AIBRIDGE_DRY_RUN=false` must not pass readiness**.

**Wave 2** enables the real gateway only after every **P1** gate passes (incl. n8n/Telegram, privacy retention, full schema validation, SPA HTTPS where required).

---

## 3. Термины (clarification only — не меняет OpenAPI)

Согласовано IDE-аудит ↔ валидатор (D1 принят):

| Термин | Определение | HTTP |
|--------|-------------|------|
| **Transport replay** («replayed callback») | Повтор с тем же `(channel, event_id)` после уже сохранённого bounded response | Вернуть **stored** response; **не** повторять OpenAI/gateway |
| **New action attempt** | Новый `event_id` + уже **consumed** `action_token` | **409**; gateway **не** повторять |
| **Optional UX** | Отдать last outcome по token-hash при новом event_id | **Не** REQ FAIL, если отсутствует |

**P0:** ключи event dedupe и тела stored response — в **PostgreSQL** (replay после restart / между instances).

---

## 4. Acceptance criteria

REQ-03 считается выполненным (Done) только когда:

1. `POST /v1/channel/turns` с тестовым Responses adapter возвращает модельный interview reply, а **не** `Received: …`.

2. Повтор того же `(channel, event_id)`:
   - не создаёт второй Responses call;
   - возвращает **previously stored HTTP status and response body** (без пересчёта результата);
   - работает после restart (Postgres-backed dedupe).

3. Responses `function_call`:
   - имеет allowlisted name;
   - проходит три validation gate;
   - сохраняется с исходным `call_id`;
   - не вызывает gateway до Send confirmation.

4. Interpretation confirm:
   - изменяет состояние;
   - не выполняет gateway HTTP;
   - возвращает следующий bounded response.

5. Send confirmation:
   - проверяет owner/chat/session/deployment/revision/hash/expiry/state;
   - атомарно consumes token;
   - создаёт не более одной локальной gateway attempt;
   - выполняет только frozen body.

6. Valid gateway 201 (dry-run or fake transport in wave 1; real only wave 2):
   - возвращает `stashed`, `draft_id`, `continuation_url` (when applicable);
   - после этого отправляется `function_call_output` с исходным `call_id`;
   - финальный resident reply не утверждает публикацию Story.

7. Restart в pending-confirm сохраняет кнопки и состояние.

8. Restart при неопределённой gateway delivery не делает automatic resend.

9. Every channel response — successful, replayed and non-2xx — conforms to
   `docs/openapi/aibridge-channel-v1.openapi.yaml`.

   A transport replay returns the previously stored HTTP status and response
   body without recomputing the result or calling OpenAI/gateway again.

Closing individual backlog rows without these AC is **not** Done.

---

## 5. P0 — до содержательного wave 1

Закрыть до заявления «wave 1 = реальный runtime», не только infra smoke.

| ID | Доработка | Почему согласовано | Якорь REQ-01 |
|----|-----------|-------------------|--------------|
| R3-P0-01 | Coordinator: `/v1/channel/turns` → session repo → Responses client → tool loop → confirm | Stub `Received: …`; `InterviewEngine` не в ASGI | §6, §10, §13 |
| R3-P0-02 | Production Responses adapter (см. §5.1) | Только `RecordingResponsesClient` | §10, §17 |
| R3-P0-03 | Полный tool loop + **pause/resume** across HTTP (см. §5.2) | Engine читает только `output_text`; нельзя держать `/turns` open | §10 AIB-RSP-03 |
| R3-P0-04 | Tool shape Responses flat (`type`/`name`/`parameters`/`strict`) | Nested Chat Completions `function` | §9 |
| R3-P0-05 | PostgreSQL sole production store; **no** silent memory fallback; versioned migrations (см. §5.3) | In-memory + boot `CREATE TABLE IF NOT EXISTS` | §14 |
| R3-P0-06 | Event dedupe + stored response bodies in PostgreSQL | Transport replay after restart / instances | §6, §14 |
| R3-P0-07 | SessionStore / confirm / token repos on runtime path | `ConfirmationGuard._sessions` only | §14 |
| R3-P0-08 | Postgres row factory; disposable Postgres CI; **transactional concurrency** tests (см. §5.3–5.4) | Dict rows without factory; live test skipped | §14, §20 |
| R3-P0-09 | Strict `/readyz` without side effects (см. §5.5) | False ready | §18 |
| R3-P0-10 | Env normalization (см. §5.6) | Drift vs REQ §17 | §17 |
| R3-P0-11 | Bounded JSON **500** channel envelope | Unhandled → non-contract body | §6 AIB-CH-05 |
| R3-P0-12 | ASGI E2E fake OpenAI + gateway transports (not `"Received:"`) + Postgres | Discovers unwired interview | §20–§21 |
| R3-P0-13 | Canonical prompt assembly — **no dual instructions** (prefix **or** `instructions=`, not both) | Wrong cost/cache if duplicated on first live smoke | §11 |

### 5.1 R3-P0-02 — Production Responses adapter must

- set `store: false` on every call;
- set `parallel_tool_calls: false` for the consequential flow;
- send a finite `max_output_tokens`;
- use bounded connect/read/total timeout;
- not block the ASGI event loop;
- preserve every replay-required output item, not only `output_text`;
- parse `function_call`, `call_id`, arguments and usage;
- record cached input tokens from the actual Responses usage structure;
- map OpenAI 429/5xx/timeouts to bounded internal outcomes;
- never expose the OpenAI API key in logs or exceptions.

### 5.2 R3-P0-03 — Pause / resume tool loop

Human confirmation pauses the logical Responses tool loop across separate channel HTTP requests. No ASGI request, database transaction or OpenAI connection remains open while waiting for the Telegram callback.

The pending Responses continuation, original `call_id`, frozen body and all replayable output items are persisted **before** `/turns` returns actions.

Sequence:

1. model formed intent;
2. aibridge stored `call_id`, arguments, draft/hash;
3. `/turns` finished and returned Telegram buttons;
4. human may press Send minutes later;
5. n8n calls `/actions`;
6. aibridge restores persisted context;
7. executes gateway (dry-run in wave 1 live);
8. sends `function_call_output` in a **new** Responses request.

### 5.3 R3-P0-05–08 — PostgreSQL transactions and migrations

Required constraints / rules:

- unique `(channel, event_id)`;
- unique action token hash;
- unique `(session_id, call_id)`;
- at most one gateway attempt per authorized revision;
- database-backed serialization of one active turn per session;
- token consume + transition to `executing` + gateway-attempt creation occur **atomically before** external HTTPS;
- gateway response/outcome is stored before the bounded channel response;
- failed transaction must not advance conversation history or FSM state.

The authorization transaction MUST commit before external gateway HTTPS begins.
No PostgreSQL transaction or session lock may remain open across the network call.

Before HTTPS, the committed gateway attempt is recorded as `executing`.
After HTTPS, the outcome is stored in a separate transaction.

If the process restarts or loses the response while an attempt remains
`executing`, recovery changes it to `unknown_outcome`. Such an attempt MUST
NOT be resent automatically. Resolution requires operator reconciliation.

**Versioned migrations** are mandatory (explicit deploy step). Boot-time `CREATE TABLE IF NOT EXISTS` as the sole schema mechanism is **not** acceptable for production/pilot (REQ-01 §14 AIB-DB-02).

### 5.4 Concurrency tests vs replica load tests

| Tier | Required |
|------|----------|
| **P0/P1** | Transactional concurrency against **real PostgreSQL**; two concurrent callbacks/messages racing same session/revision; DB constraints win over app-level locks |
| **P2** | Deployment/load with multiple production ASGI **replicas**; distributed performance/capacity |

### 5.5 R3-P0-09 — `/readyz`

`/readyz` performs **no** OpenAI generation and **no** gateway write.

It verifies:

- required configuration;
- PostgreSQL connectivity and **migration version**;
- registered current content bundle;
- tool generation and strict schema;
- OpenAI model/key configuration **presence**;
- HTTPS gateway origin syntax;
- distinct Bearers;
- redirect-base validity;
- until R3-P1-03: `AIBRIDGE_DRY_RUN` must be true (or readiness fails if false).

Optional dependency connectivity probes must be read-only, bounded and cached.

### 5.6 R3-P0-10 — Env normalization

Canonical gateway variable: **`DOGESTONIA_API_BASE_URL`**.

`DOGESTONIA_GATEWAY_ORIGIN`:

- either removed;
- or accepted only as a temporary **documented** compatibility alias.

If both are present with **different** values, readiness fails.

`Settings` must actually accept (names from REQ-01 §17):

- `AIBRIDGE_SESSION_TTL_SECONDS`;
- `AIBRIDGE_ACTION_TOKEN_TTL_SECONDS`;
- `AIBRIDGE_MAX_RESPONSE_BYTES`;
- connect/total timeouts;
- log level;
- principal/global rate limits;
- all LLM budget variables.

`.env.example` must match real Settings (no false alias claims). Numeric budget **defaults** may remain measured later, but knobs must be wired and enforceable when set.

---

## 6. P1 — до допуска жителей / wave 2

| ID | Доработка | Почему согласовано | Якорь REQ-01 |
|----|-----------|-------------------|--------------|
| R3-P1-01 | Graceful shutdown (AIB-OPS-03) | Restart during Send → ambiguity | §18 |
| R3-P1-02 | Channel **429** / rate limits + finite budget defaults; budgets on `/turns` | OpenAI spend | §6, §17 |
| R3-P1-03 | Full schema validation (enum etc.); **blocks** real gateway readiness | Subset validator unsafe for live stash | §12; wave gate §2 |
| R3-P1-04 | Restart recovery + DB race/restart tests (Send / pending-confirm / unknown_outcome) | AC #7–#8 | §18, §20 |
| R3-P1-05 | *(superseded)* Dual instructions → see **R3-P0-13** | — | — |
| R3-P1-06 | Gateway response-size limit / remaining §17 timeout knobs | Ops hardness | §15, §17 |
| R3-P1-07 | Dockerfile (reproducible deploy / node clone) | Not Railpack smoke blocker | §22 |
| R3-P1-08 | Real-device HTTPS SPA continuation E2E (pilot policy) | Wave 2 resident path | §16, §21 |
| R3-P1-09 | Live n8n/Telegram integration gate (см. §6.1) | Product contour, not aibridge alone | §6 AIB-CH-06 |
| R3-P1-10 | Privacy retention enforcement (см. §6.2) | Residents require TTL + delete | §14 AIB-DB-04; privacy-pilot |

**Снято с обязательного P1 (D1):** token-hash Send replay UX — **optional enhancement** only (§3).

### 6.1 R3-P1-09 — Live n8n/Telegram integration gate

- Telegram ordinary message → n8n → `/v1/channel/turns`;
- n8n renders every returned `actions[]` as inline buttons;
- `callback_data` contains only `actions[].token`;
- n8n immediately calls Telegram `answerCallbackQuery`;
- n8n then calls `/v1/channel/actions`;
- response is rendered through Send/Edit Message;
- Telegram Bot token and channel Bearer are the only relevant n8n secrets;
- OpenAI and gateway Bearers are **absent** from n8n;
- no n8n node calls `/story-drafts`.
- `channel` is always `telegram`;
- `event_id` is deterministically derived from the Telegram update/callback
  identifier and remains unchanged across n8n retries;
- Telegram `from.id` and `chat.id` are mapped to the channel principal fields
  required by the channel OpenAPI;
- `session_id` remains stable for the active interview;
- for `/actions`, callback user/chat values must match the binding stored with
  the action token;
- n8n MUST NOT generate a new `event_id` merely because an HTTP Request node
  retries the same Telegram update.

### 6.2 R3-P1-10 — Privacy retention enforcement

- session/narrative/Responses-item TTL = configured value; pilot default **604800** seconds;
- TTL slides only on legitimate session activity;
- expired narrative is deleted or irreversibly minimized;
- expired action tokens are purged according to audit policy;
- operator session-delete mechanism exists and is tested;
- the operator session-delete mechanism is authenticated, authorized,
  fail-closed and audit-logged;
- deletion covers history, pending intents and action tokens;
- deletion or expiry must never make an already consumed action token usable;
- a minimized non-PII replay tombstone may be retained for the required
  security/audit window;
- redacted audit metadata may follow a separate retention period;
- n8n execution retention is verified separately before residents.

---

## 7. P2 — после первой ноды

| ID | Доработка |
|----|-----------|
| R3-P2-01 | Multiple production ASGI **replicas** — deploy/load/capacity (not transactional correctness — that is P0/P1) |
| R3-P2-02 | Dedicated Prometheus prompt-cache series |
| R3-P2-03 | Distributed rate limiter / external APM |
| R3-P2-04 | Credential-stripped n8n workflow JSON as ops template (not a REQ-01 code blocker) |

---

## 8. Явно не входит

- Правки текста REQ-01 / смена channel OpenAPI без отдельного решения оператора.
- REQ-02 (федерация / Identity / post-pilot).
- Inventing n8n workflow JSON as a mandatory pilot deliverable.
- Claiming Done by class presence without §4 Acceptance criteria.
- Optional token-hash UX replay after consume (non-fail if omitted).

---

## 9. Evidence pointers (baseline code)

| Fact | Path |
|------|------|
| Stub turn | `src/aibridge/channel.py` (`Received:`) |
| No live OpenAI client | `src/aibridge/responses_client.py` |
| Nested tool shape | `src/aibridge/tool_gen.py` |
| Soft readyz | `src/aibridge/app.py` |
| In-memory dedupe | `src/aibridge/dedupe.py` |
| Dual instructions risk | `src/aibridge/interview.py` |

---

## 10. History

- v0.1.0 — 2026-09-13: backlog from gap-report + validator; D1 accepted; REQ-01 body not modified.
- v0.2.0 — 2026-09-13: validator polish — Status Draft; Acceptance criteria; wave 1 dry-run vs wave 2; pause/resume tool loop; Postgres transactions/migrations; concurrency vs replicas split; Responses adapter checklist; env canon; `/readyz` no side effects; P0 dual-instructions; P1 n8n gate + privacy retention; dry-run gate until full schema validation.
- v0.2.1 — 2026-09-13: Status Ready for implementation; commit-before-HTTPS + `unknown_outcome` no auto-resend; Telegram→channel field mapping; AC #2/#9 stored status+body + OpenAPI path SSOT; privacy delete/tombstone clarifications.
