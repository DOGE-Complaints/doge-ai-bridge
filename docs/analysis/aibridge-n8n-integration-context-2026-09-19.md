# aibridge — состояние для диалога настройки n8n

**Зона:** `doge-ai-bridge/docs/analysis/`  
**As-of:** 2026-09-19  
**Назначение:** контекст для оператора / ассистента, который **сейчас** собирает workflow n8n ↔ aibridge.  
**Method:** analysis.mdc — разделяем **operator-stated** (факт оператора) и **repo-verified** (есть в docs/коде). Без выдуманных URL, токенов и PASS live Telegram.

---

## 1. Текущее состояние (кратко)

| Слой | Статус | Источник |
|------|--------|----------|
| Деплой aibridge | Успешен | **operator-stated** |
| Связь n8n ↔ aibridge в **private** space | Доступна | **operator-stated** |
| PostgreSQL создана, подключена, миграции накатаны | Да | **operator-stated** |
| Контракт канала (OpenAPI) | `aibridge-channel-v1` **1.0.0** | repo: `docs/openapi/aibridge-channel-v1.openapi.yaml` |
| Роль n8n | Thin adapter: Telegram ↔ HTTP façade | repo: ops README + pilot runbook |
| Роль aibridge | Диалог, FSM, OpenAI, gateway (не в n8n) | repo: REQ / architecture |
| Локальный QA-сьют (стенд) | **263 passed / 0 skipped** (с disposable PG, 2026-09-18) | repo: `docs/qa/inbound-outbound/pytest-report-20260918-post36-40.md` |
| Live Gate-5 / export workflow JSON в Git | Ещё **не** закрыты артефактами | repo: TRACEABILITY deferred; export path named, body absent |

**Вывод для диалога:** infra для сборки n8n **готова** (деплой + private + PG). Дальше — корректный **mapping и порядок узлов** по контракту, не «бизнес-логика в n8n».

---

## 2. Архитектура (что куда ходит)

```text
Telegram (житель / тестовый бот)
        ↓
n8n  —  UI: trigger, ack callback, кнопки Send/Edit
        ↓  private HTTP + Channel Bearer  (НЕ gateway Bearer)
aibridge  —  /v1/channel/turns | /v1/channel/actions
        ↓
OpenAI Responses (+ Postgres session/dedupe/tokens)
        ↓  (только из aibridge; в dry-run — 0 к gateway)
gateway POST /story-drafts   ← n8n СЮДА НЕ ХОДИТ
```

**Hard rules (repo):**

- Из n8n **никогда** не вызывать gateway `/story-drafts`.
- В workflow **нет** gateway URL / gateway Bearer / OpenAI key.
- Channel Bearer (`AIBRIDGE_CHANNEL_BEARER_TOKEN`) ≠ gateway Bearer (`DOGESTONIA_API_BEARER_TOKEN`).
- Пока пилот: предпочитать `AIBRIDGE_DRY_RUN=true` — зелёный private HTTP ≠ «можно выключать dry-run».

---

## 3. Контракт, который n8n обязан соблюдать

**SSOT:** [`docs/openapi/aibridge-channel-v1.openapi.yaml`](../openapi/aibridge-channel-v1.openapi.yaml)  
**Ops mapping:** [`docs/ops/n8n-channel-workflow/README.md`](../ops/n8n-channel-workflow/README.md)  
**Pilot steps:** [`docs/runbooks/AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md`](../runbooks/AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md) — private URL pattern вида `http://doge-ai-bridge.railway.internal:8080` (hostname/port сверить с вашим сервисом; не копировать вслепую).

### Endpoints

| Method | Path | Когда |
|--------|------|--------|
| `POST` | `/v1/channel/turns` | обычное `message` |
| `POST` | `/v1/channel/actions` | после `callback_query` (и **после** `answerCallbackQuery`) |
| `GET` | `/healthz` | процесс жив (без Bearer) |
| `GET` | `/readyz` | готовность конфига/зависимостей (без Bearer; может быть 503 + `reason`) |

Auth на channel paths: `Authorization: Bearer <AIBRIDGE_CHANNEL_BEARER_TOKEN>`.

### Порядок callback (обязательный)

1. Telegram `answerCallbackQuery` — нейтрально / пусто, **сразу** (не ждать aibridge).  
2. `POST /v1/channel/actions` с opaque `action_token` + principal.  
3. `Send Message` / `Edit Message` из `reply_text` / `actions`.

Поля `callback_ack_text` в channel OAS **нет** — не изобретать.

### Mapping cheat-sheet

**turns**

| Поле façade | Источник Telegram |
|-------------|-------------------|
| `channel` | константа `telegram` |
| `event_id` | `String(update.update_id)` — **не** новый UUID |
| `principal.user_id` / `chat_id` | from.id / chat.id (decimal string) |
| `message.message_id` / `text` | из message |
| `message.language_code` | optional |

**actions**

| Поле | Источник |
|------|----------|
| `event_id` | тот же `update_id` апдейта (не `callback_query.id`) |
| `callback_query_id` | `callback_query.id` |
| `action_token` | `callback_query.data` (как есть) |
| `principal.*` | from / message.chat |

**Retry:** при повторе HTTP на тот же Telegram update **не** менять `event_id` — иначе сломается dedupe aibridge.

**Ответ → Telegram:** `reply_text`; кнопки = `actions[].label` + `callback_data` = `token` only (≤64 bytes). `continuation_url` / draft — только при `outcome=stashed`; жителю не писать «опубликовано».

---

## 4. Credentials в n8n (имена, не значения)

| Credential | Содержит |
|------------|----------|
| Telegram Bot | bot token |
| aibridge Channel Header Auth | значение Channel Bearer |

В Git не класть. Не путать с gateway Bearer.

---

## 5. Что уже доказано локальным QA (не путать с live)

| Доказано | Не доказано этим |
|----------|------------------|
| Channel auth, schema, FSM, dedupe, OAI/GW doubles, UC на disposable PG | Живой Telegram → n8n → private aibridge (Gate-5) |
| N8N mapping как **fixture/adapter-contract** в pytest | Реальный export workflow в `exports/*.json` |
| Honesty: defer N8N-WF-001 / Gate-5 / CHAR-008 пока нет артефактов | «Production Story» / выключенный dry-run |

После настройки workflow в n8n следующий честный шаг — **smoke** из ops README §5 и при готовности checklist Gate-5 / export pin (см. STORY-36/37/39), а не объявление PASS по одному 200 от `/healthz`.

---

## 6. Минимальный smoke после узлов (оператор)

- [ ] Workflow active; нужный Bot  
- [ ] Private base URL aibridge + Channel Bearer на HTTP Request  
- [ ] Message → `/turns` → 200 envelope  
- [ ] Callback → immediate `answerCallbackQuery` → `/actions` → Send/Edit  
- [ ] Без Authorization → **401**  
- [ ] Нет нод на `/story-drafts`  
- [ ] (Опционально) `GET /readyz` — если не 200, читать `reason`, не гадать  

---

## 7. SSOT ссылки (открывать в диалоге)

| Тема | Путь |
|------|------|
| Channel OAS | `doge-ai-bridge/docs/openapi/aibridge-channel-v1.openapi.yaml` |
| n8n ops contract | `doge-ai-bridge/docs/ops/n8n-channel-workflow/README.md` |
| Pilot Railway↔n8n↔TG | `doge-ai-bridge/docs/runbooks/AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md` |
| Local/Railway web | `doge-ai-bridge/docs/runbooks/aibridge-web-service-local-railway.md` |
| QA pytest + квалификация | `doge-ai-bridge/docs/qa/inbound-outbound/` |
| Gate-5 checklist | `doge-ai-bridge/docs/ops/n8n-channel-workflow/r3-p1-09-live-gate-checklist.md` |

---

## 8. Фраза-якорь для старта диалога

> aibridge задеплоен; n8n видит его по private network; Postgres подключена, миграции применены (**operator-stated**). Собираем thin Telegram adapter по channel OAS v1: только `/turns` и `/actions` + Channel Bearer; callback ack до `/actions`; без gateway из n8n; `event_id` = `update_id`. Live Gate-5 / export pin — отдельным артефактом после smoke, не смешивать с зелёным локальным pytest.
