# Черновой анализ: Module-1 инструкции (Custom GPT) → организация в doge-ai-bridge

**Зона:** `doge-ai-bridge/docs/analysis/`  
**As-of:** 2026-09-16  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc)  
**Статус:** черновик / options analysis — **без реализации**  
**Источники (прочитаны):**

| Источник | Path |
|----------|------|
| GPT UI architecture map | `GPT UI/docs/architecture/README.md` + `00`…`05` |
| Module-1 SSOT (claimed) | `GPT UI/instructions/` |
| Bridge content packaging | `doge-ai-bridge/docs/architecture/runtime/02-content-packaging.md` |
| Bridge loader / deploy | `src/aibridge/content.py`, `deployment.py`, `config.py`, `app.py`, `interview.py` |
| Local dump (operator) | `doge-ai-bridge/src/instructions/` + `instructions.manifest.json` |
| Scaling notes | `docs/analysis/ARCH-RECOMMENDATIONS-REQ-01-PILOT-AND-NODE-SCALING.md` |

---

## 1. Как я это понял (Custom GPT контекст)

### 1.1 Два канала, один wire

Из [`00-two-channels-overview.md`](../../../GPT%20UI/docs/architecture/00-two-channels-overview.md):

- **Продукт один:** `POST /story-drafts` (`postStoryDraftStash`) → `draft_id` → SPA submit.
- **Транспорт tool call разный:**
  - **A — Custom GPT Actions:** модель в ChatGPT; HTTP к gateway исполняет платформа Actions по импортированному OpenAPI.
  - **B — doge-ai-bridge:** Telegram/n8n → Python → OpenAI **Responses**; HTTP к gateway исполняет приложение (Bearer + allowlisted tool loop).

Поведенческий текст интервью задуман общим: `GPT UI/instructions/` + active schema pack. Канал B **не** заменяет Actions.

### 1.2 Слои Module-1 (как задумывалось под Knowledge upload)

Из [`01-module1-instruction-layers.md`](../../../GPT%20UI/docs/architecture/01-module1-instruction-layers.md) + index:

| Слой | Файлы | Роль |
|------|--------|------|
| Wrappers | `root.md` → `bootstrap.md` → `base.md` | Identity, `comm_context`, constitution |
| Navigation | `instruction-modules-index.md` | Карта runtime path |
| Interview / i18n / lifecycle | `story-interview-flow.md`, `story-i18n-policy.md`, `story-lifecycle-instructions.md`, … | Диалог и handoff |
| Strict chain (без HTTP) | `ingest-validation` → `safety-compliance` → `story-policy-gate` → `story-normalizer` | Артефакты до stash |
| HTTP only | `api-orchestrator.md` (+ `story-api-methods-reference.md`) | Единственный модуль с Actions/HTTP |
| Node overlay | flat `schema-packs.<id>.<ver>.*` ×6 + `schema-packs.README.md` | Active pack |

**Обязательная цепочка** (index):  
`ingest-validation → safety-compliance → story-policy-gate → story-normalizer → api-orchestrator`  
с `base.md` как constitution и lifecycle как reference.

**Init order** ([`03`](../../../GPT%20UI/docs/architecture/03-init-and-runtime-order.md)): root → bootstrap (`comm_context`) → base → interview + chain. Без bootstrap ломаются language/tone контракты.

**Upload constraint Custom GPT:** субдиректории отбрасываются → live SSOT pack = **flat** имена (`schema-packs.uus_veerenni_civic.v3.*`). Nested gateway path остаётся executable SSOT на gateway, не на GPT upload.

### 1.3 Pack vs core

Из [`02-schema-packs-and-binding.md`](../../../GPT%20UI/docs/architecture/02-schema-packs-and-binding.md):

- **Core** = shared process (фазы, STOP, envelope mapping).
- **Pack** = node model (signals, taxonomy, inbound lists, locale) — swappable.
- GPT **не** валидирует pack JSON (SEC-001); авторитет — gateway Schema Runtime.
- Active pair as-built: `uus_veerenni_civic` / `v3` (six flat files).
- Wire: root `schema_binding`; envelope `schema_version` = `m2.story_intake_envelope.v2` ≠ pack `v3`.
- Для Responses strict tool bridge подменяет model-facing schema активным `payload.schema.json` (wire OAS часто `additionalProperties: true`).

### 1.4 Как Custom GPT «организовывал» контент vs bridge

| Concern | Custom GPT (A) | Bridge (B) as designed |
|---------|----------------|------------------------|
| Delivery | Knowledge upload + Configure Instructions | Local files + `DOGESTONIA_INSTRUCTIONS_*` + manifest |
| Order of files | Runtime order documented; **upload sort-key Unknown** в репо | Manifest `files[]` order = assembly order (`\n\n`) |
| Full Knowledge set | Большой flat набор Module-1 + pack overlays | Manifest **subset** допустим и уже так используется |
| Tool schema | Actions import YAML as-is | Generated/allowlisted strict tool; app owns execution |
| OAS | Import `custom-gpt-story-intake-actions.openapi.yaml` | `DOGESTONIA_OPENAPI_PATH` (часто копия в bridge `docs/openapi/`) |
| Confirm | Actions consequential + chat | Dual confirm / n8n (отдельный слой) |

### 1.5 Verified gaps (уже зафиксированы в GPT UI `05` + коде)

1. **SSOT ownership:** claimed = `GPT UI/instructions/`; physical copy в bridge = `doge-ai-bridge/src/instructions/`. **Скрипт sync GPT UI → aibridge в репо aibridge не найден** (`05` §1) → Unknown / ops manual copy.
2. **Assembled ≠ engine:** `load_content_bundle` строит `assembled_instructions` и registry hashes; `create_app` создаёт `InterviewEngine` **без** `instructions=` (`app.py` ~L290–298; default `""` в `interview.py`). Документировано в `05` §5 как **Verified gap**, не как «уже работает E2E prompt».
3. **Dockerfile:** копирует `src/` + `migrations/`; `docs/openapi/` **не** в image по умолчанию — OAS для Railway нужно явно упаковать или положить под `src/`.
4. **Index drift:** index всё ещё упоминает `tallinn_civic`/`v1` и nested `schema-packs/README.md`; live = `uus_veerenni_civic`/`v3` + flat README (`01` §4).
5. Текущий local manifest — **узкий subset** (6 файлов), не full Module-1 chain (нет ingest/gate/normalizer/orchestrator и большинства pack md в prompt).

Сравнение деревьев (as-of 2026-09-16, только top-level names): ~25 общих имён; в GPT UI ещё archive / node-onboarding / старые pack versions / tallinn; в bridge — `instructions.manifest.json`, без archive/onboarding.

---

## 2. Что уже умеет aibridge (якорь для опций)

Уже есть и должно остаться опорой:

```text
env pins → load_content_bundle (manifest files only, root children)
        → hashes + register-once (Postgres content_bundle)
        → session pin content_bundle_hash
        → /readyz fail-closed
        → (planned) InterviewEngine.instructions / stable prefix
        → generate_strict_tool(OAS + payload + schema_id/version)
```

Ограничения loader (`content.py`):

- `files[]` — только имена в корне `INSTRUCTIONS_DIR` (без `/`);
- порядок списка = порядок склейки;
- payload schema path и openapi path — **отдельные** env, не обязаны лежать в manifest;
- tool schema path optional; при `SCHEMA_ID`+`VERSION` tool_gen на deploy/readyz.

Масштабирование нод (из packaging + ARCH notes): один image/код; новая нода = новый verified bundle + env/secrets; без `if node == …` в Python; in-flight sessions pinned to old `bundle_hash`.

---

## 3. Варианты организации контента в aibridge

Критерии: fidelity Module-1; масштаб нод; ops/CI; token/cost; churn loader; dual-channel parity.

---

### Option A — Flat dump + curated manifest (status quo+)

**Идея:** плоская куча в `src/instructions/` (как Custom GPT upload). Manifest явно перечисляет subset для Responses. Pack identity через `SCHEMA_*` + `PAYLOAD_SCHEMA_PATH`. OAS отдельно.

**Плюсы:** совпадает с flat constraint и текущим `content.py`; быстрый локальный старт; swap ноды ≈ six flat pack files + env + overlay в manifest.  
**Минусы:** смешение core/pack/meta; порядок только ручной; sync с GPT UI ручной; полный dump дорог, узкий subset — семантические дыры.  
**Масштаб:** ок для одной pilot-ноды; слабо для многих.

---

### Option B — Logical layout on disk + flat staging for runtime

**Идея:**

```text
content/
  core/module1/          # root, bootstrap, base, story-*, ingest-*, orchestrator, …
  packs/<schema_id>/<ver>/
  wire/story-intake.openapi.yaml
  manifests/
    uus_veerenni_civic.v3.json
```

CI stage → immutable tarball (flat names под текущий loader).

**Плюсы:** явный core vs pack; совпадает с `02-content-packaging.md`; node scale = новый pack + manifest.  
**Минусы:** нужен publish-шаг (сейчас нет); два представления logical vs runtime.  
**Масштаб:** лучший долгосрочный fit с packaging docs.

---

### Option C — Dual manifests: prompt profile vs hash constituents

**Идея:** (1) prompt manifest — что в `assembled_instructions`; (2) artifact set — payload/OAS/tool pin (часть уже через env). Manifest v2 или два файла / profiles.

**Плюсы:** честный token control; full Module-1 на диске, в Responses — pilot subset, потом расширение.  
**Минусы:** шире текущая схема манифеста; риск «файл есть, в prompt нет» без AC.  
**Масштаб:** хорошо для эволюции prompt quality.

---

### Option D — Layered assembly (typed layers)

**Идея:** манифест со слоями `wrappers` / `interview` / `chain` / `http` / `pack_overlay`; сборка в фиксированном порядке `01`/`03`.

**Плюсы:** максимальная fidelity; сложнее забыть bootstrap или переставить orchestrator.  
**Минусы:** breaking change формата; сам по себе не режет токены (нужны profiles).  
**Масштаб:** сильный выигрыш в качестве поведения модели.

---

### Option E — Nested paths in loader

**Идея:** разрешить `core/root.md`, `packs/…` в `files[]` (снять root-child-only).

**Плюсы:** диск = logical layout без rename.  
**Минусы:** расхождение с Custom GPT flat upload; path guards; больше churn.  
**Масштаб:** удобно monorepo; хуже dual-channel parity.

---

### Option F — GPT UI единственный file SSOT; bridge только pin + image layer

**Идея:** не владеть второй копией текста в bridge. CI: checkout GPT UI @ SHA → stage → image. В bridge — manifests/profiles + env examples.

**Плюсы:** один текстовый SSOT для A и B; git ≠ image; меньше drift двух куч.  
**Минусы:** multi-repo CI обязателен; локально нужен checkout/script; Dockerfile сегодня не готов.  
**Масштаб:** правильный ownership для многих нод.

---

### Option G — Thin bridge prompt + code-owned orchestration

**Идея:** короткий prefix (interview + pack overlay + safety); gate/normalize/stash усиливать в Python.

**Плюсы:** токены/latency; fail-closed уже частично в app.  
**Минусы:** дрейф от «тот же Module-1»; большой Python scope; слабая parity с каналом A.  
**Масштаб:** прагматично для Telegram cost; спорно как порт Custom GPT.

---

### Option H — Multi-profile content packages per node env

**Идея:** `nodes/<schema_id>/<ver>/` с profile.manifest + env fragment (+ ссылки на shared core/pack).

**Плюсы:** ops UX «пакет ноды»; сочетается с B/C/D.  
**Минусы:** ещё один слой каталогов; не заменяет engine wiring.  
**Масштаб:** лучший UX при многих нодах.

---

## 4. Сводная матрица

| Option | Fidelity Module-1 | Node scale | Ops/CI fit | Token control | Loader churn | Dual-channel parity |
|--------|-------------------|------------|------------|---------------|--------------|---------------------|
| A Flat+manifest | Medium | Weak–Med | Low friction now | Manual subset | None | Med (flat) |
| B Logical+stage | High | **High** | Needs CI | Via staged manifest | Low if stage→flat | High if from GPT UI |
| C Dual manifests | Med–High | High | Med | **High** | Med | Med |
| D Layered manifest | **Highest** | High | Med | Med (+profiles) | High | High |
| E Nested loader | High | High | Med | Med | High | Lower vs GPT flat |
| F GPT UI SSOT only | High | **High** | Needs multi-repo | Via manifests | Packaging | **Highest** |
| G Thin prompt+code | Low–Med | High | Med | **Highest** | Low–Med | Low |
| H Node packages | High | **Highest** UX | Needs discipline | Via profiles | Med | Depends |

Реалистичные комбинации: **F + B + C** или **F + D + C**; краткосрочно **A → C**.

---

## 5. Рекомендация

**Задача:** масштабируемый канал B с тем же wire и переносимым Module-1, без n8n-бизнеслогики и без request-time GitHub fetch.

### 5.1 Целевой контур

1. **Ownership:** Option **F** — SSOT текст в `GPT UI/instructions/`; в image — immutable staged bundle.  
2. **Publish:** Option **B** — logical core+packs → stage flat под текущий loader (без E пока).  
3. **Prompt control:** Option **C** — profiles (`pilot-minimal`, `full-chain`).  
4. **Order:** позже Option **D** (layered) после стабилизации profiles.  
5. **Не выбирать сейчас как единственную стратегию:** E; G без явного отказа от parity с Custom GPT.

### 5.2 Ближайший прагматичный путь (pilot)

Пока multi-repo CI нет:

1. Физически **Option A** (`src/instructions/` flat).  
2. Manifest’ы как **профили**, не «все md подряд».  
3. Черновик semantically honest порядка (`01`/`03`):

   ```text
   root → bootstrap → base
   → story-interview-flow (+ i18n/lifecycle по необходимости)
   → ingest-validation → safety-compliance → story-policy-gate → story-normalizer
   → api-orchestrator (+ story-api-methods-reference)
   → pack: interview-overlay, inbound-validation, locale-jurisdiction
   ```

   JSON pack/taxonomy в prompt не обязательны (hash через `PAYLOAD_SCHEMA_PATH` / tool_gen).

4. **Код-gap вне раскладки файлов:** `assembled_instructions` → `InterviewEngine` (`05` §5) — иначе организация файлов бесполезна для Responses.  
5. Railway: wire OAS в image (COPY или путь под `src/`).

### 5.3 Масштаб нод

| Меняется | Не меняется |
|----------|-------------|
| Pack six-file + `SCHEMA_*` + payload path | Python image / InterviewEngine |
| Manifest profile (overlay) | Channel OAS / n8n façade |
| `CONTENT_SOURCE_COMMIT` + bundle_hash | Gateway `postStoryDraftStash` |

### 5.4 Вне scope этого отчёта

Не создаёт манифесты/Dockerfile/sync/wiring. Не объявляет полный dump обязательным. Не утверждает, что 6-file manifest = complete Knowledge.

---

## 6. Открытые вопросы оператору

1. Пилот B: максимальная parity с Custom GPT Knowledge или достаточный subset + жёсткий Python?  
2. Multi-repo CI stage (F+B) в ближайшей волне или ещё N недель manual copy в `src/instructions/`?  
3. Сразу второй profile (`full-chain`) или сначала engine wiring на текущем subset?  
4. Taxonomy/inbound text в prompt или достаточно payload schema + tool_gen?

---

## 7. Evidence checklist

| Claim | Evidence |
|-------|----------|
| Two channels, one stash wire | GPT UI `00` |
| Layer / chain / init order | GPT UI `01`, `03`, index |
| Flat six-file pack | GPT UI `02`, `schema-packs.README.md` |
| Manifest assembly + hashes | `content.py`; GPT UI `05` |
| Engine instructions not wired | `app.py`; GPT UI `05` §5 |
| Packaging: git ≠ image | aibridge `02-content-packaging.md` |
| Dockerfile `src`+`migrations` only | root `Dockerfile` |
| Local subset manifest | `src/instructions/instructions.manifest.json` |

---

**Конец черновика.** Следующий шаг по запросу: выбрать option-combo → REQ/story или ops runbook.
