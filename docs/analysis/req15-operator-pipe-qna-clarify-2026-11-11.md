# REQ15 — уточнения к пайпу (Q&A для визуализации) · 2026-11-11

**Role:** ответы на операторские вопросы перед цветной схемой · не Product Done.  
**Method:** [`.cursor/rules/analysis.mdc`](../../.cursor/rules/analysis.mdc)  
**Parent training:** [`req15-operator-pipe-and-buttons-training-2026-11-11.md`](./req15-operator-pipe-and-buttons-training-2026-11-11.md)  
**Code SSOT:** `doge-ai-bridge/src/aibridge/{channel,confirm,coordinator,confirm_fsm,seam_policy,channel_wire,request_assembly}.py` · arch [`05-send-after-draft-confirm-validate.md`](../../doge-ai-bridge/docs/architecture/req15-tg-channel-interviewer-ux/05-send-after-draft-confirm-validate.md)

**Честность:** ниже — **Present в коде** + **Observed live 11.11** где есть логи. Code/harness ≠ live SUCCESS до Send/stash.

---

## Краткая карта «между Looks right и Send»

```text
Looks right (callback)
  → telegram → POST /v1/channel/actions
  → confirm.consume_action_token(CONFIRM_INTERPRETATION)
       · verify token (иначе 409 Token expired — модель НЕ вызывается)
       · FSM: awaiting_interpretation_confirm → interpretation_confirmed
       · gateway_authorized=False · actions=[] · post_confirm_engine=True
  → channel.run_post_interpretation_confirm_chain  (вне turn_lock)
       · ОДИН InterviewEngine.run_turn с server-owned prompt
       · coordinator.build_turn_from_engine
            · нет FC / engine fail → offer_continue_seam (Continue/Edit)
            · есть FC → validate_function_calls (+ run_three_gates)
                 · OK → persist_pending_tool (freeze) → offer_send_confirm (Send/Edit/Cancel)
                 · fail → Continue/Edit · без Send · без gateway
```

Участники: **человек** (кнопка) · **telegram poller** · **aibridge Confirm FSM + coordinator** · **InterviewEngine → provider API** · **Python validate/gates** · кнопки снова минтит **aibridge**. Gateway stash **ещё нет**.

---

## 1. Что названо «Custom GPT»?

**Не** обязательно бот из UI ChatGPT Custom GPT.

На live TG (Observed 11.11): текст пишет **модель через API**, которую вызывает **`InterviewEngine`** внутри **aibridge** (provider = DeepSeek / OpenAI по env). Инструкции собираются как `core` + **один** role-slice (`select_next_role` + `assemble_role_prompt` в `channel_wire.apply_before_engine_turn` на текстовых turns).

| Поверхность | Кто зовёт модель |
|-------------|------------------|
| Telegram channel | aibridge `InterviewEngine` → provider adapter |
| ChatGPT Custom GPT (отдельный pack upload) | UI ChatGPT — **другой** runtime; ROL-07 в файлах на диске ≠ авто-apply remote GPT |

Слово «Custom GPT» в training = разговорное «инструкционный pack ролей», не «бот в chatgpt.com рисует кнопки».

---

## 2. `semantic_state.phase` vs Confirm FSM

**Два независимых контура.**

| Контур | Где | Кто меняет | На что влияет |
|--------|-----|------------|---------------|
| `semantic_state.phase` | `SemanticStateService` / store | явные `set_phase` (wire читает; default `"interviewing"`) | **какая роль** в `select_next_role` |
| Confirm FSM `sess.state` | `ConfirmSession` + `confirm_fsm.py` | `offer_*` / `consume_action_token` / Edit/Cancel/gateway outcomes | **какие кнопки** и можно ли FC/Send |

**Да:** FSM может быть `awaiting_send_confirm` (или `interpretation_confirmed`), пока `phase` остаётся `interviewing`. Live default phase не auto-переключается extractor→checker→normalizer.

---

## 3. Кто решает, что черновик «готов к подтверждению»?

Инициатор перехода `interviewing → awaiting_interpretation_confirm` — **сервер aibridge**, не модель и не отдельный «ready detector».

Условие (код): на **FC-less** ответе engine, пока Confirm FSM = `INTERVIEWING`, `build_turn_from_engine` → `requires_fcless_actions` → `offer_interpretation_confirm` (`seam_policy`: INTERVIEWING FC-less = interpretation seam). Это минтит Looks right/Edit/Cancel и делает FSM hop.

Модель может *говорить* «черновик готов»; **кнопки Confirm** появляются из seam policy. Пока state = `awaiting_interpretation_confirm`, STORY-71 **remint** того же набора на новых turns.

---

## 4. Что запускает Looks right? (порядок)

1. TG callback → doge-telegram → `POST /v1/channel/actions` (`process_action`).  
2. `ConfirmationGuard.consume_action_token`:
   - `verify_for_consume` (owner/TTL/revision/expected_state) — fail → **409**, цепочка стоп;  
   - `CONFIRM_INTERPRETATION` → `interpretation_confirmed`, consume+invalidate tokens, `post_confirm_engine=True`, **без** gateway.  
3. Вне lock: `run_post_interpretation_confirm_chain`:
   - server prompt `POST_INTERPRETATION_CONFIRM_PROMPT` («citizen confirmed… emit allowlisted function_call or continue»);  
   - **один** `_run_engine_turn` → `build_turn_from_engine`.  
4. Ответ пользователю = `reply_text` + новый `actions` (Send-набор **или** Continue/Edit) в **том же** success payload `/actions`.

На 11.11 Observed: шаги 3–4 **не** выполнялись из‑за 409 на шаге 2.

---

## 5. Участвуют ли extractor / checker / normalizer после Looks right?

**Как отдельные LLM-роли в auto-chain — нет** на live default.

Два разных «авто»:

| Утверждение | Смысл | Present |
|-------------|--------|---------|
| Нет auto-chain ролей на live TG | `phase` не гоняет extract→check→normalize само | **Да** |
| Есть post-confirm цепочка STORY-72 | consume → **один** engine turn → Python validate/gates → mint Send/Continue | **Да** |

Post-confirm engine обычно всё ещё с instructions последней сборки (часто **interviewer**). Python `validate_function_calls` / `run_three_gates` — **не** вызовы ролей extractor/checker/normalizer. Prose «передача на extractor выполнена» без смены phase/кнопок = **искажение** (ROL-07).

---

## 6. «Один вызов модели на turn»

Правило: **один** `InterviewEngine` turn = **один** `client.create` / provider call с **одной** активной ролью в instructions.

| Вход | Модель |
|------|--------|
| Текстовое сообщение | 1 вызов на `/v1/channel/turns` |
| Looks right (OK token) | +1 вызов в post-confirm chain (server prompt) |
| Looks right (409 expired) | **0** вызовов |
| Send | gateway HTTPS; опционально `submit_function_call_output` после stash — отдельный follow-up, не «три роли подряд» |

Обработка одного Looks right **не** запускает последовательные вызовы extractor→checker→normalizer.

---

## 7. Что такое FC в `Validate + function call OK`?

| Вопрос | Ответ (код) |
|--------|-------------|
| Имя | Allowlist: **`postStoryDraftStash`** (`CANONICAL_OPERATION_ID`) |
| Кто запрашивает | Модель в ответе engine (`function_calls` в result) |
| Кто исполняет HTTP | **Не** модель. После validate aibridge **freeze** intent; HTTP stash только при consume **`CONFIRM_SEND`** |
| Успех для кнопки Send | Ровно 1 FC · имя в allowlist · FSM ∈ {`interpretation_confirmed`,`awaiting_send_confirm`} · `run_three_gates` OK · `persist_pending_tool` → `offer_send_confirm` |

**Отличие от Send:** FC+validate = подготовить и заморозить тело; Send = `execute_stash` по **frozen** arguments (+ `draft_hash` / deployment checks).

---

## 8. Что проверяет Validate?

`validate_function_calls` + `run_three_gates`:

1. Ровно один consequential FC; имя allowlist; есть `call_id`; args JSON object.  
2. FSM: FC запрещён до interpretation confirmed.  
3. Gate1 — tool args schema; Gate2 — `structured_payload` vs pack schema; Gate3 — assembled wire body; затем `draft_hash`.

Это **структура/схемы/сборка тела**, не «проза черновика красивая» и не отдельный safety-LLM checker.

Блокируют Send (Continue/Edit или ошибка в reply): нет FC; validate fail; нет `ValidationContext`; нет `frozen_tool_intent`; `send_blocked_for_revision` (unknown_outcome); mismatch draft_hash/deployment на Send.

---

## 9. Кнопка Continue

| | |
|--|--|
| Когда | Post-confirm: нет FC / validate fail / нет engine → `offer_continue_seam` |
| Kind | `CONTINUE` + `EDIT` (**без Cancel** — так зашито в mint) |
| Нажатие | consume: reply «Continuing interview.» · actions=[] · **FSM state не меняет** · **не** stash · **не** новый engine turn в том же `/actions` |
| Смысл | Шов «черновик уже confirmed, но Send ещё нельзя» — дальше обычно новый **текст** (интервью); снова могут появиться Continue/Edit, пока нет валидного FC |

Cancel нет, чтобы не смешивать «мягкий resume» с terminal cancel confirm-потока (Cancel есть на interpretation/send bundles).

---

## 10. Edit и Cancel на двух подтверждениях

| Кнопка | Набор A (Looks right) | Набор B (Send) |
|--------|----------------------|----------------|
| **Edit** | → `interviewing`; invalidate tokens; clear freeze/draft_hash/URL | то же |
| **Cancel** | → `cancelled`; invalidate; clear draft fields | то же |

После Edit черновик-проза в истории модели **не** обязана стираться; сбрасывается **send permission / freeze**. Чтобы снова Looks right: нужен новый FC-less turn в `interviewing` → снова `offer_interpretation_confirm`. Да — **Looks right нужно нажать снова** на свежих кнопках.

---

## 11. Новый текст, пока ждём подтверждение

Пока `awaiting_interpretation_confirm`:

- текст идёт как обычный `/turns` → снова engine → STORY-71 remint Looks right/Edit/Cancel;  
- отдельного артефакта «версия черновика» до FC **нет** — смысл в **истории диалога** engine;  
- free-text **не** двигает FSM на Send (REQ-11);  
- Looks right относится к **текущей** сессии/истории на момент успешного consume + post-confirm engine turn (не к устаревшему сообщению с expired token).

Практично: правку текстом → дождаться **нового** сообщения с кнопками → Looks right на **нём**.

---

## 12. TTL и повторный выпуск кнопок

- TTL: `AIBRIDGE_ACTION_TOKEN_TTL_SECONDS=900` (15 мин).  
- Remint = **новые токены** на **новом** outbound; labels могут совпадать.  
- Старые клавиатуры под старыми сообщениями: callback с тем же raw token → после TTL **409 Token expired** (Observed 11.11).  
- Действующая кнопка: на **самом свежем** сообщении с remint; или любой короткий текст → remint → жать в течение TTL.

---

## 13. Что сохраняется после Send?

| Слой | Что |
|------|-----|
| Freeze до Send | `frozen_tool_intent` = имя + call_id + **assembled arguments** (после three gates) + `draft_hash` |
| После Send OK | gateway stash → `draft_id` + `continuation_url`; FSM → `stashed` (типично) |
| Проза Looks right | не отдельный stash-документ; FC payload связан с `draft_hash` версии freeze |

Ошибка gateway: outcome `failed` / `unknown_outcome` и т.п.; Send может блокироваться на revision. Повторный Send: нужен валидный **новый** `CONFIRM_SEND` token при send-ready state + freeze; не «та же протухшая кнопка».

---

## 14. Финальный submit в SPA

`continuation_url` = `{SPA}/#/story/submit?draft_id=…` (`build_continuation_url`).

| Уже есть после Send | Ещё в браузере |
|---------------------|----------------|
| Stash draft на gateway (`draft_id`) — **Story ещё нет** | Login / OTP → preview → **citizen submit** |

**Точное имя шага (см. §21):** `POST /story-drafts/{draft_id}/submit` → gateway **intake Story** (202 + `story_id`) + author из identity `/me` + очередь clustering; UI статус часто `under_review`. Это **не** мгновенный `PUBLISHED` Issue на борде и **не** «только привязать draft».

---

## 15. Что должна показывать учебная схема?

**Рекомендация для гелевой схемы:**

1. **Жирным / сплошным** — live-путь, который **пройден или чётко Observed** 11.11: текст → remint Confirm-кнопок (STORY-71) · Looks right → token path (в т.ч. **409 expired** как реальный тупик).  
2. **Пунктиром / пометкой «Present в коде / harness»** — STORY-72 post-confirm → Validate/FC → Send → stash → SPA (тесты `test_story_72_…`; **live E2E до stash 11.11 не закрыт**).  
3. **Пунктиром «роли pack»** — extractor/checker/normalizer при смене `phase` (код Present; live auto-chain Absent).

| Ветка | 11.11 |
|-------|-------|
| Remint Looks right/Edit/Cancel в TG | **Live Observed** |
| Looks right → FSM advance → Send | **Blocked** 409 expired |
| Post-confirm FC + Send + stash + SPA | **Code/harness Present** · live E2E Open |
| Role theater prose | Live Observed (искажение) |
| ROL-07 obedience live | Open (pack upload / model) |

---

## Легенда цветов для следующей визуализации

| Цвет (предложение) | Класс |
|--------------------|-------|
| Человек | text / Looks right / Edit / Cancel / Continue / Send / SPA submit |
| Модель | InterviewEngine reply + optional `postStoryDraftStash` FC |
| Сервер aibridge | FSM, mint tokens, validate/gates, freeze, remint |
| Сохранение | gateway stash + `draft_id` / URL (только после Send) |

Не смешивать: **проза модели** ≠ **mint кнопок** ≠ **HTTP stash**.

---

## Round 2 — подтверждение, payload, сила кнопок (Q16–21)

### 16. Confirm после любого текстового ответа без FC?

**Да — это фактическое текущее поведение**, не отдельный «draft ready» detector.

Условие в коде (`seam_policy` + `build_turn_from_engine`):

- Confirm FSM = `INTERVIEWING`
- engine вернул **пустой** `function_calls`
- → `offer_interpretation_confirm` → Looks right / Edit / Cancel

Дополнительного условия «черновик заполнен / gaps закрыты / phase=normalize» **нет**. Значит Looks right может появиться уже после первого уточняющего вопроса, если модель не эмитит FC.

Исключения на входе (другие gates): language-pick и т.п. — не «готовность черновика».  
Пока state уже `awaiting_interpretation_confirm`, тот же набор **remint**’ится (STORY-71), даже без hop.

**Для схемы:** человек кнопкой Looks right подтверждает не «серверно верифицированный draft artifact», а **интерпретационный шов** FSM; сервер затем сам просит модель выдать FC.

---

### 17. Есть ли проверка смысла подтверждённого текста vs payload?

**Нет отдельной semantic-fidelity проверки Present.**

| Что есть | Что делает |
|----------|------------|
| Gates 1–3 + allowlist FC | структура / schema / wire assembly / `draft_hash` тела |
| `draft_hash` | хэш **уже собранного** body после gates — целостность freeze↔Send, не «проза = факты» |
| История engine | модель *может* опираться на диалог; сервер это **не** сверяет с confirmed prose |

`SemanticStateService` умеет `upsert_confirmed_fact` / `add_correction` → `invalidate_send_permission`, но ordinary TG text turn через `channel_wire` **не** пишет confirmed facts автоматически и **не** сравнивает FC с текстом Looks right.

**Риск для визуализации:** человек одобряет *прозу*; Send уносит *frozen FC arguments*. Связь — trust модели + prompt post-confirm, не cryptographic/semantic proof.

---

### 18. Новый текст, когда уже видна Send?

`process_turn` **не** вызывает `invalidate_send_permission` на каждый текст.

Пока FSM = `awaiting_send_confirm` и `frozen_tool_intent` жив:

| Событие | Freeze / Send permission |
|---------|--------------------------|
| Free-text turn (обычный) | **Сохраняются** |
| FC-less + Send-claim markers / empty actions | remint **того же** Send (тот же freeze) — harness STORY-70 |
| Edit / Cancel | Edit → clear freeze + bump revision; Cancel → cancelled |
| `SemanticStateService` meaning write (fact/correction / phase rights) | clear freeze — **если** такой write реально вызван |

**Да:** модель может ответить новым текстом, а **старая** (ещё PENDING, не expired, тот же `revision` + `draft_hash`) кнопка Send отправит **ранее замороженные** arguments. Remint новых Send-токенов сам по себе freeze не обновляет.

Сброс силы Send = Edit / Cancel / meaning-invalidate / успешный/провальный Send path / TTL/invalidation токена — не «любой текст».

---

### 19. Remint аннулирует старые кнопки или действует до TTL?

**Remint сам по себе предыдущие PENDING-токены не аннулирует.**

| Операция | Revision | Старые PENDING |
|----------|----------|----------------|
| `_mint_bundle` / remint Looks right или Send | **не** bump | остаются PENDING до TTL / явной invalidate |
| `consume` (Looks right / Continue / Send / …) | обычно без bump; `invalidate_session_revision(session, revision=current)` | PENDING этой revision → INVALIDATED |
| `invalidate_send_permission` (Edit, meaning) | **bump** `revision += 1` + invalidate old revision | старые токены той revision мертвы; consume со старым revision → **409** revision mismatch |
| Cancel | invalidate (без того же send-clear пакета, что Edit) | старые мертвы; state `cancelled` |

Проверки на consume: ownership · TTL · PENDING · `rec.revision == sess.revision` · `expected_state == sess.state` · для Send ещё deployment + `draft_hash`.

**После текстовой правки без Edit:** Looks right под **предыдущим** сообщением может **успешно** подтвердить, если токен ещё PENDING, не expired, revision/state совпали — и post-confirm увидит **текущую** историю engine (включая новый текст). Это не «подтверждение старого пузыря как снимка», а consume текущего session state.

**Практика оператора:** жать только свежайшее сообщение; старые клавиатуры считать опасными до TTL.

---

### 20. Защита post-confirm от правки/отмены во время ожидания модели?

Цепочка **by design вне** `turn_lock` (G-02: lock не держать на engine/HTTPS).

После успешного Looks right consume (под lock):

1. tokens текущей revision **invalidated** → старые Edit/Cancel/Looks right этой revision уже не consume’ятся;  
2. `actions=[]` до конца post-confirm ответа — новых Edit на этом HTTP ещё нет;  
3. engine+validate+freeze идут **без** lock.

| Конкурент | Защита Present? |
|-----------|-----------------|
| Повтор Looks right / Edit со **старых** токенов той revision | Да — INVALIDATED / 409 |
| Free-text `/turns` во время engine | `turn_lock` сериализует turns **друг с другом**, но post-confirm engine **не** под тем же hold → возможен overlap с текстом; **нет** явного re-check «state всё ещё interpretation_confirmed / Edit не было» перед `persist_pending_tool` |
| Edit/Cancel **после** появления новых кнопок Send/Continue | Обычный consume — clear / cancel |

**Итог для схемы:** от «двойного Looks right» защищены invalidated tokens; от «текст/правка во время медленного post-confirm» полной state-revalidation перед freeze в коде **не видно** — честно помечать как gap/risk, не как закрытый lock.

---

### 21. Как точно назвать последний шаг в SPA?

**Короткое имя на схеме:** *Citizen submit → Story intake (202)*  
**Не:** «только bind draft» · **Не:** «мгновенный publish Issue на борд».

| Шаг | Факт (код/API) |
|-----|----------------|
| Send в TG | stash `POST /story-drafts` → `draft_id` + URL; **Story не создана** |
| SPA `#/story/submit?draft_id=` | preview draft · login/OTP gate |
| Кнопка submit | `POST /story-drafts/{id}/submit` → `handle_story_intake` / `create_story` → **202** + `story_id`; draft удаляется; author из `/me` |
| Сразу после | Story в пайплайне; clustering deferred; cabinet часто **`under_review`** |
| Позже | Issue projection / `PUBLISHED` на фиде — **отдельный** этап, не этот endpoint |

Файлы: `spa-app/src/pages/StorySubmitPage.jsx` · `storyDraftService.submitStoryDraft` · gateway `API_REFERENCE.md` §`POST /story-drafts/{draft_id}/submit`.

---

## Сводка для визуализации (что подтверждает человек)

| Кнопка | Что реально подтверждает | Что уходит дальше |
|--------|--------------------------|-------------------|
| Looks right | FSM-шов «интерпретация ок» | затем **новый** model turn → возможный FC |
| Send | «отправить **frozen** payload» | gateway stash тела freeze |
| SPA submit | «создать Story из stash от моего `/me`» | intake 202 + under_review pipeline |

Когда подтверждение **теряет силу:** TTL 900s · invalidate после consume · Edit/meaning bump revision · Cancel · (для Send) hash/deployment mismatch.

---

## Related

- Roles / soft conversation Q&A: [`req15-roles-soft-conversation-qna-2026-11-11.md`](./req15-roles-soft-conversation-qna-2026-11-11.md)  
- Training SSOT: [`req15-operator-pipe-and-buttons-training-2026-11-11.md`](./req15-operator-pipe-and-buttons-training-2026-11-11.md)  
- 409 note: [`req15-tg-interview-2026-11-11-looks-right-token-expired-log-note.md`](./req15-tg-interview-2026-11-11-looks-right-token-expired-log-note.md)  
- Buttons Present: [`req15-tg-interview-2026-11-11-buttons-present-log-note.md`](./req15-tg-interview-2026-11-11-buttons-present-log-note.md)  
- Validate 71/72/ROL-07: [`req15-story-71-72-rol07-code-validation-test-2026-11-11.md`](./req15-story-71-72-rol07-code-validation-test-2026-11-11.md)  
- Target UX SPA: [`req15-tg-interviewer-target-ux-2026-11-06.md`](./req15-tg-interviewer-target-ux-2026-11-06.md) §5  
- Runtime 72: [`../../doge-ai-bridge/docs/runtime-docs/19-send-after-draft-confirm-validate.md`](../../doge-ai-bridge/docs/runtime-docs/19-send-after-draft-confirm-validate.md)  
- L11 invalidate: [`../../doge-ai-bridge/docs/runtime-docs/05-l11-invalidation-seam.md`](../../doge-ai-bridge/docs/runtime-docs/05-l11-invalidation-seam.md)  
- Gateway submit API: [`../../doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md`](../../doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md) §`POST /story-drafts/{draft_id}/submit`  
- SPA page: [`../../spa-app/src/pages/StorySubmitPage.jsx`](../../spa-app/src/pages/StorySubmitPage.jsx)
