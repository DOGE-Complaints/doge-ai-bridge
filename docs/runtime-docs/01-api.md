# 01. HTTP API

> Актуализировано 2026-10-15 по коду `src/aibridge/` (channel + sense-brief worker).  
> Machine SSOT канала: [`../openapi/aibridge-channel-v1.openapi.yaml`](../openapi/aibridge-channel-v1.openapi.yaml).  
> Machine SSOT worker accept: [`../openapi/aibridge-worker-sense-brief-v1.openapi.yaml`](../openapi/aibridge-worker-sense-brief-v1.openapi.yaml).  
> Wire Story Intake (не этот фасад): [`../openapi/story-intake-actions.openapi.yaml`](../openapi/story-intake-actions.openapi.yaml).  
> REQ-09 validation: [`../analysis/zeya888.req-09-stories-46-50-code-validation-2026-10-15.md`](../analysis/zeya888.req-09-stories-46-50-code-validation-2026-10-15.md).

## О чём этот документ

`doge-ai-bridge` — server-to-server ASGI: (1) channel façade для n8n/Telegram; (2) sense-brief worker accept для gateway (REQ-09). Здесь — **фактические** HTTP-маршруты: кто пускается, какие тела/статусы, где в коде.

Источники истины:

- [`app.py`](../../src/aibridge/app.py) — маршруты, middleware, `/healthz`/`/readyz`/`/metrics`, worker accept
- [`schemas.py`](../../src/aibridge/schemas.py) — Pydantic-модели канала
- [`auth.py`](../../src/aibridge/auth.py) — Channel Bearer + worker S2S
- [`worker_accept.py`](../../src/aibridge/worker_accept.py) — worker path/idempotency
- [`channel.py`](../../src/aibridge/channel.py) / [`confirm.py`](../../src/aibridge/confirm.py) — turns/actions
- [`metrics.py`](../../src/aibridge/metrics.py) — Prometheus text

FastAPI interactive docs **отключены** (`docs_url=None`, `redoc_url=None`, `openapi_url=None`).

Gateway Story Intake stash и sense-brief **bind** — **не** HTTP-маршруты aibridge; clients в [`gateway.py`](../../src/aibridge/gateway.py) / [`sense_bind/client.py`](../../src/aibridge/sense_bind/client.py).

---

## Маршруты

| Метод | Путь | Auth | Что сейчас | Где в коде |
|-------|------|------|------------|------------|
| GET | `/healthz` · `/health` | нет | `{"status":"ok"}` — liveness | [`app.py`](../../src/aibridge/app.py) health handlers |
| GET | `/readyz` · `/ready` | нет | 200 ready / 503 not_ready (+ worker fail-closed reasons when enabled) | readiness + worker slot checks |
| GET | `/metrics` | нет (private network) | Prometheus text | metrics handlers |
| POST | `/v1/channel/turns` | Channel Bearer | channel turn envelope | `CHANNEL_PATH_PREFIX` · channel turns |
| POST | `/v1/channel/actions` | Channel Bearer | channel action envelope | channel actions |
| POST | `/v1/worker/sense-brief/accept` | Worker S2S Bearer | sense brief + poster + outbound bind | [`app.py:684–847`](../../src/aibridge/app.py), [`worker_accept.py`](../../src/aibridge/worker_accept.py) |

Префиксы auth:

- Channel: `CHANNEL_PATH_PREFIX = "/v1/channel/"` — [`app.py:57`](../../src/aibridge/app.py)
- Worker: `WORKER_PATH_PREFIX = "/v1/worker/"` — [`worker_accept.py:21`](../../src/aibridge/worker_accept.py); middleware [`app.py:566–626`](../../src/aibridge/app.py)

---

## Sense-brief worker (`POST /v1/worker/sense-brief/accept`)

OpenAPI: [`aibridge-worker-sense-brief-v1.openapi.yaml`](../openapi/aibridge-worker-sense-brief-v1.openapi.yaml). Arch: [`../architecture/sense-brief-poster-worker/00-overview.md`](../architecture/sense-brief-poster-worker/00-overview.md). Gateway handoff: [`../analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md`](../analysis/handoff-gateway-req13-sense-brief-worker-2026-10-15.md).

| Env | Role |
|-----|------|
| `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED` | Master switch (default false) |
| `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` | Accept auth (≠ channel Bearer) |
| `AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER` | `mock` \| `openai` (default `mock`) |
| `AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER` | `mock` \| `openai` (default `mock`; live image deferred) |
| `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` | text-brief model nest (when text=`openai`) |
| `AIBRIDGE_WORKER_IMAGE_POSTER_MODEL` | image-poster model nest (when image=`openai`) |
| `AIBRIDGE_ALLOW_MOCK_PROVIDERS` | Allow worker `mock` at readyz/accept (AC-10-09) |
| `AIBRIDGE_WORKER_STORAGE_UPLOAD_CREDENTIAL` | aibridge-owned upload cred |
| `GATEWAY_BASE_URL` + `GATEWAY_SERVICE_API_TOKEN` | Outbound bind client |

Provider list + mock-first ops: [`02-ai-provider-selection.md`](./02-ai-provider-selection.md).

**Request JSON:** `issue_id`, `generation_version` (required); `corpus` optional.  
**Idempotency:** same `(issue_id, generation_version)` → 200 with `idempotent: true` (in-process store).  
**Success path:** brief L2 → poster HTTPS URL → bind success to gateway → response may include `brief`, `poster_url`, `pipeline=bind_ready`.  
**Failure:** error envelope `error.code` = reason class; worker also attempts fail-bind to gateway (no fake brief).

Outbound (not served by aibridge): `POST {GATEWAY_BASE_URL}/v1/issue-sense-brief/bind` with gateway service Bearer.

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
