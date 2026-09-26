# DOGEstonia pilot: простой запуск Railway → PostgreSQL → aibridge → n8n → Telegram

**Цель:** сначала поднять и проверить всю инфраструктурную цепочку первой ноды в безопасном dry-run.  
**Режим:** `AIBRIDGE_DRY_RUN=true`; реальный `POST /story-drafts` запрещён.  
**Версия:** 0.1.0 · 2026-09-14

---

## 1. Что мы запускаем

```text
Житель в Telegram
        ↓
n8n: принимает сообщение и показывает кнопки
        ↓  private HTTP + Channel Bearer
doge-ai-bridge: ведёт диалог и принимает подтверждения
        ↓
OpenAI Responses API

doge-ai-bridge ↔ отдельный PostgreSQL

В dry-run gateway получает 0 запросов /story-drafts.
```

n8n — интерфейс и маршрутизация. Все инструкции, OpenAI key, gateway Bearer, validation и правила подтверждения принадлежат aibridge.

---

## 2. Важное ограничение текущего кода

Инфраструктуру можно поднять сейчас, но содержательный DOGEstonia-диалог требует закрыть непосредственный prerequisite из REQ-03:

> verified content bundle должен быть реально подключён к `InterviewEngine` и `ConfirmationGuard.validation_context`.

Текущий Dockerfile копирует `src/` и `migrations/`, но не копирует instructions/OAS/pack. Одних переменных окружения недостаточно, если указанных файлов нет внутри image.

Поэтому запуск делится на два результата:

1. **Infra smoke:** контейнер, база, Bearer, private network и HTTP работают.
2. **Meaningful dry-run:** AI получил реальные инструкции, pack и strict tool; для него сначала нужен production content wiring.

Не отключайте dry-run только потому, что infra smoke стал зелёным.

---

## 3. Не перепутать два OpenAPI

| Файл | Для чего |
|---|---|
| `docs/openapi/aibridge-channel-v1.openapi.yaml` | Контракт между n8n и aibridge: `/v1/channel/turns` и `/v1/channel/actions` |
| Canonical Story Intake OpenAPI | Контракт aibridge с gateway; должен содержать `postStoryDraftStash` → `POST /story-drafts` |

`DOGESTONIA_OPENAPI_PATH` должен указывать на **Story Intake OpenAPI**, а не на `aibridge-channel-v1.openapi.yaml`.

Channel OpenAPI уже находится в правильном месте:

```text
docs/openapi/aibridge-channel-v1.openapi.yaml
```

---

## 4. Что должно находиться в одном Railway environment

Для первой ноды удобно держать в одном Railway project/environment:

1. `n8n`;
2. `doge-ai-bridge`;
3. отдельный PostgreSQL для n8n;
4. отдельный PostgreSQL для aibridge;
5. gateway — может быть в том же или другом проекте, но aibridge использует его HTTPS URL.

Лучше не использовать базу n8n как базу aibridge. Отдельная база упрощает миграции, backup, удаление данных и перенос ноды.

---

## 5. Создать PostgreSQL для aibridge

### В Railway

1. Откройте нужный project и environment.
2. Нажмите `+ New`.
3. Выберите `Database` → `PostgreSQL`.
4. Назовите сервис понятно, например `aibridge-postgres`.
5. Не добавляйте Public Access/TCP Proxy: база нужна только внутри Railway.
6. Дождитесь статуса Active/Deployed.

Railway сам создаст в database service переменные:

- `DATABASE_URL`;
- `PGHOST`;
- `PGPORT`;
- `PGUSER`;
- `PGPASSWORD`;
- `PGDATABASE`.

В aibridge нужна только полная строка `DATABASE_URL`.

### Подключить базу к aibridge

Откройте:

```text
doge-ai-bridge service → Variables → New Variable
```

Добавьте:

```env
DATABASE_URL=${{aibridge-postgres.DATABASE_URL}}
```

Если сервис называется иначе, выберите его через Railway autocomplete. Не переписывайте пароль вручную.

Railway использует синтаксис `${{SERVICE_NAME.VARIABLE}}` для ссылки на переменную другого сервиса.

---

## 6. Инициализировать таблицы

В репозитории находятся versioned SQL migrations в папке `migrations/`.

Откройте:

```text
doge-ai-bridge service → Settings → Deploy → Pre-deploy Command
```

Укажите:

```bash
python -c "import os; from aibridge.migrate import apply_migrations; apply_migrations(os.environ['DATABASE_URL'])"
```

Рекомендуемый `Pre-deploy Timeout`: `300` секунд.

Что произойдёт:

- Railway сначала соберёт image;
- отдельный pre-deploy container подключится к private PostgreSQL;
- применит ещё не применённые миграции;
- при ошибке deployment остановится;
- после успеха запустится основной сервис.

Повторный deployment безопасен: уже применённые версии повторно не выполняются.

---

## 7. Build и Start command

В репозитории уже есть Dockerfile. Отдельный Build Command не нужен.

Нормальный вариант:

- Builder: Dockerfile;
- Build Command: оставить пустым;
- Start Command: оставить пустым, чтобы использовался Dockerfile `CMD`.

Если Railway требует Start Command вручную:

```bash
python -m uvicorn --app-dir src aibridge.app:app --host 0.0.0.0 --port ${PORT:-8080}
```

В Variables установите:

```env
PORT=8080
```

Если вы сознательно используете другой `PORT`, этот же номер потребуется в private URL из n8n.

---

## 8. Переменные aibridge для первого dry-run

Откройте `doge-ai-bridge → Variables → RAW Editor` и используйте список ниже. Значения в `<...>` замените своими.

```env
PORT=8080

DATABASE_URL=${{aibridge-postgres.DATABASE_URL}}
AIBRIDGE_ALLOW_MEMORY_STORES=false

OPENAI_API_KEY=<secret key из OpenAI Platform project>
OPENAI_MODEL=gpt-4.1-mini
OPENAI_STORE_RESPONSES=false

AIBRIDGE_CHANNEL_BEARER_TOKEN=<отдельный случайный secret для n8n → aibridge>
AIBRIDGE_CHANNEL_PREVIOUS_BEARER_TOKEN=

GATEWAY_BASE_URL=https://<публичный HTTPS-домен intake-сервиса ноды; complaints = doge-complaints-gateway>
GATEWAY_SERVICE_API_TOKEN=<Bearer, который gateway/intake выдаёт именно aibridge>
SPA_BASE_URL=https://<публичный HTTPS-домен SPA>

DOGESTONIA_OPERATION_ID=postStoryDraftStash
DOGESTONIA_ORIGIN_SOURCE=openai_responses_telegram

AIBRIDGE_DRY_RUN=true
AIBRIDGE_SCHEMA_VALIDATION_COMPLETE=false

AIBRIDGE_DEPLOYMENT_ID=uus-veerenni-pilot-v1
AIBRIDGE_SESSION_TTL_SECONDS=604800
AIBRIDGE_ACTION_TOKEN_TTL_SECONDS=900
AIBRIDGE_BUNDLE_GC_GRACE_SECONDS=86400

AIBRIDGE_MAX_REQUEST_BYTES=65536
AIBRIDGE_MAX_RESPONSE_BYTES=1048576
AIBRIDGE_HTTP_CONNECT_TIMEOUT_MS=5000
AIBRIDGE_HTTP_TOTAL_TIMEOUT_MS=30000
AIBRIDGE_GATEWAY_TIMEOUT_SECONDS=30
AIBRIDGE_OPENAI_TIMEOUT_MS=60000

AIBRIDGE_MAX_INPUT_TOKENS=100000
AIBRIDGE_MAX_OUTPUT_TOKENS=16384
AIBRIDGE_MAX_RESPONSES_CALLS_PER_TURN=8
AIBRIDGE_MAX_TOOL_CALLS_PER_TURN=16
AIBRIDGE_MAX_SESSION_TURNS=100

AIBRIDGE_PRINCIPAL_RATE_LIMIT=60
AIBRIDGE_GLOBAL_RATE_LIMIT=600
AIBRIDGE_LOG_LEVEL=INFO

AIBRIDGE_OPS_BEARER_TOKEN=<отдельный ops secret для административного удаления сессий>
```

### Content bundle variables

Эти значения нельзя угадывать. Их нужно заполнить после того, как build действительно положит bundle в image и production wiring подключит его к engine:

```env
DOGESTONIA_INSTRUCTIONS_DIR=<абсолютный путь внутри image к корневым instruction-файлам>
DOGESTONIA_INSTRUCTIONS_MANIFEST=<абсолютный путь внутри image к instructions.manifest.json>
DOGESTONIA_CONTENT_SOURCE_COMMIT=<полный commit SHA источника content bundle>
DOGESTONIA_OPENAPI_PATH=<путь внутри image к Story Intake OpenAPI, НЕ к channel OpenAPI>
DOGESTONIA_PAYLOAD_SCHEMA_PATH=<путь внутри image к payload.schema.json активного pack>
DOGESTONIA_TOOL_SCHEMA_PATH=<путь внутри image к сохранённой/проверяемой strict-tool schema, если wiring её использует>
DOGESTONIA_SCHEMA_ID=<точный schema_id активного pack>
DOGESTONIA_SCHEMA_VERSION=<точная версия активного pack>
```

Если IDE-агент выберет стандартный layout `/app/content/...`, используйте его реальные итоговые пути. Не создавайте воображаемые пути только ради зелёного `/ready` (`/readyz`).

### Какие secrets должны отличаться

Обязательно разные значения:

- `AIBRIDGE_CHANNEL_BEARER_TOKEN` — знает n8n и aibridge;
- `GATEWAY_SERVICE_API_TOKEN` — знают только aibridge и gateway;
- `OPENAI_API_KEY` — знает только aibridge;
- Telegram Bot token — знает только n8n.

Не копируйте один Bearer во все поля.

### Как создать Channel Bearer

На локальном компьютере можно выполнить:

```bash
openssl rand -hex 32
```

Получившуюся строку сохранить:

- в Railway как `AIBRIDGE_CHANNEL_BEARER_TOKEN` у aibridge;
- в n8n Header Auth credential как часть `Bearer ...`.

Сам token не вставлять в workflow JSON, screenshots, GitHub или документацию.

---

## 9. Public и private URL: что куда

| Связь | URL | Почему |
|---|---|---|
| n8n → aibridge | `http://doge-ai-bridge.railway.internal:8080` | Оба сервиса внутри одного Railway environment |
| aibridge → gateway | `https://<gateway-domain>` | Текущий executor требует HTTPS |
| Telegram user → SPA | `https://<spa-domain>` | Ссылка должна открываться на телефоне пользователя |
| Интернет → aibridge | Не нужен | aibridge можно не публиковать |
| Интернет → PostgreSQL | Не нужен | Public Access базе не включать |

Private hostname строится из точного Railway service name:

```text
SERVICE_NAME.railway.internal
```

Если aibridge service называется не `doge-ai-bridge`, замените имя. Порт должен совпадать с `PORT` самого aibridge.

---

## 10. Сначала проверить aibridge из n8n

Поскольку aibridge не публикуется наружу, удобнее проверить его временной HTTP Request node внутри n8n.

### Health

Создайте временный HTTP Request node:

- Method: `GET`;
- URL: `http://doge-ai-bridge.railway.internal:8080/health` (REQ9-primary; alias `/healthz` OK);
- Authentication: `None`.

Ожидается:

```json
{"status":"ok"}
```

Это доказывает только сеть и работающий процесс.

### Readiness

Поменяйте URL на:

```text
http://doge-ai-bridge.railway.internal:8080/ready
# alias: …/readyz
```

- `200 ready` — конфигурация прошла текущую readiness;
- `503 not_ready` — смотрите `reason` и Railway logs.

Помните: до выполнения REQ-04 текущий readiness ещё недостаточно строгий. Поэтому `200` не заменяет meaningful dry-run.

### Проверка защиты

POST на `/v1/channel/turns` без Authorization должен вернуть `401`. Это означает, что façade не открыт без Channel Bearer.

---

## 11. Создать credential для aibridge в n8n

В n8n:

1. Откройте `Credentials`.
2. Создайте credential типа `Header Auth`.
3. Назовите его, например `aibridge Channel Bearer`.
4. Header Name:

```text
Authorization
```

5. Header Value:

```text
Bearer <точное значение AIBRIDGE_CHANNEL_BEARER_TOKEN>
```

В n8n не добавлять:

- `OPENAI_API_KEY`;
- `GATEWAY_SERVICE_API_TOKEN`;
- gateway URL;
- прямой вызов `/story-drafts`.

Для пилота private URL можно прописать прямо в HTTP Request node. Параметризация через `$env` не обязательна, особенно если n8n запрещает доступ к env из editor UI.

---

## 12. Основная схема workflow n8n

Правильное общее название элементов, которые добавляются плюсиком в n8n: **nodes** — ноды workflow.

```text
Telegram Trigger
    ↓
Switch
    ├── message → HTTP Request: turns → Telegram: Send Message
    └── callback_query
            → Telegram: Answer Callback Query
            → HTTP Request: actions
            → Telegram: Send Message или Edit Message
```

Telegram Trigger должен принимать одновременно:

- `Message`;
- `Callback Query`.

Один Telegram bot может иметь только один активный Telegram Trigger webhook. Поэтому message и callback лучше принимать одним Trigger и разделять через Switch.

---

## 13. Настроить ветку обычного сообщения

После output `message` у Switch добавьте новую node `HTTP Request`.

### HTTP Request: turns

- Method: `POST`;
- URL:

```text
http://doge-ai-bridge.railway.internal:8080/v1/channel/turns
```

- Authentication: `Generic Credential Type` → `Header Auth` → `aibridge Channel Bearer`;
- Send Headers: credential добавит Authorization;
- Send Body: `ON`;
- Body Content Type: `JSON`.

Передать поля:

| Поле aibridge | Значение из Telegram Trigger |
|---|---|
| `channel` | постоянная строка `telegram` |
| `event_id` | `String(update_id)` |
| `principal.user_id` | `String(message.from.id)` |
| `principal.chat_id` | `String(message.chat.id)` |
| `message.message_id` | `String(message.message_id)` |
| `message.text` | `message.text` |
| `message.language_code` | `message.from.language_code`, если есть |

В режиме JSON Expression тело концептуально должно получиться таким:

```javascript
{{ ({
  channel: 'telegram',
  event_id: String($json.update_id),
  principal: {
    user_id: String($json.message.from.id),
    chat_id: String($json.message.chat.id)
  },
  message: {
    message_id: String($json.message.message_id),
    text: $json.message.text,
    language_code: $json.message.from.language_code || null
  }
}) }}
```

Если конкретное поле n8n не принимает целый объект expression, добавьте эти поля через визуальный JSON/body editor по таблице выше. Главное — итоговый JSON, а не способ ввода.

### После HTTP Request

Добавьте Telegram node `Send Message`:

- Chat ID:

```javascript
{{ $('Telegram Trigger').item.json.message.chat.id }}
```

- Text:

```javascript
{{ $json.reply_text }}
```

Если `actions` пустой, отправляется обычное сообщение. Если `actions` не пустой, добавляется inline keyboard.

---

## 14. Отобразить кнопки из `actions[]`

Aibridge возвращает:

```json
{
  "actions": [
    {"label":"Looks right","token":"opaque-token","style":"success"}
  ]
}
```

В Telegram отправляется:

- текст кнопки = `label`;
- `callback_data` = только `token`.

Концептуальное выражение для inline keyboard:

```javascript
{{ ({
  inline_keyboard: $json.actions.map(action => [
    {
      text: action.label,
      callback_data: action.token
    }
  ])
}) }}
```

Не помещать в `callback_data`:

- Bearer;
- session JSON;
- draft body;
- user/chat id;
- URL;
- название действия, придуманное n8n.

Нужен только opaque token, возвращённый aibridge.

---

## 15. Настроить ветку callback_query

### Шаг 1 — немедленно подтвердить нажатие Telegram

От output `callback_query` у Switch добавьте Telegram action `Answer Callback Query`.

Callback Query ID:

```javascript
{{ $json.callback_query.id }}
```

Текст можно оставить пустым или нейтральным. Этот шаг должен идти **до** обращения к aibridge, чтобы Telegram перестал показывать индикатор ожидания.

### Шаг 2 — HTTP Request: actions

После Answer Callback Query добавьте HTTP Request:

- Method: `POST`;
- URL:

```text
http://doge-ai-bridge.railway.internal:8080/v1/channel/actions
```

- Authentication: тот же `aibridge Channel Bearer`;
- Body Content Type: `JSON`.

Передать:

| Поле aibridge | Telegram source |
|---|---|
| `channel` | постоянная строка `telegram` |
| `event_id` | `String(update_id)` текущего Telegram update |
| `callback_query_id` | `String(callback_query.id)` |
| `principal.user_id` | `String(callback_query.from.id)` |
| `principal.chat_id` | `String(callback_query.message.chat.id)` |
| `action_token` | `callback_query.data` |

Концептуальное JSON Expression:

```javascript
{{ ({
  channel: 'telegram',
  event_id: String($('Telegram Trigger').item.json.update_id),
  callback_query_id: String($('Telegram Trigger').item.json.callback_query.id),
  principal: {
    user_id: String($('Telegram Trigger').item.json.callback_query.from.id),
    chat_id: String($('Telegram Trigger').item.json.callback_query.message.chat.id)
  },
  action_token: $('Telegram Trigger').item.json.callback_query.data
}) }}
```

Важно: при автоматическом retry HTTP Request тело не меняется. `event_id` остаётся тем же Telegram `update_id`; новый UUID создавать нельзя.

### Шаг 3 — показать ответ

После `/actions` добавьте `Send Message` или `Edit Message`:

- Chat ID:

```javascript
{{ $('Telegram Trigger').item.json.callback_query.message.chat.id }}
```

- Text:

```javascript
{{ $json.reply_text }}
```

- новые buttons — снова из `$json.actions`;
- при `outcome=stashed` можно добавить `continuation_url` как URL button;
- в dry-run ожидается `outcome=dry_run_ok`, реального `draft_id` не будет.

Для первого запуска проще использовать `Send Message`. Позднее можно заменить на `Edit Message`, не меняя API aibridge.

---

## 16. Порядок первого теста

### Тест A — процесс и private network

- [ ] `/health` из n8n возвращает 200 (alias `/healthz` OK).
- [ ] n8n обращается по `.railway.internal`, не по public aibridge domain.

### Тест B — Bearer

- [ ] `/v1/channel/turns` без credential возвращает 401.
- [ ] С Channel Bearer запрос проходит дальше.
- [ ] Gateway Bearer отсутствует в n8n.

### Тест C — база

- [ ] Pre-deploy migration завершилась успешно.
- [ ] `AIBRIDGE_ALLOW_MEMORY_STORES=false`.
- [ ] После restart повтор того же `event_id` не запускает второй Responses call.

### Тест D — Telegram message

- [ ] Отправить боту обычное текстовое сообщение.
- [ ] Telegram Trigger получил `update_id`, `from.id`, `chat.id`, `message_id`, `text`.
- [ ] Switch отправил update в ветку message.
- [ ] `/turns` вернул bounded JSON.
- [ ] Telegram показал `reply_text`.

### Тест E — buttons/callback

- [ ] n8n создал кнопки из `actions[]`.
- [ ] В `callback_data` находится только opaque token.
- [ ] Нажатие сразу прошло через Answer Callback Query.
- [ ] Затем n8n вызвал `/actions`.
- [ ] Telegram показал новый `reply_text`.

### Тест F — dry-run safety

- [ ] `AIBRIDGE_DRY_RUN=true`.
- [ ] `AIBRIDGE_SCHEMA_VALIDATION_COMPLETE=false`.
- [ ] Gateway logs показывают zero `POST /story-drafts`.
- [ ] n8n workflow вообще не содержит `/story-drafts`.

---

## 17. Как понимать частые ошибки

| Симптом | Вероятная причина | Что проверить |
|---|---|---|
| `ENOTFOUND ...railway.internal` | Сервисы в разных Railway environment или ошибочное service name | Одинаковый environment; точное имя сервиса |
| `Connection refused` | Неверный port | `PORT` aibridge и port в n8n URL должны совпадать |
| `401 Unauthorized` | Header Auth отсутствует или token различается | `Authorization: Bearer ...`; одинаковый Channel Bearer на обеих сторонах |
| `503 database_not_postgres` | Неверный `DATABASE_URL` или memory policy | Reference `${{aibridge-postgres.DATABASE_URL}}`; `ALLOW_MEMORY=false` |
| `503 migration...` | Миграции не применены | Railway Pre-deploy logs и command |
| `503 dry_run_required` | Попытка включить real gateway раньше schema gate | Вернуть `AIBRIDGE_DRY_RUN=true` |
| `content_bundle_not_ready` | Файлы отсутствуют в image, неверны paths/hash/manifest | Сначала исправить content packaging/wiring |
| `schemas not configured` | `ValidationContext` не подключён в production | Закрыть immediate REQ-03 blocker №1 |
| Telegram бесконечно крутит на кнопке | Нет/поздно вызван Answer Callback Query | Поставить его первым в callback branch |
| Кнопка нажимается, но `/actions` даёт 403 | Другой Telegram user/chat | Проверить callback principal mapping |
| Повтор сообщения повторно вызывает AI | n8n создаёт новый `event_id` | Всегда использовать исходный `update_id` |

---

## 18. Что считать успешным запуском сейчас

### Infra chain запущена

Можно считать инфраструктурный запуск успешным, если:

- PostgreSQL private и мигрирован;
- aibridge запущен на `$PORT`;
- n8n видит `/health` по private URL (alias `/healthz` OK);
- façade без Bearer даёт 401;
- façade с Bearer принимает корректный JSON;
- Telegram message и callback проходят через нужные n8n branches;
- dry-run не вызывает `/story-drafts`.

### Meaningful DOGEstonia dry-run запущен

Дополнительно требуется:

- content files присутствуют внутри image;
- production engine получил инструкции и strict tool;
- validation context собран из active pack/wire schemas;
- модель возвращает не технический stub, а DOGEstonia interview reply.

### Что пока не означает успех

- один зелёный Railway deployment;
- один `/health=200` (alias `/healthz`);
- текущий `/ready=200` (alias `/readyz`) до REQ-04;
- прохождение тестов, где engine/validation вручную подставлены helper-кодом.

---

## 19. После первого запуска

Следующая короткая последовательность:

1. Зафиксировать redacted screenshots/logs прохождения message и callback branches.
2. Закрыть REQ-04.
3. Подключить полноценную JSON Schema validation.
4. Проверить async action/follow-up path.
5. Пройти live dry-run повторно.
6. Только затем решить, можно ли включить `AIBRIDGE_DRY_RUN=false`.
7. Провести настоящий stash и открыть HTTPS SPA continuation на телефоне.

---

## 20. Источники

- Репозиторий: <https://github.com/DOGE-Complaints/doge-ai-bridge/tree/dev>
- Runtime env: <https://github.com/DOGE-Complaints/doge-ai-bridge/blob/dev/.env.example>
- Dockerfile: <https://github.com/DOGE-Complaints/doge-ai-bridge/blob/dev/Dockerfile>
- Channel OpenAPI: <https://github.com/DOGE-Complaints/doge-ai-bridge/blob/dev/docs/openapi/aibridge-channel-v1.openapi.yaml>
- n8n mapping: <https://github.com/DOGE-Complaints/doge-ai-bridge/blob/dev/docs/ops/n8n-channel-workflow/README.md>
- Railway variables: <https://docs.railway.com/variables>
- Railway private networking: <https://docs.railway.com/networking/private-networking>
- Railway PostgreSQL: <https://docs.railway.com/databases/postgresql>
- Railway pre-deploy command: <https://docs.railway.com/deployments/pre-deploy-command>

