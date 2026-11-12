# REQ-04: `doge-ai-bridge` — строгая готовность, атомарная отправка и корректное подтверждение интерпретации

**Index key:** REQ-04  
**Service / repo:** `doge-ai-bridge`  
**Parent requirements:** REQ-01, REQ-03  
**Status:** Draft — planned immediately after first end-to-end infrastructure launch  
**Priority:** обязательная до допуска жителей и реального gateway stash  
**Version:** 0.1.0 · 2026-09-14

---

## 1. Зачем нужен этот REQ

Сервис уже содержит основные компоненты: HTTP façade, Responses API, PostgreSQL stores, dual-confirm, gateway executor и SPA continuation URL. Однако три защитных механизма пока требуют доработки:

1. сервис способен объявить себя готовым, хотя часть обязательной конфигурации отсутствует;
2. подтверждение Send сохраняется несколькими отдельными операциями и может остаться в неопределённом промежуточном состоянии при crash/redeploy;
3. Interpretation confirm может появиться до того, как AI действительно сформировал итоговое понимание истории, и не всегда инвалидируется после изменения содержания.

REQ-04 не заменяет REQ-01/REQ-03 и не меняет channel OpenAPI v1. Он уточняет обязательное поведение перед включением `AIBRIDGE_DRY_RUN=false` и допуском реальных жителей.

---

## 2. Scope

### Входит

- production-safe PostgreSQL policy;
- строгий `/readyz`;
- проверка фактического runtime wiring;
- атомарная авторизация Send перед gateway HTTPS;
- однократность gateway attempt на revision;
- корректный lifecycle Interpretation confirm;
- revision/hash invalidation при изменении истории;
- restart/crash/concurrency tests этих механизмов;
- redacted operational evidence.

### Не входит

- первичное подключение content bundle к `InterviewEngine` и `ValidationContext`: это непосредственный незакрытый prerequisite REQ-03 и должно быть выполнено до содержательного запуска;
- изменение `docs/openapi/aibridge-channel-v1.openapi.yaml`;
- изменение gateway Story Intake API;
- fork n8n;
- multi-replica load testing, distributed rate limiter и внешний APM;
- redesign Telegram UI;
- Identity/federation и multi-node routing.

---

## 3. Термины простыми словами

| Термин | Значение |
|---|---|
| Ready | Сервис не просто запущен, а действительно способен безопасно обработать предусмотренный режим работы |
| Fail-closed | При сомнительной или неполной конфигурации сервис отказывается принимать рабочий трафик |
| Revision | Версия текущего понимания и подготовленного черновика |
| Interpretation confirm | Пользователь подтверждает, что AI правильно понял актуальную историю |
| Send confirm | Отдельное разрешение отправить конкретную замороженную revision в gateway |
| Atomic transaction | Набор изменений сохраняется в PostgreSQL либо целиком, либо не сохраняется вообще |
| Gateway attempt | Единственная локальная запись о попытке отправить конкретную revision |

---

## 4. R4-01 — PostgreSQL обязателен в production

### Требование

В Railway/pilot/production PostgreSQL является единственным хранилищем для:

- event dedupe и сохранённых HTTP responses;
- sessions и conversation history;
- action-token hashes;
- frozen intent, pending `call_id` и replay items;
- gateway attempts и outcomes;
- content bundle registration и session pinning.

Memory stores разрешены только в явно выбранном test/development режиме.

### Обязательное поведение

1. Production default для `AIBRIDGE_ALLOW_MEMORY_STORES` — `false`.
2. Если `DATABASE_URL` отсутствует, не является PostgreSQL URL или база недоступна, `/readyz` возвращает `503`.
3. Ошибка открытия PostgreSQL store не должна приводить к автоматическому переходу на memory store.
4. Тесты, которым нужна память, включают её явно.
5. В логах разрешён тип backend (`postgres`/`memory`), но запрещены URL, пароль и другие credentials.

### Acceptance criteria

- [ ] Railway-shaped configuration без `DATABASE_URL` → `/readyz` 503.
- [ ] Railway-shaped configuration с недоступным PostgreSQL → `/readyz` 503.
- [ ] PostgreSQL initialization failure не создаёт memory fallback.
- [ ] Test profile с явным memory opt-in продолжает работать.
- [ ] Restart сохраняет session, dedupe, action token и gateway attempt.

---

## 5. R4-02 — `/readyz` проверяет собранную систему, а не отдельные файлы

### Требование

`/readyz=200` означает, что production composition root уже собрал и связал обязательные компоненты текущего deployment.

### `/readyz` обязан подтвердить

1. Channel Bearer существует.
2. Gateway Bearer существует и отличается от Channel Bearer.
3. `DATABASE_URL` указывает на доступный PostgreSQL с актуальной версией миграций.
4. Current content bundle зарегистрирован и прошёл hash/manifest verification.
5. Canonical instructions реально загружены и непусты.
6. Story Intake OpenAPI содержит ровно одну разрешённую операцию `postStoryDraftStash`.
7. Active pack schema загружена.
8. Responses-flat strict tool успешно сгенерирован.
9. `InterviewEngine` использует инструкции и этот strict tool из того же pinned bundle.
10. `ConfirmationGuard.validation_context` собран из того же pinned bundle.
11. `schema_id`, `schema_version`, `deployment_id`, origin source и pack binding согласованы.
12. OpenAI key/model присутствуют; readiness не делает генерацию.
13. Gateway base URL синтаксически корректен и использует HTTPS; readiness не делает stash.
14. SPA redirect base URL корректен.
15. До доказанного полного schema validation разрешён только `AIBRIDGE_DRY_RUN=true`.

### Запрещено

- считать отсутствие content env допустимым в production;
- считать отсутствие tool schema допустимым в production;
- возвращать ready только потому, что файлы существуют, если они не подключены к engine/guard;
- выполнять OpenAI generation или gateway POST из readiness;
- раскрывать secret или полный путь с чувствительными параметрами в response.

### Response

- готово: HTTP 200, bounded JSON `{"status":"ready"}`;
- не готово: HTTP 503, bounded reason code без secret/PII.

Примеры reason codes:

- `database_not_postgres`;
- `database_unreachable`;
- `migration_version_mismatch`;
- `content_bundle_not_ready`;
- `instructions_not_bound`;
- `strict_tool_not_bound`;
- `validation_context_not_bound`;
- `bundle_binding_mismatch`;
- `dry_run_required`.

### Acceptance criteria

- [ ] Полностью отсутствующие content env → 503.
- [ ] Частично заполненные content env → 503 с конкретным reason.
- [ ] Bundle зарегистрирован, но engine не получил tool → 503.
- [ ] Engine и validation context используют разные bundle hash → 503.
- [ ] Полная корректная dry-run конфигурация → 200.
- [ ] Вызов `/readyz` не увеличивает OpenAI/gateway counters.

---

## 6. R4-03 — атомарная авторизация Send

### Продуктовая гарантия

Одно нажатие `Send to DOGEstonia` может авторизовать не более одной попытки отправки одной конкретной revision. Crash, restart, двойной клик и повтор HTTP request не должны создавать второй stash.

### Одна PostgreSQL-транзакция до HTTPS

В одной транзакции и на одном database connection необходимо:

1. найти action token по hash;
2. заблокировать необходимые token/session rows (`SELECT ... FOR UPDATE` или эквивалент);
3. проверить:
   - token state = pending;
   - expiry;
   - Telegram user/chat ownership;
   - session id;
   - deployment id;
   - operation id = `postStoryDraftStash`;
   - revision;
   - expected FSM state;
   - draft hash;
4. убедиться, что frozen body и исходный `call_id` существуют;
5. consume Send token;
6. инвалидировать соседние pending actions этой revision;
7. перевести session в `executing` и убрать повторную авторизацию;
8. создать уникальный gateway attempt `(session_id, revision)` со статусом `executing`;
9. commit.

Если любой шаг не выполнен, вся транзакция откатывается. Gateway HTTPS запрещён.

### После commit

1. Снять database transaction/row locks.
2. Выполнить один HTTPS `POST /story-drafts` с frozen body.
3. В отдельной транзакции записать bounded outcome.
4. При `stashed` сохранить `draft_id` и `continuation_url`.
5. При неопределённой доставке сохранить `unknown_outcome` и запретить автоматический resend этой revision.
6. OpenAI `function_call_output` можно повторить отдельно; повтор gateway stash из-за его ошибки запрещён.

### Crash semantics

| Где произошёл crash | После restart |
|---|---|
| До commit authorization transaction | Token остаётся pending; gateway attempt отсутствует; HTTPS не было |
| После commit, до получения gateway response | Attempt остаётся executing и восстанавливается как `unknown_outcome`; automatic resend запрещён |
| После сохранённого outcome | Повтор event получает сохранённый bounded response; второй gateway POST запрещён |

### Acceptance criteria

- [ ] Token consume, session executing и attempt creation используют один commit.
- [ ] Искусственный crash между логическими шагами до commit оставляет исходное состояние.
- [ ] Два одновременных Send для одной revision дают ровно один gateway attempt.
- [ ] Новый `event_id` со старым consumed token получает 409 без gateway POST.
- [ ] Повтор того же `(channel,event_id)` возвращает сохранённый response.
- [ ] Restart с executing attempt → `unknown_outcome`, zero automatic resend.
- [ ] Никакая DB-транзакция не остаётся открытой во время gateway HTTPS.

---

## 7. R4-04 — корректный Interpretation confirm

### Продуктовая гарантия

Interpretation confirm означает только следующее:

> Пользователь увидел конкретное актуальное понимание своей истории и подтвердил, что AI понял её правильно.

Он не означает Send и никогда не разрешает gateway HTTPS.

### Проблема, которую нужно исключить

Кнопки Interpretation confirm нельзя показывать автоматически после любого обычного ответа модели. Уточняющий вопрос, приветствие или промежуточная реплика не являются готовой интерпретацией.

### Нужен явный readiness signal

Runtime должен получать машинно различимый сигнал, что итоговая интерпретация готова. Допустим один из вариантов реализации:

- отдельный non-consequential structured tool/event `interpretation_ready`;
- строго типизированный structured output;
- другое явно задокументированное поле runtime, не основанное на догадке по тексту.

Signal обязан содержать или однозначно связывать:

- session id;
- revision;
- итоговый resident-visible summary;
- hash актуального interpretation snapshot;
- deployment/bundle binding;
- время создания.

### Lifecycle

1. Пока AI собирает сведения, state остаётся `interviewing`; confirm-кнопок нет.
2. AI формирует итоговую интерпретацию и выдаёт explicit readiness signal.
3. Aibridge сохраняет snapshot/hash/revision.
4. Только после сохранения возвращаются `Looks right / Edit / Cancel`.
5. `Looks right` переводит эту revision в `interpretation_confirmed`; gateway остаётся запрещён.
6. После подтверждения модель может сформировать consequential function call для той же revision.
7. Любое новое пользовательское содержание, меняющее историю, инвалидирует interpretation confirmation, увеличивает revision и требует нового summary/confirm.
8. Send buttons связываются только с frozen body, полученным после актуального interpretation confirmation.

### Что считается изменением содержания

- новый текст жителя;
- Edit;
- изменение structured payload;
- изменение narrative, географии или других полей draft;
- смена pack/bundle/deployment для активной сессии.

Технические повторы того же Telegram event через dedupe изменением не являются.

### Acceptance criteria

- [ ] Приветствие/вопрос модели не создаёт Interpretation buttons.
- [ ] Buttons появляются только после explicit `interpretation_ready`.
- [ ] Snapshot и hash сохранены до возврата buttons.
- [ ] Interpretation confirm не вызывает gateway.
- [ ] Новый содержательный user message после confirm увеличивает revision и инвалидирует старые action tokens.
- [ ] Function call со старой confirmed revision блокируется.
- [ ] Send доступен только для revision, чья интерпретация актуально подтверждена.
- [ ] Restart сохраняет pending interpretation snapshot и действующие opaque buttons.

---

## 8. Совместимость и масштабирование

Доработка не должна менять channel v1 request/response shape. n8n продолжает:

- передавать Telegram update;
- отображать `reply_text`;
- строить кнопки из `actions[]`;
- отправлять обратно только opaque `actions[].token`.

Все решения безопасности остаются в aibridge. Это позволяет позднее подключать дополнительные Telegram bots/nodes без копирования логики подтверждения в workflow.

DB API необходимо проектировать без process-local assumptions, чтобы переход к нескольким ASGI replicas потребовал нагрузочной доработки, а не переписывания state machine.

---

## 9. Test matrix

| Уровень | Обязательная проверка |
|---|---|
| Unit | readiness reasons, state transitions, revision invalidation |
| PostgreSQL integration | atomic Send transaction, unique attempt, rollback, restart recovery |
| ASGI E2E | production `create_app()` без ручного присваивания engine/guard полей |
| Recorded Responses | multi-turn interview → explicit interpretation → confirm → function call → Send |
| Failure injection | crash до/после commit, gateway timeout, lost response, OpenAI follow-up failure |
| Live dry-run | Telegram → n8n → aibridge, zero `/story-drafts` |

Disposable PostgreSQL обязателен для transactional tests. SQLite/memory не являются доказательством конкурентной корректности.

---

## 10. Definition of Done

REQ-04 считается выполненным, когда:

1. все AC R4-01…R4-04 пройдены;
2. production `create_app()` собирает тот же runtime, который тестируется;
3. `/readyz=200` невозможно получить без PostgreSQL и полностью связанного verified bundle;
4. доказано ≤1 gateway attempt на confirmed revision;
5. Interpretation confirm относится к сохранённому актуальному snapshot;
6. live dry-run через n8n проходит без gateway stash;
7. после этого отдельно разрешается решение об установке `AIBRIDGE_DRY_RUN=false`.

---

## 11. Evidence paths

- `src/aibridge/app.py`
- `src/aibridge/config.py`
- `src/aibridge/readiness.py`
- `src/aibridge/confirm.py`
- `src/aibridge/coordinator.py`
- `src/aibridge/pg_runtime.py`
- `migrations/`
- `tests/story13_e2e_helpers.py`
- `docs/openapi/aibridge-channel-v1.openapi.yaml`
- `docs/requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md`

