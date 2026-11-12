# REQ-06: Content Phase B — scalable packaging (без spaceship)

**Index key:** REQ-06  
**Service / repo:** `doge-ai-bridge`  
**Parent:** [REQ-01](./REQ-01-doge-ai-bridge-runtime.md)  
**Depends on:** [REQ-05](./REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) **Done** (engine уже потребляет `assembled_instructions`)  
**Related:** [REQ-03](./REQ-03-RUNTIME-REMEDIATION-AGREED.md) · [REQ-04](./REQ-04-RUNTIME-SAFETY-AND-CONFIRMATION-HARDENING.md)  
**Related analysis:** [module1-instructions-custom-gpt-to-aibridge-organization-2026-09-16.md](../analysis/module1-instructions-custom-gpt-to-aibridge-organization-2026-09-16.md) §5.1 (combo F+B+C)  
**Related architecture:** [02-content-packaging.md](../architecture/runtime/02-content-packaging.md) · [GPT UI 00–05](../../../GPT%20UI/docs/architecture/README.md) · [GPT UI 05](../../../GPT%20UI/docs/architecture/05-python-bridge-instruction-delivery.md)  
**Status:** Draft — after REQ-05  
**Version:** 0.1.0 · 2026-09-16  
**Phase:** B — ownership + minimal publish + prompt profiles; anti-overbuild

---

## 1. Цель

После Phase A зафиксировать **масштабируемую** организацию контента для канала B:

1. один текстовый SSOT с Custom GPT (`GPT UI/instructions/` + active pack);
2. immutable stage в image (git ownership ≠ runtime packaging);
3. два prompt-profile над одним деревом файлов;
4. смена ноды без Python branch.

Без типичного overbuild: без nested loader, без обязательного layered manifest, без object-storage/federation/Pack Builder platform.

REQ-06 **не** меняет channel OpenAPI v1 и **не** дублирует Module-1 semantics в новый Python DSL.

---

## 2. Зафиксированный architectural combo

| Option (analysis) | Роль в Phase B |
|-------------------|----------------|
| **F** GPT UI text SSOT | Ownership инструкций |
| **B** Logical/source → flat stage | Publish в image под текущий loader |
| **C** Dual/prompt profiles | Token control + эволюция prompt |

**Явно не в Done Phase B:**

| Option | Статус |
|--------|--------|
| **E** nested paths в `content.py` | Out of scope |
| **D** layered manifest schema | Optional follow-up **после** стабильных profiles; не blocker Done |
| **G** thin prompt only | Не единственная стратегия (parity с Module-1 сохраняется через profiles) |

---

## 3. Scope

### Входит

1. **SSOT:** claimed + operational source of truth текста = `GPT UI/instructions/` (+ active pack six-file set). `doge-ai-bridge/src/instructions/` **перестаёт** быть ownership SSOT (допустим staged/vendored snapshot с явной пометкой generated / manual-until-CI).
2. **Minimal publish:** pin commit SHA(s) → stage flat tree + profile manifest(s) → Docker/image layer — согласовано с [02-content-packaging.md](../architecture/runtime/02-content-packaging.md). **No** GitHub/network fetch at request time (`content.py` / AIB-INS-04).
3. **Profiles** (два манифеста, формат v1 `bundle_version` + `files[]`):

   | Profile id | Назначение |
   |------------|------------|
   | `full-set` | Паритет с [REQ-05](./REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2+ — **полный** flat набор (baseline после Phase A) |
   | `pilot-minimal` | Осознанный **урезающий** profile для дешёвого smoke — только Phase B; не подменяет Phase A Done |

   Выбор профиля = path в `DOGESTONIA_INSTRUCTIONS_MANIFEST`. Оба читают **одно** staged flat дерево. Phase A не вводит `pilot-minimal`.

4. **Node scale:** новая нода = active pack six-file + `DOGESTONIA_SCHEMA_ID` / `DOGESTONIA_SCHEMA_VERSION` + `DOGESTONIA_PAYLOAD_SCHEMA_PATH` + profile overlay entries — **без** `if node == …` в Python.
5. **Registry:** session `content_bundle_hash` pin и register-once / GC contract без регрессии относительно REQ-01 packaging.

### Не входит (anti-spaceship)

- Nested path support в loader (Option E).
- Layered manifest как обязательный deliverable (Option D).
- Object storage для payloads; Identity / federation (REQ-02).
- Redesign Responses client / channel façade.
- Auto-promote content merge → production.
- Pack Builder / `node-onboarding/` tooling как часть bridge runtime.
- Новый Python DSL, дублирующий Module-1 chain.
- Переписывание `content.py` hash model.

**Name ≠ create:** CI scripts, stage dirs, profile JSON paths — acceptance targets; этот документ их не материализует.

---

## 4. Verified current state (pre-Phase B)

| Факт | Evidence |
|------|----------|
| Dual-channel claim: SSOT `GPT UI/instructions/` | GPT UI architecture `00`, `05` |
| Bridge physical copy / manual dump; sync script **Unknown** | GPT UI `05` §1; analysis 2026-09-16 |
| Flat loader + Postgres bundle registry | `content.py`, `registry.py`, packaging `02` |
| Phase A gap wiring / OAS-in-image | закрываются [REQ-05](./REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md); Phase B **не стартует** до REQ-05 Done |

---

## 5. Acceptance criteria

REQ-06 Done только когда:

1. **Prerequisite:** REQ-05 Done (engine получает assembled text).

2. **Ownership documented + operable:** операторский путь «изменил текст в `GPT UI/instructions/` → pin commit → stage → redeploy» описан; bridge `src/instructions/` не описан как long-term SSOT.

3. **Publish exists (minimal):** воспроизводимый шаг (CI job **или** checked-in script + documented manual) собирает flat tree + оба profile manifests из pinned GPT UI (и wire OAS / payload paths) в layout, читаемый текущим `load_content_bundle` (root children only). Request-time fetch отсутствует.

4. **Profiles:** оба файла `full-set` и `pilot-minimal` существуют в staged layout; переключение меняет `instructions_hash` / `bundle_hash` предсказуемо; env pin указывает на один выбранный manifest.

5. **Node scale proof (docs + dry checklist):** процедура смены pack pair (six flat files + env) без изменения Python; in-flight sessions остаются на старом `bundle_hash` (существующий contract).

6. **No spaceship regression:** loader по-прежнему root-child-only; нет обязательного layered schema; нет object-storage dependency для Done.

---

## 6. Work items (implementation wave)

| ID | Доработка | Зачем |
|----|-----------|--------|
| R6-B-01 | Зафиксировать ownership + de-SSOT bridge dump | Dual-channel parity |
| R6-B-02 | Minimal stage/publish (script and/or CI) → flat + OAS + payload | packaging `02` |
| R6-B-03 | Manifests `full-set` + `pilot-minimal` | Option C; full-set = REQ-05 baseline |
| R6-B-04 | Ops runbook: pin → stage → deploy → `/readyz`; node swap | Масштаб нод |
| R6-B-05 | Verify registry pin / hash behavior unchanged | No regression |

**Optional follow-up (не Done):** layered manifest (Option D) после стабильных profiles.

---

## 7. Non-goals

- REQ-02 federation / multi-node routing product.
- Nested Custom GPT Knowledge upload automation inside bridge.
- Full parity «каждый файл Knowledge в каждом turn» без profile choice.
- Правка текста REQ-01.

---

## 8. Version log

- v0.1.1 — 2026-09-16: profiles renamed to `full-set` + `pilot-minimal`; align with REQ-05 v0.2 full-dump rule.
- v0.1.0 — 2026-09-16: Phase B REQ from accepted F+B+C recommendations; anti-spaceship outs; REQ-only delivery.
