# aibridge: запуск только веб-сервиса (локально и Railway)

**Цель:** поднять HTTP-процесс `doge-ai-bridge` и проверить liveness.  
**Не входит:** n8n, Telegram, полный pilot — см. [AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md](./AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md).  
**Шаблон env:** [`.env.example`](../../.env.example) · **код настроек:** `src/aibridge/config.py`

---

## Что запускается

```text
uvicorn → aibridge.app:app
  GET /health    — REQ9-primary: процесс жив (без секретов); alias /healthz
  GET /ready     — REQ9-primary: готовность конфига/зависимостей (может быть 503); alias /readyz
```

Старт:

| Где | Команда |
|-----|---------|
| Локально | `make serve` / `make dev` (required `./.env`, G8) · thin alias `PORT=8080 python -m aibridge` |
| Dockerfile `CMD` | `python -m uvicorn --app-dir src aibridge.app:app --host 0.0.0.0 --port ${PORT:-8080}` |
| Railpack | то же в `railpack.json` (`${PORT:-8080}`) |

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

Минимум для старта процесса (не обязательно зелёный `/ready` / `/readyz`):

```env
PORT=8080
AIBRIDGE_CHANNEL_BEARER_TOKEN=dev-channel-token
GATEWAY_SERVICE_API_TOKEN=dev-gateway-token-different
```

Для Postgres (предпочтительно):

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/aibridge
AIBRIDGE_ALLOW_MEMORY_STORES=false
```

#### Локальный Postgres из Homebrew (системный сервис)

Если Postgres установлен «из коробки» через Homebrew (`postgresql@15`):

```bash
# статус
brew services list | grep postgres

# запуск (остаётся в фоне после перезагрузки логина)
brew services start postgresql@15

# остановка
brew services stop postgresql@15
```

Создать БД/роль под свой `DATABASE_URL` (пример; подставьте user/db):

```bash
/opt/homebrew/opt/postgresql@15/bin/createdb aibridge
# затем в .env:
# DATABASE_URL=postgresql://$(whoami)@localhost:5432/aibridge
```

**Важно для QA pytest (story 34 UC / часть LIFE):** системный Homebrew Postgres **не** то, что проверяет `pg_available()`. Эти тесты ждут **отдельный disposable** кластер в `doge-ai-bridge/.pgdata-test`:

```bash
cd doge-ai-bridge
./scripts/start-disposable-pg.sh
# URL: postgresql://aibridge@/aibridge_test?host=.../.pgdata-test&port=55432
```

Скрипт переживает «осиротевший» listener на `:55432` и stale shm (stop/kill + retry). Запускать в **обычном Terminal**, не из sandbox Cursor (иначе `shmget: Operation not permitted`).

Подробный прогон QA: [`../qa/inbound-outbound/TEST-MANUAL.md`](../qa/inbound-outbound/TEST-MANUAL.md).

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
# из doge-ai-bridge, с активированным .venv и заполненным ./.env (G8)
make serve
# или: make dev
```

Thin alias (без Make `.env` load):

```bash
PORT=8080 python -m aibridge
```

Эквивалент uvicorn напрямую:

```bash
PYTHONPATH=src python -m uvicorn --app-dir src aibridge.app:app --host 0.0.0.0 --port 8080
```

### 1.4 Smoke

```bash
# REQ9-primary
curl -sS http://127.0.0.1:8080/health
# ожидаемо: {"status":"ok"}

curl -sS http://127.0.0.1:8080/ready
# 200 {"status":"ready"} или 503 {"status":"not_ready","reason":"..."}

# aliases (same semantics)
# curl -sS http://127.0.0.1:8080/healthz
# curl -sS http://127.0.0.1:8080/readyz
```

`/health` (`/healthz`) = процесс слушает. `/ready` (`/readyz`) = полный checklist (Bearer’ы, dry-run, content paths, DB, OpenAI presence и т.д.) — см. `src/aibridge/readiness.py`.

### 1.5 Частые локальные сбои

| Симптом | Что проверить |
|---------|----------------|
| Процесс падает при импорте / старте | `DATABASE_URL` недоступен с машины (DNS/сеть). Для локальной разработки к Railway Postgres нужен **публичный** proxy URL; private `*.railway.internal` с ноутбука не резолвится. |
| `/ready` или `/readyz` 503 | Смотреть `reason` в JSON; добить env по `.env.example` / pilot §8. |
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
GATEWAY_SERVICE_API_TOKEN=<другой secret>
```

Для зелёного `/ready` (`/readyz`) нужны ещё OpenAI, intake HTTPS URL, content paths в image и т.д. — полный список в pilot runbook §8 и `.env.example`. Не отключайте `AIBRIDGE_DRY_RUN` только из‑за зелёного `/health` (`/healthz`).

### 2.4.1 Railway target var names (REQ9 checklist — Lock C)

**Names only** — set/verify on live Railway is **STORY-AIBRIDGE-REQ9-04** (do not invent SUCCESS here).

| aibridge Railway var | Role | Peer / note |
|----------------------|------|-------------|
| `GATEWAY_BASE_URL` | HTTPS origin of intake/gateway peer | complaints node → gateway public HTTPS origin |
| `GATEWAY_SERVICE_API_TOKEN` | S2S Bearer aibridge → gateway | **same secret value** as gateway `SERVICE_API_TOKEN` (pairing); **≠** `AIBRIDGE_CHANNEL_BEARER_TOKEN` (R8) |
| `SPA_BASE_URL` | SPA base for `continuation_url` | resident SPA public origin |
| `AIBRIDGE_CHANNEL_BEARER_TOKEN` | channel façade Bearer (Keep) | n8n / channel clients only — never equal to gateway S2S |

Removed as primary (no dual-read): `DOGESTONIA_INTAKE_BASE_URL`, `DOGESTONIA_API_BEARER_TOKEN`, `DOGESTONIA_DRAFT_REDIRECT_BASE_URL`.

### 2.5 Smoke на Railway

- Deploy logs: uvicorn слушает `$PORT`.
- Из другого сервиса в том же private network (или временный one-off):

```text
http://<aibridge-service>.railway.internal:8080/health
# alias: …/healthz
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

- [ ] `GET /health` → `200` `{"status":"ok"}` (alias `/healthz` OK)
- [ ] Процесс на ожидаемом `PORT`
- [ ] При Postgres: миграции применены (pre-deploy и/или старт app)
- [ ] (Опционально) `GET /ready` → разобрать `reason`, если не 200 (alias `/readyz` OK)

Дальше (канал, n8n, Telegram): pilot runbook.
)
