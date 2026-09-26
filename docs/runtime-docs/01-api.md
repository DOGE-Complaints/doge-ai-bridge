# 01. HTTP API

> Актуализировано 2026-09-13 по коду `src/aibridge/`. Machine SSOT канала: [`../openapi/aibridge-channel-v1.openapi.yaml`](../openapi/aibridge-channel-v1.openapi.yaml). Wire Story Intake (не этот фасад): [`../openapi/story-intake-actions.openapi.yaml`](../openapi/story-intake-actions.openapi.yaml).  
> Сверка с REQ-01: [`../analysis/req-01-runtime-code-gap-2026-09-13.md`](../analysis/req-01-runtime-code-gap-2026-09-13.md).

## О чём этот документ

`doge-ai-bridge` — server-to-server channel façade для n8n (Telegram UI). Здесь — **фактические** HTTP-маршруты ASGI-приложения: кто пускается, какие тела/статусы, где в коде.

Источники истины:

- [`app.py`](../../src/aibridge/app.py) — маршруты, middleware, `/healthz`/`/readyz`/`/metrics`
- [`schemas.py`](../../src/aibridge/schemas.py) — Pydantic-модели канала
- [`auth.py`](../../src/aibridge/auth.py) — Channel Bearer
- [`channel.py`](../../src/aibridge/channel.py) / [`confirm.py`](../../src/aibridge/confirm.py) — turns/actions
- [`metrics.py`](../../src/aibridge/metrics.py) — Prometheus text

FastAPI interactive docs **отключены** (`docs_url=None`, `redoc_url=None`, `openapi_url=None`) — [`app.py:176–181`](../../src/aibridge/app.py).

Gateway `POST /story-drafts` **не** является HTTP-маршрутом aibridge; executor ходит на gateway по wire OAS ([`gateway.py`](../../src/aibridge/gateway.py)).

---

## Маршруты

| Метод | Путь | Auth | Что сейчас | Где в коде |
|-------|------|------|------------|------------|
| GET | `/healthz` | нет | `{"status":"ok"}` — liveness | [`app.py:239–241`](../../src/aibridge/app.py) |
| GET | `/readyz` | нет | 200 `{"status":"ready"}` или 503 `{"status":"not_ready","reason":…}` | [`app.py:243–271`](../../src/aibridge/app.py) |
| GET | `/metrics` | нет (ожидается private network) | Prometheus text (`text/plain; version=0.0.4`) | [`app.py:273–280`](../../src/aibridge/app.py), [`metrics.py`](../../src/aibridge/metrics.py) |
| POST | `/v1/channel/turns` | Channel Bearer | 200 success envelope (сейчас stub `Received: …` — **не** Responses/InterviewEngine; см. gap C1) или 4xx | [`app.py:282–295`](../../src/aibridge/app.py), [`channel.py:55–81`](../../src/aibridge/channel.py) |
| POST | `/v1/channel/actions` | Channel Bearer | 200 success envelope или 4xx error body | [`app.py:297–328`](../../src/aibridge/app.py) |

Префикс, на котором требуется Bearer: `CHANNEL_PATH_PREFIX = "/v1/channel/"` — [`app.py:29`](../../src/aibridge/app.py), [`app.py:214–224`](../../src/aibridge/app.py).

---

## Успешный ответ канала (envelope)

Оба `POST /v1/channel/*` при успехе отдают JSON без обёртки `data` — поля `ChannelSuccessResponse` ([`schemas.py:71–83`](../../src/aibridge/schemas.py)):

| Поле | Тип | Примечание |
|------|-----|------------|
| `request_id` | string | id запроса |
| `session_id` | string | opaque session reference (не credential) |
| `state` | string | FSM / session state label |
| `reply_text` | string | текст для Telegram |
| `actions` | array | `{label, token, style}`; `token` ≤64; `style` ∈ `primary\|success\|danger\|default` |
| `outcome` | string \| null | bounded outcome (напр. после Send) |
| `draft_id` | string \| null | только при успешном stash-пути |
| `continuation_url` | string \| null | только вместе с успешным stash-путём |

**Нет поля `callback_ack_text`.** n8n должен сам сразу вызвать Telegram `answerCallbackQuery` с нейтральным/пустым текстом — см. [01-channel-facade §3](../architecture/runtime/01-channel-facade.md) и [n8n ops README](../ops/n8n-channel-workflow/README.md).

---

## Ошибка канала

Не-2xx для channel API используют `ChannelErrorBody` ([`schemas.py:86–98`](../../src/aibridge/schemas.py)):

```json
{
  "request_id": "…",
  "error": {
    "code": "bounded_machine_code",
    "message": "…",
    "retryable": false
  }
}
```

Сборка через `error_body()` — [`app.py:35–45`](../../src/aibridge/app.py).

### HTTP-статусы, которые код реально отдаёт на фасаде

| HTTP | Когда (факт кода) |
|-----:|-------------------|
| 200 | Успешный turn/action или dedupe replay |
| 400 | Malformed JSON / unknown field (`extra_forbid`) / bad Content-Length — [`app.py:74–86`](../../src/aibridge/app.py), [`89–119`](../../src/aibridge/app.py) |
| 401 | Нет/невалидный Channel Bearer — [`app.py:216–223`](../../src/aibridge/app.py) |
| 403 | Principal не владеет токеном — `confirm.py` → `channel_actions` |
| 404 | Токен/сессия не найдены |
| 409 | Expired/consumed/invalidated / illegal transition / `unknown_outcome` block |
| 413 | Body > `AIBRIDGE_MAX_REQUEST_BYTES` — middleware + handlers |
| 422 | Семантически невалидный channel input |
| 503 | `/readyz` not ready |

**429** в OAS/REQ есть; как **ответ канала** rate-limit в `app.py` не найден (429 используется при маппинге ответа *gateway* в `gateway.py`).

---

## Request bodies

Модели: `ChannelTurnRequest` / `ChannelActionRequest` — [`schemas.py:44–60`](../../src/aibridge/schemas.py); `extra="forbid"`; Telegram IDs — decimal strings.

**Turn** (`POST /v1/channel/turns`):

- `channel`: только `"telegram"`
- `event_id`, `principal.user_id`, `principal.chat_id`, `message.message_id`, `message.text` (non-empty)
- `message.language_code` optional

**Action** (`POST /v1/channel/actions`):

- `channel`, `event_id`, `callback_query_id`, `principal`, `action_token` (1…64 chars)

Дубликат `(channel, event_id)` возвращает сохранённый ответ без повторного side-effect — [`dedupe.py`](../../src/aibridge/dedupe.py) (in-process store).

---

## Аутентификация

- Заголовок: `Authorization: Bearer <token>`
- Accepted tokens: `AIBRIDGE_CHANNEL_BEARER_TOKEN` (+ optional previous при ротации) — `Settings.accepted_channel_tokens()`
- Сравнение: constant-time — [`auth.py:11–26`](../../src/aibridge/auth.py)
- Gateway Bearer (`GATEWAY_SERVICE_API_TOKEN`) **не** принимается на канале; если channel == gateway → `/readyz` reason `channel_gateway_bearer_equal`

`/healthz`, `/readyz`, `/metrics` **не** требуют Channel Bearer.

---

## `/readyz` reasons

При 503 тело вида `{"status":"not_ready","reason":"<code>"}` ([`app.py:243–270`](../../src/aibridge/app.py)):

| `reason` | Условие |
|----------|---------|
| `channel_auth_missing` | channel Bearer не сконфигурирован |
| `channel_gateway_bearer_equal` | channel token равен gateway token |
| `content_bundle_not_ready` / `dep.error` | content env задан, но bundle не ready |
| `database_adapter_unavailable:…` | ошибка открытия registry при init (через `DeploymentBundleState.error`) |

---

## `/metrics`

- Media type: `text/plain; version=0.0.4; charset=utf-8`
- Счётчики ([`metrics.py:61–91`](../../src/aibridge/metrics.py)):  
  `aibridge_channel_turns_total`, `aibridge_channel_actions_total`, `aibridge_channel_http_errors_total`, `aibridge_gateway_posts_total`, `aibridge_openai_calls_total`, `aibridge_budget_stops_total{reason=…}`
- Budget reason labels allowlisted (no free-form narrative) — [`metrics.py:11–19`](../../src/aibridge/metrics.py)
- Ошибки канала (≥400) инкрементятся middleware — [`app.py:226–237`](../../src/aibridge/app.py)

---

## Limits и CORS

- `BodySizeLimitMiddleware` + повторная проверка `len(raw)` на turns/actions — лимит `AIBRIDGE_MAX_REQUEST_BYTES` ([`app.py:207–208`](../../src/aibridge/app.py), [`284–290`](../../src/aibridge/app.py))
- CORS middleware **не** подключён (server-to-server) — факт `create_app` middleware list

---

## Bind / process

- Production start (Railway Railpack): `python -m uvicorn --app-dir src aibridge.app:app --host 0.0.0.0 --port ${PORT:-8000}` — [`railpack.json`](../../railpack.json)
- Локально также: `python -m aibridge` — [`__main__.py`](../../src/aibridge/__main__.py)
- Модуль ASGI: `aibridge.app:app` (`app = create_app()` в конце [`app.py:356`](../../src/aibridge/app.py))

---

## n8n (кратко)

Ожидаемый порядок без форка платформы — [01-channel-facade](../architecture/runtime/01-channel-facade.md) §3 / [ops README](../ops/n8n-channel-workflow/README.md):

1. Message → `POST /v1/channel/turns` → Send Message (+ inline `actions[].token` в `callback_data`)
2. Callback → immediate `answerCallbackQuery` → `POST /v1/channel/actions` → Send/Edit
