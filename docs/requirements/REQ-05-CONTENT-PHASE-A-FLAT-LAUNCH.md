# REQ-05: Content Phase A — flat launch (полный flat dump)

**Index key:** REQ-05  
**Service / repo:** `doge-ai-bridge`  
**Parent:** [REQ-01](./REQ-01-doge-ai-bridge-runtime.md)  
**Related:** [REQ-03](./REQ-03-RUNTIME-REMEDIATION-AGREED.md) · [REQ-04](./REQ-04-RUNTIME-SAFETY-AND-CONFIRMATION-HARDENING.md) (content→engine как prerequisite) · [REQ-06](./REQ-06-CONTENT-PHASE-B-SCALABLE-PACKAGING.md) (следующая фаза)  
**Related analysis:** [module1-instructions-custom-gpt-to-aibridge-organization-2026-09-16.md](../analysis/module1-instructions-custom-gpt-to-aibridge-organization-2026-09-16.md)  
**Related architecture:** [02-content-packaging.md](../architecture/runtime/02-content-packaging.md) · [GPT UI 05-python-bridge-instruction-delivery.md](../../../GPT%20UI/docs/architecture/05-python-bridge-instruction-delivery.md)  
**Status:** Ready for implementation  
**Version:** 0.2.0 · 2026-09-16  
**Phase:** A — flat dump **полной** комплектации из `src/instructions/` + wire OAS из `docs/openapi/`; без multi-repo CI  

**Operator decisions (2026-09-16):**

1. Manifest пишется **in-place** в `src/instructions/instructions.manifest.json` (текущий 6-file — черновик).  
2. Phase A = **полное** воспроизведение загруженного набора (не subset / не «pilot-chain only»).  
3. Prompt channel = **stable prefix** (`prompt_channel=prefix`); не `instructions=` API.

---

## 1. Цель

На уже предоставленном flat-материале получить **работающую** доставку в OpenAI Responses текста и схем **той же полноты**, что лежит в репозитории для Phase A:

- всё содержимое [`src/instructions/`](../../src/instructions/) (кроме самого файла манифеста);
- Story Intake wire OAS из [`docs/openapi/`](../openapi/) в runtime image и в `DOGESTONIA_OPENAPI_PATH`.

«Лайтовость» Phase A — только в **архитектуре доставки** (один flat dir, один manifest v1, текущий loader, без CI multi-repo, без layered schema).  
**Не** в урезании Module-1 / pack v3 набора: subset ломает parity с Custom GPT Knowledge и даёт ложное «готово».

Итог: `content_configured()` + non-empty **полный** assembled text в stable prefix + strict tool + OAS в image.

REQ-05 **не** заменяет REQ-01/03/04 и **не** меняет channel OpenAPI v1 контракт.

---

## 2. Scope

### Входит

1. Wiring: `assembled_instructions` (+ strict tool из deploy) → `InterviewEngine` через **stable prefix** (`prompt_channel=prefix`; XOR с `instructions=` соблюдён — второй карман пуст).
2. Manifest **полной комплектации** in-place: `src/instructions/instructions.manifest.json`  
   - `files[]` перечисляет **каждый** root-child артефакт в `src/instructions/`, кроме `instructions.manifest.json` самого;  
   - включая все Module-1 `.md` и все `schema-packs.uus_veerenni_civic.v3.*` (md + json) + `schema-packs.README.md`;  
   - порядок — **архитектурно заданный** (см. §4.2), не `ls` наугад.
3. Env pins (local + Railway) в `.env.example` / web runbook — без новых alias.
4. `docs/openapi/` доступен в runtime image: как минимум Story Intake wire для `DOGESTONIA_OPENAPI_PATH`; channel OAS (`aibridge-channel-v1.openapi.yaml`) **копируется вместе с каталогом** (не терять артефакт деплоя), но **не** входит в `files[]` манифеста инструкций (другой контракт — n8n↔bridge).
5. Automated proof + короткий smoke checklist.

### Не входит

- Multi-repo sync из `GPT UI/instructions/` ([REQ-06](./REQ-06-CONTENT-PHASE-B-SCALABLE-PACKAGING.md)).
- Layered manifest schema; nested paths в loader.
- Урезанные prompt-profiles (`pilot-minimal` и т.п.) — это Phase B; Phase A = полный набор.
- Node package tree / object storage / Pack Builder.
- Смена семантики channel или Story Intake API.
- Стратегия thin-prompt / отказ от Module-1 текста.
- Реализация Phase B.

**Name ≠ create:** полный `files[]` и Dockerfile COPY — acceptance targets implementation wave.

---

## 3. Verified current state (as-of 2026-09-16)

| Факт | Evidence |
|------|----------|
| Loader: manifest `bundle_version` + `files[]` (root children only), join `\n\n`, hashes, register-once | `src/aibridge/content.py`, `deployment.py` |
| `content_configured()` требует commit + dir + manifest + openapi + payload | `src/aibridge/config.py` |
| Flat dump в `src/instructions/`; manifest сейчас **6-file subset** (неполный) | `src/instructions/instructions.manifest.json` |
| **Gap:** `InterviewEngine` без assembled text; default `prompt_channel=prefix`, `instructions=""` | `src/aibridge/app.py` (~290–298); `interview.py` (~42–50); GPT UI `05` §5 |
| Engine создаётся **до** `_init_stores`/deployment | `src/aibridge/app.py` (~287–300 vs ~383–392) |
| Dockerfile: `src/` + `migrations/`; `docs/openapi/` **не** в image | root `Dockerfile` |
| OpenAPI in-repo | `docs/openapi/story-intake-actions.openapi.yaml`, `docs/openapi/aibridge-channel-v1.openapi.yaml` |
| Active pack | `uus_veerenni_civic` / `v3` flat files under `src/instructions/` |

---

## 4. Acceptance criteria

REQ-05 Done только когда:

### 4.1 Wiring (stable prefix)

При успешном `verify_and_register_deployment`:

- `InterviewEngine.prompt_channel == "prefix"`;
- non-empty `assembled_instructions` участвует в stable prefix (через `engine.instructions` → `build_stable_prefix`, как уже устроено при `prompt_channel=prefix`);
- Responses payload **не** дублирует тот же текст в `instructions=`;
- `DeploymentBundleState.strict_tool` (при `SCHEMA_ID`+`SCHEMA_VERSION`) доступен interview path (`engine.tools` или эквивалент).

### 4.2 Manifest полной комплектации + порядок

`DOGESTONIA_INSTRUCTIONS_MANIFEST` → `src/instructions/instructions.manifest.json`.

**Полнота:** каждый файл в `src/instructions/` кроме `instructions.manifest.json` входит в `files[]` ровно один раз.  
Пропущенный файл = **FAIL** Phase A (не «опциональный later»).

**Порядок (архитектура слоёв; внутри слоя — стабильный явный список в manifest):**

```text
1) Wrappers
   root.md → bootstrap.md → base.md → communication-presets-reference.md

2) Navigation / model map
   instruction-modules-index.md → story-data-model.md → story-label-taxonomy.md

3) Interview / i18n / lifecycle
   story-interview-flow.md → story-i18n-policy.md → story-lifecycle-instructions.md

4) Strict chain (без HTTP)
   ingest-validation.md → ingest-deep-parsing.md → safety-compliance.md
   → story-policy-gate.md → story-normalizer.md

5) HTTP / wire companion (текст)
   api-orchestrator.md → story-api-methods-reference.md

6) Active pack uus_veerenni_civic / v3 (все flat артефакты пака + README)
   schema-packs.README.md
   → schema-packs.uus_veerenni_civic.v3.interview-overlay.md
   → schema-packs.uus_veerenni_civic.v3.inbound-validation.md
   → schema-packs.uus_veerenni_civic.v3.locale-jurisdiction.md
   → schema-packs.uus_veerenni_civic.v3.pack.json
   → schema-packs.uus_veerenni_civic.v3.payload.schema.json
   → schema-packs.uus_veerenni_civic.v3.taxonomy.json

7) Legacy / inventory (если файл присутствует в dir — обязателен в manifest)
   activity-legacy-paths-inventory.md
```

Если после даты REQ в каталог добавят новый root-child — Phase A implementation обязан включить его в подходящий слой (или новый хвостовой слой) **до** Done; молчаливый omit запрещён.

JSON пака **входят** в `files[]` (в промпт как Knowledge, parity с Custom GPT upload).  
Параллельно `DOGESTONIA_PAYLOAD_SCHEMA_PATH` указывает на тот же `schema-packs.uus_veerenni_civic.v3.payload.schema.json` для tool_gen / `pack_hash` (двойная роль: текст в assembly + path для генератора — допустимо).

### 4.3 Env

Задокументированы непустые:

- `DOGESTONIA_INSTRUCTIONS_DIR=src/instructions` (local; в image — путь внутри контейнера)
- `DOGESTONIA_INSTRUCTIONS_MANIFEST=src/instructions/instructions.manifest.json`
- `DOGESTONIA_CONTENT_SOURCE_COMMIT`
- `DOGESTONIA_OPENAPI_PATH` → Story Intake wire (`…/story-intake-actions.openapi.yaml`)
- `DOGESTONIA_PAYLOAD_SCHEMA_PATH` → `…/schema-packs.uus_veerenni_civic.v3.payload.schema.json`
- `DOGESTONIA_SCHEMA_ID=uus_veerenni_civic`
- `DOGESTONIA_SCHEMA_VERSION=v3`
- `DOGESTONIA_TOOL_SCHEMA_PATH` может быть пустым

### 4.4 OpenAPI в image

- Image содержит содержимое `docs/openapi/` (оба YAML), без ручного mount.
- `DOGESTONIA_OPENAPI_PATH` резолвится на **Story Intake** wire (не channel façade).
- Channel OAS остаётся артефактом репо/image для façade; в instruction `files[]` не попадает.

### 4.5 Proof

- Test: content_configured + loaded full manifest → prefix/engine несёт non-empty assembled text; при необходимости — assembled покрывает обязательные basenames из §4.2.
- Missing/broken path → readiness fail-closed (не silent empty prompt).
- Smoke: `/healthz` 200; полный env → `/readyz` не `content_bundle_not_ready` из‑за OAS/manifest/wiring.

### 4.6

Phase B **не** требуется для Done Phase A.

---

## 5. Work items (implementation wave)

| ID | Доработка | Зачем |
|----|-----------|--------|
| R5-A-01 | Wire assembled → **stable prefix**; tools из `strict_tool`; fix create_app order vs deployment | GPT UI `05` §5 |
| R5-A-02 | Full `instructions.manifest.json` (§4.2 completeness + layer order) | Parity с загруженным набором |
| R5-A-03 | Dockerfile: `COPY docs/openapi` (или эквивалент) | OAS в image |
| R5-A-04 | `.env.example` + web runbook: Phase A pins | Ops |
| R5-A-05 | Tests + smoke checklist (полнота + wiring) | Доказательство |

---

## 6. Non-goals / out of Done

- Авто sync `GPT UI` → bridge.
- Manifest v2 / layered / nested loader.
- **Урезание** набора «чтобы быстрее зелёный /readyz» или дешевле токены — запрещено в Phase A; экономия токенов = [REQ-06](./REQ-06-CONTENT-PHASE-B-SCALABLE-PACKAGING.md) profiles поверх полного дерева.
- Изменение REQ-01 body; federation (REQ-02).

---

## 7. Version log

- v0.2.0 — 2026-09-16: operator — full dump (not subset); in-place manifest; stable prefix only; pack JSON in `files[]`; openapi dir in image; layer order §4.2.
- v0.1.0 — 2026-09-16: initial Phase A (subset `pilot-chain`) — **superseded** by v0.2.0 completeness rule.
