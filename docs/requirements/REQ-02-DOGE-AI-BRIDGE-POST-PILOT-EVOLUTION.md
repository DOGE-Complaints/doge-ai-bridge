# REQ-02: `doge-ai-bridge` — постпилотное развитие

**Service / repo:** `doge-ai-bridge`  
**Depends on:** REQ-01 v0.4.x — pilot runtime  
**Status:** Draft / post-pilot backlog  
**Priority:** не блокирует запуск первой ноды при выполнении REQ-01 и pilot recommendations  
**Назначение:** собрать последующие улучшения в отдельный scope, не перегружая пилот и не ослабляя его безопасность

---

## 1. Цель

После подтверждения работоспособности первой ноды расширить aibridge от безопасного single-node Telegram pilot к управляемой федеративной инфраструктуре с Identity, автоматизированным подключением нод, более сильной доставкой, несколькими каналами и зрелой эксплуатацией.

REQ-02 не разрешает откладывать из REQ-01:

- dual-confirm;
- channel/gateway secret separation;
- strict schema validation;
- pinned sessions;
- n8n privacy controls;
- bounded LLM usage;
- safe `unknown_outcome` behavior;
- pilot E2E и доступный SPA continuation URL.

---

## 2. Принципы совместимости

1. Стабильный `/v1/channel/*` продолжает работать для уже развёрнутых нод.
2. Изменения добавляются обратно совместимо либо через новый major API version.
3. Node-specific behavior не добавляется условными ветками в core runtime.
4. Существующие bundle/session hashes остаются проверяемыми после migrations.
5. Новые способы авторизации не переиспользуют channel или gateway Bearer не по назначению.
6. Новые каналы используют ту же confirm policy и gateway executor, а не копируют их.
7. Миграции допускают поэтапное обновление нод без одновременной остановки всей федерации.

---

## 3. Post-pilot scope

## 3.1 DOGEstonia Identity и переносимость пользователя

### Цель

Заменить доверие только к Telegram `user_id/chat_id` на привязку канальной сессии к подтверждённой DOGEstonia Identity там, где пользователь выбирает авторизацию.

### Требования

- OAuth/OIDC-подобный redirect flow через публичный DOGEstonia Identity URL без ребрендинга провайдером ноды.
- State/nonce/PKCE или эквивалентные средства защиты выбранного протокола.
- Telegram principal остаётся channel binding, но не становится federation identity.
- Identity subject не передаётся модели без необходимости.
- Возможность начать анонимно и позднее привязать draft/session по явному действию пользователя.
- Revocation, logout и unlink channel.
- Threat model для account linking.

### Acceptance criteria

- Один пользователь может продолжить разрешённый workflow через другой клиент после Identity auth.
- Нельзя привязать чужой Telegram chat к Identity посредством подмены callback.
- Отказ от Identity не ломает разрешённый анонимный сценарий, если он поддерживается политикой ноды.

---

## 3.2 Реестр нод и matching по критериям приёма

### Цель

История направляется не потому, что пользователь вошёл через приложение конкретной ноды, а по совместимости story с опубликованными критериями приёма нод.

### Требования

- Проверяемый node registry с `node_id`, endpoint metadata, supported schema/pack versions, jurisdiction и acceptance criteria.
- Подписанные или иным образом проверяемые записи реестра.
- Отдельный policy layer для matching; LLM может предлагать, но не является единственным авторитетом маршрутизации.
- Явный выбор/согласие пользователя перед отправкой в выбранную ноду.
- Защита от node-supplied URL injection: endpoint берётся только из проверенного registry/config.
- Обработка недоступной, отозванной или несовместимой ноды.

---

## 3.3 Автоматизированный onboarding и выпуск ноды

### Цель

Сделать создание новой ноды повторяемой операцией без ручной сборки workflow и без участия автора core-кода.

### Требования

- Валидируемый node deployment descriptor.
- CI template: checkout content refs → validate → bundle → image/config → deploy gates.
- Автоматическая проверка manifest, pack, OAS и совместимости версий.
- Импорт шаблона n8n workflow без credentials.
- Автоматический smoke и отчёт о готовности.
- Rollback к предыдущему release descriptor.
- Подписанный release manifest / provenance как отдельное улучшение supply-chain.

---

## 3.4 Gateway idempotency и authoritative outcome lookup

### Цель

Устранить необходимость ручного решения большинства `unknown_outcome`.

### Требования

- Gateway принимает стабильный client operation/idempotency key для одной подтверждённой revision либо предоставляет lookup по operation reference.
- Уникальность обеспечивается на стороне gateway.
- Повторный запрос возвращает исходный результат, а не создаёт второй draft.
- aibridge меняет retry policy только после отдельного versioned protocol review.
- Contract, concurrency и lost-response tests обязательны.

### Совместимость

До поддержки gateway продолжает действовать безопасное правило REQ-01: `unknown_outcome`, без автоматического retry.

---

## 3.5 Расширенная операторская консоль и reconciliation UI

### Цель

Заменить часть ручных SQL/runbook действий безопасной административной поверхностью.

### Требования

- Просмотр redacted operational states без narrative по умолчанию.
- Поиск по request/attempt/trace references.
- Controlled reconciliation с обязательным audit trail.
- Session delete/expire.
- Просмотр bundle adoption и безопасный GC.
- Role-based operator access и strong authentication.
- Никакого просмотра Bearer/raw action tokens.

---

## 3.6 Внешний monitoring/APM

### Требования

- Отдельный metrics credential или mTLS; channel Bearer не переиспользуется.
- Dashboards для latency, errors, OpenAI/cache cost, confirm funnel и gateway outcomes.
- Alerting без PII в labels.
- Низкая cardinality: session/user/chat/hash не используются как metric labels.
- Определённые SLO/SLI после получения pilot baseline.
- Trace correlation без полного текста истории.

---

## 3.7 Queue workers и горизонтальное масштабирование

### Триггер включения

Добавлять только если pilot metrics показывают недостаточность async single-ASGI topology.

### Возможности

- Несколько ASGI replicas.
- Отдельные workers/queue для допустимых фоновых операций.
- Distributed locking и fencing для session turns/actions.
- Backpressure и bounded queues.
- Graceful deployment без повторения consequential requests.

### Ограничение

Gateway Send нельзя бездумно переносить в автоматически повторяемую очередь до появления idempotency contract.

---

## 3.8 Внешний content registry / object storage

### Триггер включения

Использовать, когда объём или число bundle становится неудобным для pilot PostgreSQL registry.

### Требования

- Content-addressed immutable objects.
- Hash verification перед использованием.
- Session references сохраняют прежний contract.
- Transactional publish pointer на current bundle.
- GC только после отсутствия активных references и grace period.
- Защита от mutable overwrite и rollback attack.

---

## 3.9 Дополнительные каналы и собственное приложение

### Возможные клиенты

- DOGEstonia mobile/web app;
- web chat;
- voice channel;
- другие мессенджеры.

### Требования

- Channel adapter передаёт нормализованные events и opaque actions.
- Core Responses, validation, confirm и gateway logic не копируются в клиент.
- Каждый канал реализует быстрый acknowledgement и безопасное отображение Send/Edit/Cancel.
- Channel-specific identity связывается с DOGEstonia Identity отдельным защищённым flow.

---

## 3.10 Model routing и локальные модели

### Цель

Снижать стоимость или повышать приватность после появления моделей, проходящих evaluation suite.

### Требования

- Provider/model adapter не меняет domain state machine.
- Модель допускается только после RU/ET/EN tests, instruction-following, strict structured output и tool-intent evaluation.
- Consequential permission всегда остаётся вне модели.
- Возможен routing простых turns на дешёвую модель, но frozen draft и validation остаются серверными.
- Локальная модель не получает автоматического доверия только из-за local execution.

---

## 3.11 Продвинутая стоимость и квоты

### Требования

- Бюджеты на deployment/node и период.
- Soft/hard quota с понятным пользовательским поведением.
- Model fallback только между заранее проверенными совместимыми моделями.
- Отчёт cached/uncached input, output и estimated cost.
- Защита от массового abuse одной channel credential.
- Никаких user/chat identifiers в публичных metrics labels.

---

## 3.12 Расширенные evaluations

- Регрессионный корпус RU/ET/EN.
- Prompt injection и попытки изменить node/gateway/confirmation.
- Длинные, противоречивые и эмоциональные истории.
- Accessibility/text-only alternative для action flows.
- Pack compatibility matrix для нескольких типов нод.
- Shadow evaluation новой модели или bundle до promotion.
- Проверка, что модель не обещает публикацию вместо stash.

---

## 4. Осознанно не включено автоматически

Следующие изменения требуют отдельного продуктового и security решения даже после пилота:

- единый multi-tenant runtime для всех нод;
- автоматическая отправка одной истории сразу во множество нод;
- хранение полного narrative в federation registry;
- разрешение модели выбирать произвольный endpoint;
- передача gateway Bearer в n8n или клиентское приложение;
- автоматическая публикация истории после stash;
- обучение модели на историях жителей без отдельного правового основания и governance.

---

## 5. Предлагаемый порядок post-pilot работ

| Очередь | Возможность | Условие старта |
|---:|---|---|
| 1 | Gateway idempotency/lookup | Есть pilot evidence по ambiguous outcomes или готовность gateway |
| 2 | Node onboarding automation | Первая нода стабильно разворачивается вручную по release contract |
| 3 | Identity linking | Утверждены user journey, privacy roles и Identity protocol |
| 4 | Node registry + matching | Есть минимум две совместимые ноды и формализованные acceptance criteria |
| 5 | Operator UI/APM | Runbooks и pilot metrics показали реальные повторяющиеся операции |
| 6 | Horizontal workers | Нагрузка доказала необходимость |
| 7 | Additional channels/local models | Пройдены contract/evaluation gates |

Порядок может меняться по данным пилота; ни один пункт не должен внедряться только ради архитектурной полноты.

---

## 6. Общие acceptance criteria REQ-02

- Расширения не ослабляют dual-confirm и server-owned configuration.
- Первая нода продолжает работать во время и после migrations.
- Новая нода не требует fork n8n или изменения core Python-кода.
- Identity и routing не превращают Telegram ID в неподтверждённую глобальную личность.
- Gateway delivery не называется strict idempotent до появления серверного контракта.
- Все новые API versioned и contract-tested.
- Все новые хранилища имеют retention/delete/provenance rules.
- Все новые модели проходят multilingual и tool-safety evaluations.
- Документация обновляется вместе с изменением интерфейсов и runbooks.

---

## 7. Выходные артефакты будущей детализации

Каждый принятый раздел REQ-02 перед implementation должен получить отдельную постановку с:

- owner и boundaries;
- protocol/schema;
- threat model;
- migrations/rollback;
- observability;
- privacy/retention;
- tests и acceptance criteria;
- совместимостью с действующими нодами.

---

*Конец REQ-02.*
