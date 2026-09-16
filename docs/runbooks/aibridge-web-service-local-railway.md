# aibridge: запуск только веб-сервиса (локально и Railway)

**Цель:** поднять HTTP-процесс `doge-ai-bridge` и проверить liveness.  
**Не входит:** n8n, Telegram, полный pilot — см. [AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md](./AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md).  
**Шаблон env:** [`.env.example`](../../.env.example) · **код настроек:** `src/aibridge/config.py`

---

## Что запускается

```text
uvicorn → aibridge.app:app
  GET /healthz   — процесс жив (без секретов)
  GET /readyz    — готовность конфига/зависимостей (может быть 503)
```

Старт:

| Где | Команда |
|-----|---------|
| Локально | `PORT=8080 python -m aibridge` (`src/aibridge/__main__.py`) |
| Dockerfile `CMD` | `python -m uvicorn --app-dir src aibridge.app:app --host 0.0.0.0 --port ${PORT:-8080}` |
| Railpack | то же в `railpack.json` (`${PORT:-8000}`) |

При импорте приложения с PostgreSQL `DATABASE_URL` миграции применяются из `create_app()` (`src/aibridge/app.py`). Отдельный pre-deploy на Railway всё равно полезен (fail до старта сервиса).

---

## 1. Локально

### 1.1 Установка

```bash
cd doge-ai-bridge
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # заполнить секреты; не коммитить
```

Минимум для старта процесса (не обязательно зелёный `/readyz`):

```env
PORT=8080
AIBRIDGE_CHANNEL_BEARER_TOKEN=dev-channel-token
DOGESTONIA_API_BEARER_TOKEN=dev-gateway-token-different
```

Для Postgres (предпочтительно):

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/aibridge
AIBRIDGE_ALLOW_MEMORY_STORES=false
```

Только локальный throwaway без Postgres (не для residents / не для pilot):

```env
AIBRIDGE_ALLOW_MEMORY_STORES=true
# DATABASE_URL можно не задавать / не postgres
```

Подробности имён — в `.env.example` и `config.py`.

### 1.1b REQ-05 Phase A content pins

Для полного flat dump + OAS в image (STORY-21 / ADR-3). Имена без новых alias — как в `.env.example` §8 и TECH §9.

**Local** (`cwd` = `doge-ai-bridge`):

```env
DOGESTONIA_INSTRUCTIONS_DIR=src/instructions
DOGESTONIA_INSTRUCTIONS_MANIFEST=src/instructions/instructions.manifest.json
DOGESTONIA_CONTENT_SOURCE_COMMIT=<pin SHA or label>
DOGESTONIA_OPENAPI_PATH=docs/openapi/story-intake-actions.openapi.yaml
DOGESTONIA_PAYLOAD_SCHEMA_PATH=src/instructions/schema-packs.uus_veerenni_civic.v3.payload.schema.json
DOGESTONIA_SCHEMA_ID=uus_veerenni_civic
DOGESTONIA_SCHEMA_VERSION=v3
# DOGESTONIA_TOOL_SCHEMA_PATH may stay empty
```

**Image** (`WORKDIR /app`; Dockerfile copies `src/`, `migrations/`, `docs/openapi/`):

```env
DOGESTONIA_INSTRUCTIONS_DIR=/app/src/instructions
DOGESTONIA_INSTRUCTIONS_MANIFEST=/app/src/instructions/instructions.manifest.json
DOGESTONIA_CONTENT_SOURCE_COMMIT=<pin SHA or label>
DOGESTONIA_OPENAPI_PATH=/app/docs/openapi/story-intake-actions.openapi.yaml
DOGESTONIA_PAYLOAD_SCHEMA_PATH=/app/src/instructions/schema-packs.uus_veerenni_civic.v3.payload.schema.json
DOGESTONIA_SCHEMA_ID=uus_veerenni_civic
DOGESTONIA_SCHEMA_VERSION=v3
```

`DOGESTONIA_OPENAPI_PATH` = **Story Intake** wire only (`story-intake-actions.openapi.yaml`), не channel façade. Channel YAML едет в image вместе с `docs/openapi/`, но **не** попадает в instruction `files[]`.

### 1.2 Миграции (Postgres)

Явно (опционально; тот же код, что при старте app):

```bash
PYTHONPATH=src python -c "import os; from aibridge.migrate import apply_migrations; apply_migrations(os.environ['DATABASE_URL'])"
```

`DATABASE_URL` должен быть в окружении (или экспортирован из `.env`).

### 1.3 Старт

```bash
# из doge-ai-bridge, с активированным .venv
# dotenv подхватывается Settings (pydantic-settings), если есть .env
PORT=8080 python -m aibridge
```

Эквивалент:

```bash
PYTHONPATH=src python -m uvicorn --app-dir src aibridge.app:app --host 0.0.0.0 --port 8080
```

### 1.4 Smoke

```bash
curl -sS http://127.0.0.1:8080/healthz
# ожидаемо: {"status":"ok"}

curl -sS http://127.0.0.1:8080/readyz
# 200 {"status":"ready"} или 503 {"status":"not_ready","reason":"..."}
```

`/healthz` = процесс слушает. `/readyz` = полный checklist (Bearer’ы, dry-run, content paths, DB, OpenAI presence и т.д.) — см. `src/aibridge/readiness.py`.

### 1.5 Частые локальные сбои

| Симптом | Что проверить |
|---------|----------------|
| Процесс падает при импорте / старте | `DATABASE_URL` недоступен с машины (DNS/сеть). Для локальной разработки к Railway Postgres нужен **публичный** proxy URL; private `*.railway.internal` с ноутбука не резолвится. |
| `/readyz` 503 | Смотреть `reason` в JSON; добить env по `.env.example` / pilot §8. |
| IDE: `pydantic_settings` unresolved | Interpreter = `doge-ai-bridge/.venv`, не другой venv репо. |

---

## 2. Railway (только aibridge + Postgres)

Без n8n/Telegram достаточно двух сервисов в одном environment: **PostgreSQL для aibridge** + **doge-ai-bridge**.

### 2.1 Postgres

1. `+ New` → `Database` → `PostgreSQL` (например `aibridge-postgres`).
2. Public Access/TCP Proxy для продакшена не обязателен (сервис ходит по private network).
3. В сервисе aibridge:

```env
DATABASE_URL=${{aibridge-postgres.DATABASE_URL}}
AIBRIDGE_ALLOW_MEMORY_STORES=false
```

Имя сервиса подставьте своё через autocomplete Railway.

### 2.2 Build / Start

**Рекомендуемый путь — Dockerfile** в корне `doge-ai-bridge`:

- Builder: Dockerfile  
- Build Command: пусто  
- Start Command: пусто → используется `CMD` из Dockerfile  

Если нужен ручной Start:

```bash
python -m uvicorn --app-dir src aibridge.app:app --host 0.0.0.0 --port ${PORT:-8080}
```

Альтернатива без Dockerfile: Railpack + `railpack.json` (start уже закреплён).

### 2.3 Pre-deploy (миграции)

Settings → Deploy → Pre-deploy Command:

```bash
python -c "import os; from aibridge.migrate import apply_migrations; apply_migrations(os.environ['DATABASE_URL'])"
```

Timeout ≈ `300` с. Повторный deploy идемпотентен (уже применённые версии не гоняются снова).

### 2.4 Переменные минимума для «процесс + healthz»

Обязательно на сервисе:

```env
PORT=8080
DATABASE_URL=${{aibridge-postgres.DATABASE_URL}}
AIBRIDGE_ALLOW_MEMORY_STORES=false
AIBRIDGE_CHANNEL_BEARER_TOKEN=<secret>
DOGESTONIA_API_BEARER_TOKEN=<другой secret>
```

Для зелёного `/readyz` нужны ещё OpenAI, intake HTTPS URL, content paths в image и т.д. — полный список в pilot runbook §8 и `.env.example`. Не отключайте `AIBRIDGE_DRY_RUN` только из‑за зелёного `/healthz`.

### 2.5 Smoke на Railway

- Deploy logs: uvicorn слушает `$PORT`.
- Из другого сервиса в том же private network (или временный one-off):

```text
http://<aibridge-service>.railway.internal:8080/healthz
```

Порт в URL = `PORT` сервиса aibridge.

Публичный домен для aibridge в pilot не обязателен (канал идёт private HTTP из n8n).

---

## 3. DATABASE_URL: локально vs Railway

| Контекст | URL |
|----------|-----|
| Контейнер aibridge **внутри** Railway | private `${{…DATABASE_URL}}` (`*.railway.internal`) |
| Ноутбук / локальный `python -m aibridge` к той же БД | **публичный** TCP proxy / public Postgres URL из Railway Variables (если включён) |
| Только локальная БД | свой `postgresql://…` на localhost / Docker |

Не копируйте internal hostname в локальный `.env` — DNS с машины упадёт.

---

## 4. Чеклист «веб поднят»

- [ ] `GET /healthz` → `200` `{"status":"ok"}`
- [ ] Процесс на ожидаемом `PORT`
- [ ] При Postgres: миграции применены (pre-deploy и/или старт app)
- [ ] (Опционально) `GET /readyz` → разобрать `reason`, если не 200

Дальше (канал, n8n, Telegram): pilot runbook.
)
