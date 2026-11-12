# Рекомендации по доработке архитектуры REQ-01 перед пилотом первой ноды

**Проект:** `doge-ai-bridge`  
**Профиль:** `aibridge`  
**Назначение:** постановка для IDE-агента на уточнение документации архитектуры перед реализацией  
**Основание:** REQ-01 v0.4.0 и пакет `docs/architecture/runtime/`  
**Приоритет:** обязательное для пилота либо обязательный архитектурный задел, исключающий переписывание ядра при быстром развёртывании новых нод  
**Не является:** реализацией, изменением runtime-кода или разрешением расширять scope пилота функциями из REQ-02

---

## 1. Цель доработки

Уточнить REQ-01 и архитектуру так, чтобы:

1. первая нода `uus_veerenni_civic / v3` могла безопасно пройти путь Telegram → n8n → aibridge → dual-confirm → gateway stash → SPA;
2. новая нода разворачивалась тем же Docker image и тем же кодом, меняя только проверенный content bundle, настройки окружения и секреты;
3. изменение инструкций или pack не ломало уже начатые интервью;
4. n8n оставался тонким UI/маршрутизатором и не становился вторым владельцем бизнес-логики;
5. реальные пользовательские тексты не сохранялись бесконтрольно в n8n, логах или технических метриках;
6. расходы и длительность Responses-вызовов имели жёсткие технические пределы;
7. ошибки с неопределённым результатом отправки не приводили к автоматическому созданию дублей.

---

## 2. Обновлённый факт об OpenAPI YAML — применить первым

### 2.1 Решение оператора

Оператор перенёс YAML из проекта `GPT UI` в:

```text
doge-ai-bridge/docs/openapi/aibridge-channel-v1.openapi.yaml
```

IDE-агент должен считать это более новым локальным состоянием, чем опубликованная на момент предыдущего аудита ветка `dev`, где файл ещё не был виден.

### 2.2 Обязательная проверка содержания

Нельзя определять назначение YAML только по имени файла. Перед обновлением ссылок IDE-агент должен прочитать документ и классифицировать его по `paths` и `operationId`.

| Контракт | Что обязан содержать | Владелец / назначение |
|---|---|---|
| **Channel façade OpenAPI** | `POST /v1/channel/turns` и `POST /v1/channel/actions`; channel Bearer; bounded request/response envelopes | `doge-ai-bridge`; контракт n8n ↔ aibridge |
| **Story Intake wire OpenAPI** | `operationId: postStoryDraftStash`, `POST /story-drafts`, gateway Bearer и `StoryDraftStashRequest` | канонический wire SSOT; контракт aibridge ↔ gateway и источник strict tool projection |

### 2.3 Правило разрешения возможной ошибки переноса

Если перенесённый YAML по-прежнему описывает `postStoryDraftStash` / `POST /story-drafts`, его нельзя использовать как `aibridge-channel-v1.openapi.yaml` только из-за нового имени.

В таком случае IDE-агент должен:

1. зафиксировать обнаруженное несоответствие;
2. сохранить Story Intake YAML как отдельный канонический wire-артефакт с однозначным именем, например:

   ```text
   docs/openapi/story-intake-actions.openapi.yaml
   ```

3. создать или отдельно поставить создание настоящего `docs/openapi/aibridge-channel-v1.openapi.yaml` для двух façade endpoints;
4. не копировать вручную `StoryDraftStashRequest` во второй контракт;
5. обновить архитектурные ссылки только после классификации файла.

### 2.4 Acceptance criteria по контрактам

- В репозитории существуют два логически разных контракта, если оба нужны физически.
- Channel schema contract-тестируется против FastAPI/ASGI runtime.
- Wire schema используется для разрешения только `postStoryDraftStash`, сборки tool projection и финальной валидации gateway body.
- Изменение channel API не меняет Story Intake wire schema автоматически и наоборот.
- Ни один документ больше не утверждает `name ≠ create`, если channel YAML уже существует и проверен.
- Межрепозиторные ссылки на `GPT UI` заменены абсолютными GitHub URL; относительные ссылки через `../../../GPT UI` не используются.

---

## 3. Обязательные архитектурные доработки для пилота

## 3.1 Версионированное хранение content bundle

### Проблема

Сессия живёт до семи дней без активности и закрепляется за версиями instructions/tool/pack. Новый Docker image не должен удалять bundle, на который ссылается незавершённое интервью.

### Решение для пилота, совместимое с масштабированием

Использовать PostgreSQL как versioned bundle registry:

1. CI собирает immutable tarball и включает его в image.
2. При старте aibridge проверяет manifest, source commit и hashes.
3. После проверки bundle один раз регистрируется в PostgreSQL по итоговому `bundle_hash`.
4. Содержимое либо нормализованные составляющие сохраняются один раз на bundle, а не копируются в каждую сессию.
5. Сессия хранит ссылку на immutable bundle record и отдельные OAS/pack/tool hashes.
6. Запись bundle никогда не изменяется после регистрации.
7. Garbage collection удаляет bundle только если на него нет активных сессий и закончился audit/recovery grace period.

Минимальные логические сущности:

```text
content_bundle
  bundle_hash (unique)
  source_commit
  bundle_version
  instructions_hash
  wire_oas_hash
  pack_hash
  tool_schema_hash
  verified_at
  immutable_payload_or_components

session
  ...
  content_bundle_hash (foreign key)
```

### Почему это не придётся переписывать

- Несколько ASGI-инстансов увидят одинаковые bundle через PostgreSQL.
- Новая нода сможет использовать тот же код и собственный проверенный bundle.
- Позже хранение payload можно перенести в object storage, сохранив hash/reference contract.
- Не требуется Railway Volume, привязанный к одному экземпляру контейнера.

### Обновить документацию

- `docs/architecture/runtime/00-overview.md`
- `docs/architecture/runtime/02-content-packaging.md`
- REQ-01 §8, §14, §18, §20

### Acceptance criteria

- Redeploy с новым bundle не ломает активную сессию на старой версии.
- Две сессии на разных bundle корректно продолжаются параллельно.
- Нельзя изменить bundle под существующим hash.
- GC не удаляет bundle с активной ссылкой.
- Readiness проверяет текущий bundle; загрузка pinned session проверяет наличие её bundle.

---

## 3.2 Устранить противоречие Telegram callback acknowledgement

### Проблема

Текущий workflow рекомендует сначала вызвать Telegram `answerCallbackQuery`, а затем aibridge. При этом façade response содержит `callback_ack_text`, который появляется слишком поздно для первоначального acknowledgement.

### Решение

Для пилота:

1. n8n немедленно вызывает `answerCallbackQuery` с нейтральным локальным текстом либо без текста;
2. затем вызывает `POST /v1/channel/actions`;
3. бизнес-результат aibridge показывает отдельным `Send Message` или `Edit Message`;
4. `callback_ack_text` удалить из обязательного façade contract либо явно пометить как не используемое для первичного acknowledgement поле с планом удаления до фиксации v1.

Предпочтение: удалить неиспользуемое поле до стабилизации channel v1.

### Acceptance criteria

- Telegram callback получает быстрый acknowledgement независимо от latency OpenAI/gateway.
- n8n не принимает security-решения до ответа aibridge.
- Только aibridge определяет результат action; n8n лишь отображает его.

---

## 3.3 Ввести LLM budget policy

### Проблема

Стабильный prompt prefix и cache telemetry описаны хорошо, но отсутствуют числовые ограничения, предотвращающие бесконечный или чрезмерно дорогой turn.

### Обязательные конфигурируемые пределы

Добавить архитектурные параметры и `.env.example` placeholders:

```text
AIBRIDGE_MAX_INPUT_TOKENS
AIBRIDGE_MAX_OUTPUT_TOKENS
AIBRIDGE_MAX_RESPONSES_CALLS_PER_TURN
AIBRIDGE_MAX_TOOL_CALLS_PER_TURN
AIBRIDGE_OPENAI_TIMEOUT_MS
AIBRIDGE_MAX_SESSION_TURNS
AIBRIDGE_PRINCIPAL_RATE_LIMIT
AIBRIDGE_GLOBAL_RATE_LIMIT
```

Точные пилотные числа должны быть выбраны при реализации после измерения реального bundle и модели. Архитектура обязана определить поведение при превышении:

- fail bounded, без бесконечного retry;
- resident-safe сообщение;
- сохранение последнего подтверждённого состояния;
- отсутствие gateway side effect;
- redacted metric с причиной остановки.

Суммаризация истории допускается только как отдельная проверяемая трансформация. Она не должна изменять frozen draft, confirmation state или pinned content version.

### Acceptance criteria

- На один Telegram event невозможно создать неограниченное число OpenAI-вызовов.
- Output и общий контекст ограничены.
- Timeout/cancel не продвигает сессию молча.
- Usage и cached tokens доступны в метриках без narrative.

---

## 3.4 Зафиксировать n8n workflow как отдельный ops-артефакт

### Проблема

n8n workflow не является частью runtime-кода aibridge, но без его версии невозможно воспроизводимо развернуть новую ноду или восстановиться после потери n8n.

### Решение

Не включать workflow в бизнес-логику aibridge. Создать отдельный версионированный deployment/ops-артефакт, содержащий:

- экспортированный workflow JSON без credentials;
- совместимую версию `aibridge-channel-v1`;
- mapping Telegram fields → façade request;
- mapping façade actions → inline keyboard;
- инструкции импорта и активации;
- имена необходимых credentials без значений;
- версию n8n, на которой workflow проверен;
- smoke checklist.

Каждая новая нода должна импортировать один и тот же шаблон workflow и менять только Bot credential, private aibridge URL/channel credential и отображаемые node labels при необходимости.

### Acceptance criteria

- Новая нода разворачивается без ручного конструирования Switch/HTTP nodes.
- В JSON нет Telegram token, channel Bearer, gateway Bearer или OpenAI key.
- Workflow не содержит gateway URL и никогда не вызывает `/story-drafts`.
- Совместимость workflow ↔ channel OpenAPI проверяется smoke/E2E.

---

## 3.5 Закрыть privacy по всей системной цепочке

### Проблема

Ограничения aibridge не запрещают n8n сохранять полный Telegram payload и ответы workflow. `store: false` также регулирует хранение Responses, но не означает, что пользовательские данные вообще не обрабатываются OpenAI или Telegram.

### Требования перед приглашением реальных жителей

1. Создать `docs/runbooks/privacy-pilot.md` либо общий system privacy runbook.
2. Для n8n определить и проверить:
   - запрет или минимизацию сохранения успешных execution payload;
   - короткий retention error executions;
   - запрет pinning execution с реальными данными;
   - очистку старых executions;
   - отсутствие narrative в custom logs.
3. Для aibridge:
   - narrative/Responses items ≤7 дней sliding;
   - раннее удаление после stash/Cancel, когда continuation больше не нужен;
   - audit metadata отдельно и без полного текста;
   - операторское удаление сессии;
   - определить backup retention и действие удаления относительно backups.
4. Для пользовательского интерфейса:
   - короткое уведомление до начала интервью о Telegram, AI processing и цели обработки;
   - не называть Telegram principal подтверждённой DOGEstonia Identity;
   - не обещать публикацию после stash.
5. Зафиксировать владельцев обработки и внешних процессоров организационно; это не должно реализовываться моделью.

### Acceptance criteria

- Тестовый workflow с уникальной фразой не оставляет её в стандартных n8n success execution records после принятого retention window.
- Полный narrative отсутствует в stdout и `/metrics`.
- Удаление сессии проверяется интеграционным тестом.
- Пользователь видит privacy notice до передачи содержательного рассказа.

---

## 3.6 Определить reconciliation для `unknown_outcome`

### Проблема

Gateway пока не гарантирует idempotency. При потере ответа aibridge правильно запрещает автоматическую повторную отправку, но операторский процесс не определён полностью.

### Решение для пилота

Создать `docs/runbooks/unknown-outcome-reconciliation.md` и минимальную операторскую поверхность без повторной автоматической отправки.

Runbook должен определить:

- как обнаруживается `unknown_outcome`;
- какие локальные `request_id`, attempt ID, gateway `trace_id` или hash доступны;
- как проверить наличие draft на стороне gateway доступным операторским способом;
- какие переходы разрешены после проверки;
- что видит пользователь;
- кто имеет право завершить reconciliation;
- запрет кнопки автоматического повторного Send для той же revision.

Если gateway не предоставляет lookup, это явно фиксируется как ограничение пилота. Ручное решение не должно выдавать неподтверждённый результат `stashed`.

---

## 3.7 SPA continuation URL для мобильного пилота

`localhost` допустим только в контролируемом тесте, когда SPA действительно доступна на устройстве, открывающем ссылку. Для Telegram на телефоне `localhost` означает сам телефон.

До полного wave-2 E2E требуется:

- пользовательски доступный HTTPS base URL SPA;
- allowlisted origin из env;
- тест открытия ссылки из Telegram mobile;
- URL encoding `draft_id`;
- отсутствие continuation URL для любого outcome кроме `stashed`.

---

## 4. Архитектурный задел для быстрого запуска новых нод

## 4.1 Не делать runtime multi-tenant в пилоте

Сохранить правило:

```text
one deployment = one node = one active pack
```

Быстрое масштабирование достигается тиражированием стандартного образа, а не добавлением `if node == ...` в Python.

## 4.2 Все различия ноды — только в Node Deployment Configuration

Код не должен содержать `uus_veerenni`, Tallinn или civic-поля. На deployment задаются:

- стабильный `node_id` / deployment identity;
- content source commit и bundle hash;
- pack ID/version/hash;
- wire OAS hash и operation allowlist;
- gateway base URL и отдельный gateway Bearer;
- SPA base URL;
- `origin.source`;
- модель и budget policy;
- retention и rate-limit values;
- channel Bearer.

Серверные значения нельзя принимать из n8n или LLM.

## 4.3 Стабильные интерфейсы

- n8n интегрируется только через versioned channel OpenAPI.
- Runtime получает node differences через verified bundle/env, а не через новый код.
- Gateway body формируется только из wire SSOT + pack projection.
- Новые необязательные response fields добавляются обратно совместимо.
- Ломающие изменения получают новый API major version, а не тихо меняют `/v1`.
- Database migrations должны быть forward-compatible с rolling redeploy, насколько допускает один сервис пилота.

## 4.4 Namespace данных

Даже при отдельной БД на ноду сущности должны содержать стабильную `deployment_id`/`node_id` привязку там, где она участвует в безопасности token/session/bundle. Это позволит позднее объединить инфраструктуру или проводить перенос без изменения основных ключей и hash domain.

Не использовать переданный клиентом `node_id` как источник маршрутизации или авторизации.

## 4.5 Release contract новой ноды

Новая нода считается развёрнутой только после:

1. проверки manifest/OAS/pack hashes;
2. migrations;
3. `/readyz`;
4. unauthenticated façade smoke → 401;
5. live n8n → `/v1/channel/turns` с channel Bearer;
6. отсутствия real stash в wave 1;
7. отдельного wave-2 dual-confirm E2E;
8. проверки privacy settings n8n;
9. проверки SPA URL на реальном пользовательском устройстве.

---

## 5. Точечные изменения по документам

| Документ | Требуемая доработка |
|---|---|
| `docs/requirements/REQ-01-doge-ai-bridge-runtime.md` | Обновить статус channel YAML после проверки; развести channel/wire OAS; добавить LLM budgets, n8n privacy dependency, bundle registry/GC, callback ack решение и reconciliation deliverable |
| `docs/architecture/runtime/00-overview.md` | Убрать устаревшее `name ≠ create`; добавить принятый physical bundle store; показать external n8n ops artifact и privacy boundary |
| `docs/architecture/runtime/01-channel-facade.md` | Синхронизировать с фактическим channel YAML; разрешить `callback_ack_text`; добавить contract version compatibility |
| `docs/architecture/runtime/02-content-packaging.md` | Зафиксировать PostgreSQL versioned bundle registry и GC вместо `Unknown`; заменить двусмысленное `monorepo` на multi-repository CI checkout |
| `docs/architecture/runtime/03-confirm-gateway.md` | Добавить pre-send safe failure и `unknown_outcome` reconciliation state rules |
| `docs/architecture/runtime/04-ops-security.md` | Добавить n8n execution privacy, LLM budget metrics, backup/retention и mobile SPA gate |
| `docs/runbooks/channel-bearer-rotation.md` | Оставить; добавить ссылку из общего Operator README |
| Новый privacy runbook | n8n/aibridge/Telegram/OpenAI data path, retention и deletion checklist |
| Новый reconciliation runbook | безопасная ручная обработка `unknown_outcome` |
| Отдельный ops/deploy location | versioned n8n workflow JSON без секретов |

---

## 6. Приоритет реализации

### P0 — до реализации зависимого компонента

1. Классифицировать и развести два OpenAPI-контракта.
2. Создать/finalize channel v1 contract.
3. Зафиксировать PostgreSQL versioned bundle registry и GC.
4. Исправить callback acknowledgement contract.
5. Зафиксировать LLM budget policy и bounded failure behavior.

### P1 — до wave 1

1. Versioned n8n workflow artifact без секретов.
2. Bundle registration/migrations/readiness.
3. Private façade + channel Bearer + smoke/live turn.
4. Проверяемые rate/timeout/token limits.

### P1 — до реальных пользователей / wave 2

1. n8n privacy configuration и privacy notice.
2. `unknown_outcome` reconciliation runbook.
3. Публично доступный HTTPS SPA continuation URL.
4. Полный dual-confirm E2E на RU/ET/EN.
5. Проверка удаления narrative и отсутствия PII в logs/metrics.

---

## 7. Definition of Done этой доработки документации

- Все решения выше отражены в REQ и соответствующих architecture siblings без противоречий.
- Фактическое содержание нового YAML прочитано и его роль определена по paths/operationId.
- Channel façade и Story Intake wire API не смешаны.
- Ни один обязательный pilot seam не остаётся просто `Unknown`, кроме конкретных numeric defaults, выбираемых измерением.
- Новая нода не требует изменения Python-кода.
- Архитектура явно отделяет pilot requirements от REQ-02.
- IDE-агент выдаёт список изменённых документов и consistency matrix, но не начинает implementation wave без отдельной команды оператора.

---

*Конец документа.*
