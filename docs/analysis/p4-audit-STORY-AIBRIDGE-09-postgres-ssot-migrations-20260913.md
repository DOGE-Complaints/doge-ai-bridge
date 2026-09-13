# P4 Audit — STORY-AIBRIDGE-09-postgres-ssot-migrations

| Field | Value |
|-------|-------|
| **Date** | 2026-09-13 |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/STORY-AIBRIDGE-09-postgres-ssot-migrations/STORY-AIBRIDGE-09-postgres-ssot-migrations.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md` |
| **Method** | Read/Glob only; no product patches; no live pytest this pass |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story AC #1–#5** | **PASS** on migrations + `pg_runtime` library + disposable PG tests |
| **Bullrun t01–t07 Done** | **Confirmed** vs modules + gate PASS 2026-09-13T15:25:46Z |
| **Default ASGI / Confirm runtime path** | **Incomplete** — see **G-01** / **G-02** |
| **OPEN gaps** | **2 Medium** |
| **Critical OPEN** | **0** |
| **Live pytest** | **Unknown**; historical **109 passed / 1 skipped** @ P3 gate |

---

## Bullrun touchpoints (отчёт only)

| ID | Claim | P4 fact |
|----|-------|---------|
| Story 09 | 🟢 Done · awaiting P4 | **Library/schema Done**; ASGI + Confirm SSOT residual |
| t01–t06 | Done | **Confirmed** (`migrations/`, `migrate.py`, `pg_runtime.py`, tests) |
| t07 gate | Done | PASS artifact — evidence is store-level, not full ASGI wire |

---

## AC matrix (`$storyFile`)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | Versioned migrations; boot schema-only not production-acceptable | **PASS** | `migrations/0001_ssot_core.sql`; `migrate.apply_migrations` on PG `create_app`/`_init_stores`; `ensure_schema=False` default in `PostgresSessionStore` / `PostgresBundleRegistry`; `test_migrations_files_exist_and_apply`, `test_boot_schema_flag_defaults_off_for_open_helpers` |
| 2 | Constraints enforced; failed txn does not advance history/FSM | **PASS** (schema/store) · **residual** | Unique PK on `event_dedupe`, `action_token`, `session_call`, `gateway_attempt`; store tests. **No** Confirm/FSM + history atomic txn on live path — see **G-02** |
| 3 | Transport replay after restart → stored HTTP status + body | **PASS** (library) · **residual** | `PostgresEventDedupeStore` + `test_event_dedupe_unique_and_replay_after_reconnect`. Default `create_app` still uses in-memory `EventDedupeStore()` — see **G-01** |
| 4 | Disposable Postgres + concurrency races (constraints win) | **PASS** | `scripts/start-disposable-pg.sh`; `test_turn_lock_concurrency_one_wins`; `test_event_dedupe_concurrency_constraints_win` |
| 5 | Production path no silent memory fallback for dedupe/session/confirm/tokens/history | **PARTIAL** | Policy: `assert_no_silent_memory_fallback` + `AIBRIDGE_ALLOW_MEMORY_STORES` for registry/sessions open. **Fact:** Grep `src/aibridge` — **no** import of `pg_runtime` outside `pg_runtime.py`; `create_app` defaults `EventDedupeStore()` + in-process `ConfirmationGuard` — see **G-01** |

### Scope extras

| Item | Status | Evidence |
|------|--------|----------|
| dict_row factory | **PASS** | `db.connect_postgres` → `row_factory=dict_row` |
| One active turn (DB) | **PASS** (library) | `PostgresTurnLock`; not used by `channel.py` / `InterviewEngine` (still `turn_lock.SessionTurnLock`) |
| At most one gateway attempt / revision | **PASS** (schema+store) | `GatewayAttemptStore`; **not** called from `confirm.py` |
| Supersedes STORY-07/08 | **Noted** | Backlog meta; persistence now in this story’s stores |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | `create_app` (`app.py`): `store = dedupe_store or EventDedupeStore()` always; `ConfirmationGuard` gets only `GatewayExecutor`, still `ActionTokenStore` + `_sessions` in-process. When `DATABASE_URL=postgresql://…`, migrations + session/registry open PG, but **dedupe / confirm / tokens / history / turn-lock never switch to** `PostgresEventDedupeStore`, `PostgresConfirmSessionStore`, `PostgresActionTokenStore`, `PostgresHistoryStore`, `PostgresTurnLock`. AC #3/#5 production path residual; gate evidence was repos+policy, not ASGI wire. | Factory: if postgres URL and not `allow_memory`, construct PG stores and inject into dedupe + `ConfirmationGuard` (+ interview history/lock if on path); fail-closed without `AIBRIDGE_ALLOW_MEMORY_STORES`; TestClient integration without manual inject. |
| **G-02** | **Medium** | REQ-03 §5.3: token consume + `executing` gateway-attempt **atomically before** HTTPS; failed txn must not advance history/FSM. Fact: `GatewayAttemptStore` unused outside `pg_runtime`/tests; `confirm.call_gateway` has no attempt-row / commit-before-HTTPS; `InterviewEngine` defaults in-process `HistoryStore` + `SessionTurnLock`. Schema constraints exist; runtime orchestration absent. | Wire attempt create+commit before `execute_stash`; outcome update after; share txn / fail-closed with history+FSM; concurrency under `PostgresTurnLock` on turn/action path; tests for race + rollback. |

### Non-gaps

| Topic | Note |
|-------|------|
| Live OpenAI client / ASGI coordinator / n8n / SPA / multi-replica | Out of scope (stories 10–11, 18) |
| `CREATE TABLE IF NOT EXISTS` under `ensure_schema=True` | Explicit non-prod / unit-fake path; default False |
| Disposable PG skip when `.pgdata-test` down | Documented; not AC fail when script started for gate |

---

## Cited paths

- `migrations/0001_ssot_core.sql`, `migrations/README.md`
- `src/aibridge/{db,migrate,pg_runtime,app,confirm,dedupe,history,turn_lock,sessions,registry,interview,config}.py`
- `tests/test_story_09_postgres_ssot.py`
- `scripts/start-disposable-pg.sh`
- Gate: `acceptance-verification-task-aibridge-02-09-t07-…md`

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Medium)
- **Critical:** 0
- **OPEN counts:** Medium **2** · Info **0** · Low **0** · Critical **0**
- **next:** **P5** disposition
