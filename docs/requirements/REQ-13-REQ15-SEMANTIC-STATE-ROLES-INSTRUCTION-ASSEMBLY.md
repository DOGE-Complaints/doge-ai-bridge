# REQ-13 — REQ15: Semantic interview state, roles, instruction assembly (hybrid C)

Parent: [docs/requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md](<../../../docs/requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md>) §3 L8–L13, §4 O4–O6, §5–6, AC-06, AC-09, AC-11  
Parent-id: REQ15-interview-deepseek-telegram  
**T1 audit:** [`../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md`](../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md) (2026-11-01T12:30:40Z)  
**Wave readiness / arch after REQ-11+12:** [`../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md`](../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md) — §5.3 copy-paste; stories only after arch  
**Renumber (2026-11-01):** was aibridge REQ-12 (state/roles); ids `AC-AIB-12-*`/`L12-*` → `AC-AIB-13-*`/`L13-*`  
Siblings:
- [GPT UI REQ-48](<../../../GPT UI/docs/requirements/REQ-48-req15-role-oriented-instruction-line-and-export.md>) (authoring SSOT: role-oriented line + mapping + **export parity**; archive prerequisite)
- [`REQ-12`](./REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) (model port)
- [`REQ-11`](./REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) (submit/handoff **code**; not in role prompts)
- [doge-telegram REQ-01](../../../doge-telegram/docs/requirements/REQ-01-REQ15-TELEGRAM-CHANNEL-TRANSPORT.md) (transport only)
Status: Draft — **T1 Present** · **target tech-arch Present** · **STORY-62…64 Product Done** · **STORY-65 ASGI wire Present (G-02 Lifted)** · residuals: **AC-05 Explicit Partial** · STORY-66/67 · product locks Q3–Q5 2026-11-01  
Дата: 2026-10-31 · T1/hygiene: 2026-11-02 · Locks: 2026-11-01 · Renumber: 2026-11-01 · Arch: 2026-11-02 · Backlog Done: 2026-11-02 · Cascade prep: 2026-11-02 · STORY-65 wire: 2026-11-04  

**Architecture:** [`../architecture/req15-semantic-state-roles/00-overview.md`](../architecture/req15-semantic-state-roles/00-overview.md)  
**Tech-arch interview:** [`../analysis/zeya888.target-tech-arch-interview-req15-semantic-state-roles-2026-11-02.md`](../analysis/zeya888.target-tech-arch-interview-req15-semantic-state-roles-2026-11-02.md)  
**Backlog:** [`../tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md`](../tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md) · active 65→66→67 · G-02 **Lifted** (STORY-65)  
**Runtime evidence:** [`../runtime-docs/09-semantic-state-store-invalidation.md`](../runtime-docs/09-semantic-state-store-invalidation.md) · [`10`](../runtime-docs/10-roles-coordinator-assembly.md) · [`11`](../runtime-docs/11-content-volume-parity-stub-live-evidence.md) · [`12`](../runtime-docs/12-asgi-channel-semantic-roles-wire.md)  

Locks: delivery **C**; **consume parity Pass** on this side (live Explicit Partial until GPT-48 export + ops); instructions lose model-owned gateway/redirect (server REQ-11)

> **Naming note:** This child is **aibridge REQ-13** (REQ15 semantic state / roles / assembly). It is **not** product backlog [REQ13 sense-brief/poster](../../../docs/requirements%20backlog/REQ13-DOGEstonia-Issue-Sense-Brief-And-Civic-Poster.md) (that worker line is aibridge [REQ-09](./REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md)).

---

## Целевое состояние (простыми словами)

Bridge ведёт **смысл интервью** у себя: фаза, факты со ссылками на реплики, гипотезы, пробелы, правки — не «только длинный чат в промпт».

Роли (настройка общения, интервьюер, экстрактор, нормализатор, checker) — **версионные конфиги задач**. Код **собирает** им инструкции из файлов на диске (`INSTRUCTIONS_DIR`): локально — путь для dev/CI, на проде — **Railway volume** с выгрузкой из GPT UI. Python-пакет **не** мастерская текстов.

Перед тем как считать content готовым: **consume parity** — то, что смонтировано/лежит в dir, совпадает с выпущенным набором (sibling GPT UI export Pass). Дырявый каталог → ready/fail-closed, не тихий subset.

Модель **не** сама шлёт в gateway и **не** строит SPA-redirect — это REQ-11.

---

## 1) Goal

Application-owned semantic interview state; versioned roles; code-driven instruction assembly from dir (hybrid **C**); **consume parity Pass**; coordinator selects tasks (not a free meta-agent).

## 2) Scope / Out of scope

**In scope**

- Semantic state: phase, coverage, facts↔utterances, hypotheses, gaps, corrections; invalidate dependents on meaning change (with REQ-11 confirms).  
- Role registry v1: Communication setup · Interviewer · Extractor · Normalizer · Checker.  
- Instruction assembly from shared core + node settings; pin versions per conversation.  
- Read content only via `DOGESTONIA_INSTRUCTIONS_DIR` + manifest (Present env pattern); prod volume-capable.  
- **Consume parity** vs GPT UI export inventory/hashes; `/ready`-class fail-closed on incomplete content.  
- Context trim rules: preserve confirmed facts/grounds (parent O6).  
- Coordinator: explicit Python step selection — not roaming meta-agent (L10).  
- Adapt Present auto-offer-interpret behavior toward resume-readiness (T1 Adapt) — product policy + arch.

**Out of scope**

- Authoring/editing instruction markdown in this repo as SSOT (GPT UI REQ-48).  
- Implementing provider HTTP (REQ-12).  
- Gateway HTTP client + dual-confirm product gates (REQ-11) — **except** invalidation hooks from meaning change.  
- Telegram bot I/O (telegram REQ-01).  
- Agent admin UI (L15).  
- Product REQ13/14 worker pipelines (aibridge REQ-09).  
- Inventing DB table schemas as SSOT in this REQ (Architect Studio / PA.2).

## 3) Verified current state (T1 + post STORY-62…64)

| Fact | Path / note |
|------|-------------|
| Content load from dir + manifest (Phase-A `files[]`) | [`content.py`](../../src/aibridge/content.py) · env [`config.py`](../../src/aibridge/config.py) `DOGESTONIA_INSTRUCTIONS_*` — **legacy/transitional** readiness path |
| Roles manifest + assembly (REQ15 line) | [`roles/assembly.py`](../../src/aibridge/roles/assembly.py) · fixture [`tests/fixtures/content/roles.manifest.json`](../../tests/fixtures/content/roles.manifest.json) — **GPT-48 export target** (§3b) |
| Physical copy in image | `src/instructions/` + Dockerfile COPY = fixture/dev (L13-2); sync script from GPT UI **not found** |
| InterviewEngine instructions | [`interview.py`](../../src/aibridge/interview.py) — assembled string; per-role ASGI bind **Absent** |
| Semantic state store | **Present as module+harness** (STORY-62) — [`semantic_state/`](../../src/aibridge/semantic_state/) · migration [`0002_semantic_state.sql`](../../migrations/0002_semantic_state.sql); ≠ HistoryStore; **ASGI/channel bind Present** (STORY-65 · G-02 Lifted) — Transition C EDIT path remains enforce in channel |
| Role registry / policy / assembly | **Present as module+harness** (STORY-63) — [`roles/`](../../src/aibridge/roles/); `select_next_role` / `assemble_role_prompt` **wired** on `/v1/channel/turns` (STORY-65 · G-02 Lifted; roles paths optional until STORY-66) |
| Coordinator auto-offer interpret | [`coordinator.py`](../../src/aibridge/coordinator.py) — FC-less → interpret offer (L13-1); send only after FC; `select_next_role` re-export |
| AC validation (2026-11-02 code audit) | See §5 wave column — harness Confirmed; runtime Partial; AC-05 live Explicit Partial |
| T1/post-story verdict | content load **Keep**/Adapt; semantic/roles **Present harness+channel wire** (STORY-65); mega-prompt **Adapt** via GPT-48 / STORY-66 cutover |

### 3b) GPT-48 export consumer contract (locked · cascade input)

Copy into GPT UI REQ-48 export/authoring. **Do not invent** alternate layout.

| Contract | Value |
|----------|--------|
| Env root | `DOGESTONIA_INSTRUCTIONS_DIR` |
| Manifest env | `DOGESTONIA_INSTRUCTIONS_MANIFEST` — after REQ15 cutover points at **roles-schema** manifest (not Phase-A `files[]` alone) |
| Roles schema | JSON object: `bundle_version` (string) · `core` (filename) · `roles` (object) |
| Role ids (exact) | `communication_setup` · `interviewer` · `extractor` · `normalizer` · `checker` |
| Per role | `{ "file": "<root-child.md>", "version": "<pin>" }` — both required strings |
| Path rule | `core` and every `roles.*.file` = **non-empty root children** of the instructions dir — no `/`, `\`, `.`, `..`, absolute paths (enforced in `roles/assembly.py` and Phase-A `content.py`) |
| Phase-A `files[]` | `bundle_version` + `files[]` loader remains for **legacy/transitional** readiness until ASGI role wire; **not** SSOT of the new GPT-48 line |
| Dual schema | Concurrent `files[]` vs roles-schema on one env = **wire residual** (blocking live channel orchestration), **not** authoring ambiguity if export follows this table |
| Forbidden in new texts | Gateway stash URL choice, `POST /story-drafts`, SPA redirect procedure (AC-AIB-13-07 · peer REQ-11) — Checker **prose** only; submit stays code |
| Parity | **Export Pass** (GPT-48) ≠ **Consume Pass** (this REQ AC-05); inventory/hash wire format = joint Open — do not invent here |
| Cascade note | On GPT UI cascade: refresh REQ-48 §3 Verified state (role registry Present in aibridge harness; ASGI wire Absent) — **not** done in this wave |

## 4) Target behavior

1. State persists and drives what roles may claim; model proposes, app validates.  
2. Assembly builds role prompts from files — model does not “hunt” active pack via vague links.  
3. Hybrid **C**: same read contract local and volume; authoring stays GPT UI.  
4. Consume parity Pass required for content Done; incomplete mount fails closed.  
5. Role prompts do not encode stash URL choice or SPA redirect procedure.  
6. Ordinary model reply ≠ automatic final-confirm offer without explicit resume/process gate (parent O5; T1 Adapt).

## 5) Acceptance criteria

| ID | Criterion | Parent map | Wave status (2026-11-02 code audit) |
|----|-----------|------------|-------------------------------------|
| **AC-AIB-13-01** | Semantic state fields (phase/facts/hypotheses/gaps/corrections + utterance grounds) persist across turns | AC-REQ15-06 | **Harness Confirmed** (`test_story_62_*`); channel ASGI persist **Present** (STORY-65 · `test_story_65_*`) |
| **AC-AIB-13-02** | Five v1 roles callable via coordinator with version pins | O5 · §6 | **Harness Confirmed** (`test_story_63_*`); channel orchestration **Present** (STORY-65 · `select_next_role` on turns); roles-schema cutover residual → **STORY-66** |
| **AC-AIB-13-03** | Instructions assembled only from configured dir + manifest | AC-REQ15-09 | **Harness Confirmed** (roles-schema); channel assemble **Present** when `DOGESTONIA_ROLES_*` set (STORY-65); full cutover residual → **STORY-66** |
| **AC-AIB-13-04** | Prod path documented for Railway volume mount (ops may upload manually v1) | AC-REQ15-14 | **Confirmed** (docs) — runtime-docs `11` |
| **AC-AIB-13-05** | **Consume parity Pass** evidence vs GPT UI export inventory | AC-REQ15-13 | **Explicit Partial** — gate/docs+stub Done; live needs GPT-48 export Pass + ops window |
| **AC-AIB-13-06** | Incomplete/mismatched content → readiness fail-closed | AC-REQ15-13 spirit | **Partial Confirmed** — local incomplete/file miss fail-closed Present; export-inventory **mismatch** comparator Absent (joint Open) |
| **AC-AIB-13-07** | Role instruction text does not own gateway submit or SPA redirect (REQ-11) | AC-REQ15-12 | **Confirmed** (fixtures + harness) |
| **AC-AIB-13-08** | Resume / confirm-offer policy: ordinary reply does not equal send-permission offer without process gate | O5 · T1 Adapt | **Confirmed** (`coordinator.py` L13-1) |

**Parent AC-REQ15-11 (methodology):** preserved via GPT-48 **mapping** deliverable + this consume contract; aibridge does not re-author Module-1 — enforcement is export→consume without silent drop.

## 6) Interview locks (operator 2026-11-01)

| ID | Lock |
|----|------|
| **L13-1** | Confirm-offer policy v1 (**soft**): auto-offer **understanding** confirm may remain; **send** confirm is never automatic — ordinary model reply ≠ send permission (O5 partial Adapt) |
| **L13-2** | After volume cutover: image-baked `src/instructions/` = **fixture/dev only**; prod read = configured dir / Railway volume; authoring SSOT stays GPT UI |
| **L13-3** | **Send-permission invalidation (Q5):** **Target = A** — any app-recorded meaning change in semantic state invalidates dependent send permission (and dependent checks) even without Telegram EDIT. **Transition = C** — until semantic state Present, keep Present EDIT/revision invalidation only. |

## 7) Open (residual)

| Item | Class | Next |
|------|-------|------|
| Exact DB/table shape for semantic state | **Closed for v1** | Migration `0002` Present; further DDL = implement residual |
| Consume parity hash/inventory format | **Product** (joint GPT-48) + **Arch** enforce gate | Align with GPT UI export Pass — **blocking live AC-05**, not blocking GPT-48 **authoring** if §3b followed |
| Dual manifest schema (`files[]` vs roles) / ASGI role+semantic wire | **Wire residual** | **Blocking live channel** orchestration; **not** blocking GPT-48 authoring under §3b |
| Hard gate on understanding-offer (Q3 option A as later goal) | **Product later** | After roles land in channel |
| Role merge/split after latency measurement | **Product later** | Parent allows after quality data |
| Which state field updates count as “meaning change” (sensitivity) | **Locked arch D2** | Confirmed facts / corrections / (phase if rights change) |
| Coordinator selection model | **Locked arch D3** | Policy table → one next role |
| Assembly shape | **Locked arch D5** | Shared core + per-role slice + session pin |
| Evidence stub vs live | **Locked arch D6** | Split gate; live Partial without ops window |

## 8) Functional vs tech split

| Layer | Lives in |
|-------|----------|
| Product / AC | This REQ + parent REQ15 |
| Target tech | [`../architecture/req15-semantic-state-roles/00-overview.md`](../architecture/req15-semantic-state-roles/00-overview.md) |
| Work items | [`STORY-AIBRIDGE-62…64`](../tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md) **Product Done** · residuals above |
| GPT-48 export contract | §3b this file — input to sibling cascade |

**Next process step (operator):** peer **GPT UI REQ-48** cascade (use §3b); residual ASGI wire / live AC-05 when ops+export ready. No second architecture prompt. No invent hash SSOT.
