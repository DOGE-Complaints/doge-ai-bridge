# REQ-01 runtime — code gap matrix (2026-09-13)

**Scope:** сверка [`REQ-01-doge-ai-bridge-runtime.md`](../requirements/REQ-01-doge-ai-bridge-runtime.md) v0.4.1 с кодом в `doge-ai-bridge/src/aibridge/`  
**Method:** analysis.mdc — только Read/Grep evidence; REQ-чекбоксы §21 **не** менялись в REQ-файле  
**As-of:** 2026-09-13 · **Rev:** интегрирован внешний validator review (см. §0, §6)  
**Baseline commit (validator):** [`55f4165`](https://github.com/DOGE-Complaints/doge-ai-bridge/commit/55f4165e2789bd4360367505aa3e7428117ee73e) — pytest **100 passed, 1 skipped** (skipped = live PostgreSQL)  
**Disagreements with validator:** [`req-01-gap-validator-disagreements-2026-09-13.md`](./req-01-gap-validator-disagreements-2026-09-13.md)

---

## 0. Overall verdict (revised)

Предыдущая редакция этого отчёта **переоценила готовность** runtime как продукта.

На `55f4165`:

- модульные тесты зелёные; HTTP façade + Channel Bearer работают;
- отдельные библиотеки (tool_gen, InterviewEngine, confirm, gateway executor) существуют;
- **сквозной путь** `Telegram → Responses → dual-confirm → gateway` **не собран** в production ASGI.

Итог: хороший набор протестированных деталей, **не** работающий aibridge как единый транзакционный runtime. Live n8n smoke доказывает сеть и Bearer, не интервью.

Приоритеты ниже: **P0** до содержательного wave 1; **P1** до жителей / wave 2; **P2** после первой ноды.

---

## 1. HTTP surface vs §6 / §7 / §18

| REQ | Claim | Verdict | Pri | Evidence |
|-----|-------|---------|-----|----------|
| AIB-CH-01 | Base `/v1`, JSON, Bearer, decimal IDs, forbid extras, size bound, no CORS | **PASS** | — | `app.py`; `schemas.py`; no CORSMiddleware |
| AIB-CH-02/03 | Routes `turns` / `actions` exist | **PASS** (wire) | — | `app.py:282–328` |
| AIB-CH-02 behavior | Turn drives interview / Responses | **FAIL** | **P0** | `channel.py:55–81` — stub `Received: …`; `InterviewEngine` **не** вызывается |
| AIB-CH-04 | Success envelope; no `callback_ack_text` | **PASS** | — | `schemas.py:71–83`; OAS |
| AIB-CH-05 | Status matrix incl. channel **429** + bounded **500** | **PARTIAL** | **P0** 500 · **P1** 429 | 200/400/401/403/404/409/413/422/503 есть. Channel **429** не отдаётся. Unhandled → не контрактный JSON **500** (нет handler) |
| AIB-AUTH-01/02 | Bearer ≠ gateway; constant-time | **PASS** | — | `auth.py`; `readyz` equal check |
| AIB-OPS-02 | `/healthz` / `/readyz` | **PARTIAL** | **P0** | Liveness OK (`app.py:239–241`). **`/readyz` ложно-ready** при отсутствии DB/OpenAI/bundle/gateway — проверяет почти только channel Bearer (`app.py:243–271`); противоречит REQ §18 |
| AIB-OPS-03 | Graceful shutdown | **GAP** | **P1** | Нет `lifespan`/`shutdown` в `src/`. Не дублировать как отдельную «health vs shutdown» проблему — один gap |

---

## 2. §21 Acceptance criteria (revised)

| # | REQ claim (abbrev.) | Verdict | Pri | Evidence / note |
|---|---------------------|---------|-----|-----------------|
| 1 | Two versioned channel endpoints as §6 | **PARTIAL** | **P0** | Routes PASS; turn semantics stub (`channel.py:75–79`) |
| 2 | n8n two HTTP Request nodes, no fork | **PASS** (API) | — | Endpoints достаточны для двух HTTP Request. **Committed workflow JSON не deliverable REQ** (§3.2 / §22 «Explicitly not delivered… inventing unverified workflow JSON»). Ops export — позже, не code-blocker |
| 3 | Channel Bearer distinct from gateway | **PASS** | — | middleware + `readyz` |
| 4 | PostgreSQL persists sessions, events, tokens, intents, outcomes | **FAIL** | **P0** | Persist: `content_bundle` + `session` tables. In-memory: tokens (`action_tokens.py`), confirm (`confirm.py` `_sessions`), dedupe (`dedupe.py`), history (`history.py`). `app.state.session_store` **не** используется `process_turn` — runtime ходит в `ConfirmationGuard._sessions` |
| 5 | Dedupe + serialization across instances | **PARTIAL** | **P0** DB-dedupe/atomic Send · **P2** multi-replica suite | In-process only (`dedupe.py`, `turn_lock.py`) |
| 6 | `store:false` + replayable history in Postgres | **FAIL** | **P0** | Assemble forces `store:false`. History — memory (`history.py`). REQ §10: history in PostgreSQL |
| 7 | Bundle pin / registry / GC | **PASS** (module) | — | Modules+tests; production path still optional via `content_configured()` |
| 8 | Wire OAS SSOT | **PASS** | — | `story-intake-actions.openapi.yaml` |
| 9 | Strict deterministic tool **for Responses** | **FAIL** | **P0** | `tool_gen.py:238–252` emits Chat Completions nested `function:{…}`; Responses ожидает flat `type/name/parameters/strict`. Unit «strict» PASS ≠ runtime-compatible tool |
| 10 | LLM budgets bound turns; no gateway on breach | **PARTIAL** | **P1** | `BudgetGuard` / `InterviewEngine` tested offline; **не** на `/turns`; defaults `None`; estimate ≈ `len(text)//4` only |
| 11 | `parallel_tool_calls: false` | **PASS** (assemble) | — | `responses_client.py:32` — unused in live `/turns` |
| 12 | Pack schema independent validation | **PARTIAL** | **P1** | Subset validator (`request_assembly.py:87–125`) — type/required/properties/additionalProperties; **no enum** etc. |
| 13 | Server-owned fields | **PASS** (library) | — | `strip_server_owned_fields` / assembly — not on live turn path |
| 14–17 | Dual-confirm / tokens ≤64 / Edit-Cancel | **PARTIAL** | **P0** wire | Library+tests PASS; production `/turns` не выдаёт interpretation/Send actions |
| 18–23 | Gateway outcomes / stash copy | **PARTIAL** | **P0** wire | Executor+tests PASS; not reached from live interview loop |
| 24 | Prompt cache telemetry | **PARTIAL** | **P2** Prometheus · **P1** double-instructions | `CacheTelemetry` exists; no dedicated Prom series. `interview.py:61–82` кладёт instructions и в stable prefix, и в `instructions=` |
| 25 | Startup/readiness fail-closed | **FAIL** | **P0** | Soft `/readyz` (см. §1). Silent memory fallback when DB adapter fails (`app.py:128–140`) |
| 26 | Unit / contract / restart / E2E | **PARTIAL** | **P0** façade E2E · **P1** restart/Send · **P2** multi-instance | Unit+contract green. Нет ASGI E2E без `"Received:"`. Live Postgres skipped |

---

## 3. Critical gaps **missing from v1 of this report** (validator-confirmed)

| Id | Issue | Pri | Evidence |
|----|-------|-----|----------|
| C1 | `/v1/channel/turns` не вызывает модель / `InterviewEngine` | **P0** | `channel.py:55–81`; Grep `InterviewEngine` в `app.py`/`channel.py` — только tests |
| C2 | Нет production OpenAI Responses client | **P0** | Только `ResponsesClient` Protocol + `RecordingResponsesClient` (`responses_client.py:41–70`) |
| C3 | Нет полного tool loop (`function_call` → validate → freeze → confirm → Send → `function_call_output`) | **P0** | `interview.py:93–138` — один call, только `output_text` |
| C4 | Tool shape Chat Completions, не Responses | **P0** | `tool_gen.py:238–252` |
| C5 | `/readyz` false ready | **P0** | `app.py:243–271`; REQ §18 |
| C6 | Postgres row mapping вероятно ломается без row factory | **P0** | `psycopg.connect` без `row_factory`; `_from_row` / `get` используют `row["…"]` (`registry.py:288–305`, `sessions.py:245–249`). Live test skipped (`test_postgres_adapter.py`) |
| C7 | Postgres `SessionStore` не в runtime path | **P0** | `app.state.session_store` vs `ConfirmationGuard._sessions` |
| C8 | Env contract drift vs REQ §17 | **P0** | REQ `DOGESTONIA_API_BASE_URL`; код `DOGESTONIA_GATEWAY_ORIGIN`; `.env.example` врёт про alias — в `Settings` alias **нет**. `AIBRIDGE_SESSION_TTL_SECONDS` / `AIBRIDGE_ACTION_TOKEN_TTL_SECONDS` в example, **нет** в `config.py` |
| C9 | Schema gates incomplete | **P1** | `request_assembly.py` subset |
| C10 | Budgets не защищают production `/turns` | **P1** | см. AC #10 |
| C11 | Instructions likely duplicated in request | **P1** | `interview.py:61–82` |
| C12 | Bounded JSON `500` handler | **P0** | нет global exception → channel envelope |

---

## 4. §22 Deliverables (short, revised)

| # | Deliverable | Verdict | Pri | Notes |
|---|-------------|---------|-----|-------|
| 1 | Python app + Dockerfile | **PARTIAL** | **P1** Dockerfile | App + Railpack OK for smoke. Dockerfile — воспроизводимость / node clone, не блокер первого infra smoke |
| 2–3 | OAS + contract tests | **PASS** | — | |
| 4–13 | Bundle/tool/session/confirm/gateway modules | **PARTIAL** | **P0** integrate | Modules exist; **not** one transactional runtime |
| 14 | Health + graceful shutdown | **PARTIAL** | **P1** shutdown | Health OK; shutdown = AIB-OPS-03 gap (один пункт) |
| 15 | Audit + metrics | **PASS** (surface) | — | Series wire partial historically; increments exist on some paths |
| 16 | `.env.example` | **PARTIAL** | **P0** | Names present; alias/TTL claims vs `Settings` drift (C8) |
| 17–21 | Runbooks / n8n ops docs | **PASS** | — | Workflow JSON export **not required** by REQ |

---

## 5. P0 package (do now) — validator-aligned

1. Coordinator: `/turns` → session repo → live Responses client → tool loop → confirm repo.  
2. Fix Responses tool JSON shape.  
3. PostgreSQL as sole production store for security/session state; **no** silent memory fallback.  
4. Fix Postgres row factory; mandatory live Postgres CI test.  
5. Strict `/readyz` (DB, OpenAI, bundle, gateway, required env).  
6. Align env names with REQ §17.  
7. One ASGI E2E (fake OpenAI + gateway transports) asserting non-stub interview/tool/confirm.  
8. Bounded `500` JSON envelope.

Defer (согласовано): multi-replica tests, cache Prom series, APM, distributed rate limiter, universal n8n JSON template — **P2** / post first node.  
До жителей (**P1**): history/tokens persistence beyond P0 package, restart recovery, graceful shutdown, full schema validation, rate limits + budget defaults, response-size limits, locale E2E.  
**Не P1:** token-hash Send replay UX (D1 accepted — optional only). SSOT доработок: [`../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md`](../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md).

---

## 6. Deploy note

- Liveness: `GET /healthz`. Readiness: не доверять `200 ready` до фикса C5.  
- Public smoke = Bearer/network only, пока C1–C3 не закрыты.

---

## 7. Related

- API doc: [`../runtime-docs/01-api.md`](../runtime-docs/01-api.md)  
- Validator disagreements: [`req-01-gap-validator-disagreements-2026-09-13.md`](./req-01-gap-validator-disagreements-2026-09-13.md)
