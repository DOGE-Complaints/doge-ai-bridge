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
Status: Draft — **T1 Present** · **target tech-arch Present** · **backlog STORY-62…64 Todo** · product locks Q3–Q5 2026-11-01 · AC-05 Partial (Q1)  
Дата: 2026-10-31 · T1/hygiene: 2026-11-02 (roles Present · STORY-63 t09) · Locks: 2026-11-01 · Renumber: 2026-11-01 · Arch: 2026-11-02 · Backlog: 2026-11-02  

**Architecture:** [`../architecture/req15-semantic-state-roles/00-overview.md`](../architecture/req15-semantic-state-roles/00-overview.md)  
**Tech-arch interview:** [`../analysis/zeya888.target-tech-arch-interview-req15-semantic-state-roles-2026-11-02.md`](../analysis/zeya888.target-tech-arch-interview-req15-semantic-state-roles-2026-11-02.md)  
**Backlog:** [`../tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md`](../tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md)  

Locks: delivery **C**; **consume parity Pass** on this side; instructions lose model-owned gateway/redirect (server REQ-11)

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

## 3) Verified current state (T1)

| Fact | Path / note |
|------|-------------|
| Content load from dir + manifest | [`content.py`](../../src/aibridge/content.py) · env [`config.py`](../../src/aibridge/config.py) `DOGESTONIA_INSTRUCTIONS_*` |
| Physical copy in image | `src/instructions/` + Dockerfile COPY; sync from GPT UI **not found** |
| Manifest often subset | e.g. Module-1 chain — not full Custom GPT Knowledge set |
| InterviewEngine instructions | [`interview.py`](../../src/aibridge/interview.py) — assembled string into Responses |
| Full semantic state store (phase/facts/hypotheses as app SSOT) | **Present** (STORY-62) — [`semantic_state/`](../../src/aibridge/semantic_state/) · migration [`0002_semantic_state.sql`](../../migrations/0002_semantic_state.sql); ≠ HistoryStore / ≠ `last_confirmed_state` SSOT; ASGI/channel bind residual OOS (Transition C) |
| Role registry as parent §6 | **Present** (STORY-63) — [`roles/`](../../src/aibridge/roles/) · five v1 + pins · policy `select_next_role` · assembly+fixtures; ASGI/channel bind residual OOS (G-02 WAIVED) |
| Coordinator auto-offer interpret | [`coordinator.py`](../../src/aibridge/coordinator.py) — FC-less interviewing → interpret offer (T1 Adapt) · `select_next_role` re-export |
| T1 verdict | content load **Keep**/Adapt; semantic state **Present** (62) · roles **Present** (63 harness; ASGI wire residual WAIVED) · mega-prompt **Adapt** |

## 4) Target behavior

1. State persists and drives what roles may claim; model proposes, app validates.  
2. Assembly builds role prompts from files — model does not “hunt” active pack via vague links.  
3. Hybrid **C**: same read contract local and volume; authoring stays GPT UI.  
4. Consume parity Pass required for content Done; incomplete mount fails closed.  
5. Role prompts do not encode stash URL choice or SPA redirect procedure.  
6. Ordinary model reply ≠ automatic final-confirm offer without explicit resume/process gate (parent O5; T1 Adapt).

## 5) Acceptance criteria

| ID | Criterion | Parent map |
|----|-----------|------------|
| **AC-AIB-13-01** | Semantic state fields (phase/facts/hypotheses/gaps/corrections + utterance grounds) persist across turns | AC-REQ15-06 |
| **AC-AIB-13-02** | Five v1 roles callable via coordinator with version pins | O5 · §6 |
| **AC-AIB-13-03** | Instructions assembled only from configured dir + manifest | AC-REQ15-09 |
| **AC-AIB-13-04** | Prod path documented for Railway volume mount (ops may upload manually v1) | AC-REQ15-14 |
| **AC-AIB-13-05** | **Consume parity Pass** evidence vs GPT UI export inventory | AC-REQ15-13 |
| **AC-AIB-13-06** | Incomplete/mismatched content → readiness fail-closed | AC-REQ15-13 spirit |
| **AC-AIB-13-07** | Role instruction text does not own gateway submit or SPA redirect (REQ-11) | AC-REQ15-12 |
| **AC-AIB-13-08** | Resume / confirm-offer policy: ordinary reply does not equal send-permission offer without process gate | O5 · T1 Adapt |

## 6) Interview locks (operator 2026-11-01)

| ID | Lock |
|----|------|
| **L13-1** | Confirm-offer policy v1 (**soft**): auto-offer **understanding** confirm may remain; **send** confirm is never automatic — ordinary model reply ≠ send permission (O5 partial Adapt) |
| **L13-2** | After volume cutover: image-baked `src/instructions/` = **fixture/dev only**; prod read = configured dir / Railway volume; authoring SSOT stays GPT UI |
| **L13-3** | **Send-permission invalidation (Q5):** **Target = A** — any app-recorded meaning change in semantic state invalidates dependent send permission (and dependent checks) even without Telegram EDIT. **Transition = C** — until semantic state Present, keep Present EDIT/revision invalidation only. |

## 7) Open (residual)

| Item | Class | Next |
|------|-------|------|
| Exact DB/table shape for semantic state | **Open (implement / PA.2)** | Arch D1 = separate Postgres store; DDL not SSOT here |
| Consume parity hash/inventory format | **Product** (joint GPT-48) + **Arch** enforce gate | Align with GPT UI export Pass |
| Hard gate on understanding-offer (Q3 option A as later goal) | **Product later** | After roles land |
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
| Work items | [`STORY-AIBRIDGE-62…64`](../tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md) Present |

**Next process step (operator):** backlog STORY-62…64 Present → optional PA.3 refine → P1.3 per story · peer GPT UI REQ-48 for live AC-05 Pass. No second architecture prompt. No P3.
