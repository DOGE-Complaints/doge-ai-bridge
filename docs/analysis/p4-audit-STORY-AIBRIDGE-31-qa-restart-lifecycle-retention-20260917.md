# P4 Audit — STORY-AIBRIDGE-31-qa-restart-lifecycle-retention

| Field | Value |
|-------|-------|
| **Date** | 2026-09-17T20:15:03Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-04-…/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md` |
| **Method** | Read/Glob + live pytest `tests/integration/test_lifecycle_retention.py`; fixture hash package↔`tests/fixtures/{settings,channel,spies}`; product `app.py` / `pg_runtime` / `privacy_retention` / `story13_e2e_helpers.rebuild_app_same_pg`; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway / live Telegram** | **No** Railway SUCCESS · **No** live Telegram PASS invented |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (LIFE-001…012 · guide §10.9)** | **PASS (core)** — 13 fixtures + suite; characterization 009/010 marked; **1 Medium** residual on PG/`rebuild_app_same_pg` restart depth |
| **Bullrun t01–t04 Done** | **Confirmed** vs promote copies + gate PASS 2026-09-17T20:12:21Z |
| **OPEN gaps** | **0 Critical · 1 Medium · 1 Low · 3 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **13 passed** (`tests/integration/test_lifecycle_retention.py`) @ 2026-09-17T20:15:03Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-31** | 🟢 Implemented (P3 · next P4) · pkg-000028 | **Confirmed** LIFE suite; gate PASS; Preference A mem noted; **this P4** → next **P5** |
| **t01** | Done — generate LIFE-* envelopes | **Confirmed** 13 package `life-*.json` |
| **t02** | Done — promote=copy | **Confirmed** 13 hash_eq settings/channel/spies |
| **t03** | Done — integration lifecycle | **Confirmed** 13 passed · residual G-01/G-02 |
| **t04** | Done — story gate PASS | **Confirmed** acceptance 2026-09-17T20:12:21Z · no Railway/live TG invent |
| **pkg-000028** | Active · 4 paths | YAML present under `aibridge-active-packages/` |
| **TRACEABILITY** | LIFE-001…012 → story `covered` | **Confirmed** |
| **$storyFile AC** | nested tasks **Todo** · AC `[ ]` · «not materialized until P1» stale | **Drift** → **Info G-05** (epic/pipeline Done; backlog stale) |

---

## AC matrix (`$storyFile` / pipeline · guide §10.9 LIFE-*)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| LIFE-001 | 503 `shutting_down`, retryable true | **PASS** | `test_life_001` · settings `life-shutting-down` · `app.state.accepting_traffic=False` · `/healthz` 200 |
| LIFE-002 | PG history/session restored; no duplicate side effect | **PARTIAL → G-01/G-02** | `_MemConfirmSessions` + `_rebuild_guard`; state/revision restored; **no** `PostgresConfirmSessionStore` / `PostgresHistoryStore` / `rebuild_app_same_pg`; spy `openai_call_count_after_restart_replay` **unread** |
| LIFE-003 | Pending token usable after restart (if persistence active) | **PARTIAL → G-01** | shared in-memory `ActionTokenStore` across rebuild; **no** `PostgresActionTokenStore` |
| LIFE-004 | Consumed token stays consumed | **PARTIAL → G-01** | same memory token store; consumed 409 path OK in-process |
| LIFE-005 | Open gateway attempt → unknown; reconciliation | **PASS (seam)** | `GatewayAttemptStore` + `_FakeGwAttemptConn` · recover → unknown · send blocked |
| LIFE-006 | TTL → new session; narrative minimized; old tokens unusable | **PASS** | `SessionActivityClock.seed` · tombstone · old token not usable |
| LIFE-007 | Bundle retained while session active | **PASS** | `MemoryBundleRegistry` + `gc_unreferenced_bundles` · deleted=[] |
| LIFE-008 | Unreferenced after grace → GC | **PASS** | deactivate + grace · hash deleted |
| LIFE-009 | After `cancelled` — characterization | **PASS (char)** · **Info G-03** | marked characterization; captures **same** cancelled session (terminal trap) |
| LIFE-010 | After `stashed` — characterization | **PASS (char)** · **Info G-03** | marked; captures same stashed session |
| LIFE-011 | Edit from `unknown_outcome` → new revision; old non-resendable | **PASS** | timeout → unknown · `apply_edit` · revision++ · offer reinterpret |
| LIFE-012 | Deployment change → token invalid | **PASS** | mutate `deployment_id` · 409 conflict · message contains deployment |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| TRACEABILITY story key | **PASS** | Matrix LIFE-001…012 `covered` |
| Promote = copy | **PASS** | 13 FIXTURE_NAMES hash_eq |
| Characterization LIFE-009/010 | **PASS** | envelope `notes` + test docstrings |
| Harness disposable PG + `rebuild_app_same_pg` | **FAIL vs claim → G-01** | Preference A mem; helper exists in `tests/story13_e2e_helpers.py` but **unused** here |
| Fake clock for TTL | **Info G-04** | `SessionActivityClock.seed` offset, not named injectable clock |
| SPA / hasUxPipeline | false | |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | Guide/story Context: PostgreSQL SSOT; TECH/t03 harness = disposable PG + `rebuild_app_same_pg`. LIFE-002/003/004 restart path uses `_MemConfirmSessions` + in-memory `ActionTokenStore` + `_rebuild_guard` only. Product has `PostgresConfirmSessionStore` / `PostgresActionTokenStore` / `PostgresHistoryStore` (`pg_runtime.py`) and `rebuild_app_same_pg` (`story13_e2e_helpers.py`) — **unexercised** in this suite. Gate explicitly Preference A. TRACEABILITY marks LIFE-002…004 `covered` while PG restart branch is documentary. | Disposable-PG (or skipif) LIFE-002/003/004 via `rebuild_app_same_pg` + PG confirm/token(/history) stores; or mark characterization Preference A memory-only and align TRACEABILITY/harness docs. |
| **G-02** | **Low** | Spy `life-restart-interview` declares `openai_call_count_after_restart_replay: 0`; `test_life_002` never reads it. «History restored» / «no duplicate confirmed side effect» asserted only via session id/state/rev + `gateway_call_count` (no history list / OpenAI recording across rebuild). | Assert spy openai field via recording engine; persist+restore history across restart; or mark spy fields matrix-only. |
| **G-03** | **Info** | LIFE-009/010 characterization documents terminal trap (same session stays cancelled/stashed). Guide text also asks raise mismatch if resident cannot start over / must not silently trap — **no** pending-decision artifact raised; capture-only. | Optional pending-decision note; or WAIVE capture-first sufficient until product policy. |
| **G-04** | **Info** | Story harness names fake clock + graceful shutdown; TTL uses `clock.seed(…, time.time()-1000)`; LIFE-001 flips `accepting_traffic` directly (not lifespan shutdown API). | Optional injectable clock / shutdown helper; or WAIVE current seams. |
| **G-05** | **Info** | `$storyFile` nested tasks still **Todo**, AC mostly `[ ]`, «folders not created until P1» while epic/tasks Done and gate PASS. | Align backlog Meta/tasks/AC to Done/`[x]` (docs-only). |

### Non-gaps

| Topic | Note |
|-------|------|
| Inventing Railway SUCCESS / live Telegram | Avoided |
| Fixture originals moved | Not done; promote=copy verified (13) |
| Silent product invent on 009/010 | Avoided — characterization marked |
| LIFE-005/006/007/008/011/012 core asserts | Present under memory/fake seams |
| SPA / hasUxPipeline | false |

### Regressions

| Topic | Note |
|-------|------|
| vs gate t04 (13 passed) | **None** — re-run 13 passed @ 2026-09-17T20:15:03Z |

---

## Cited paths

- `tests/integration/test_lifecycle_retention.py`
- `tests/fixtures/{settings,channel,spies}/life-*.json`
- `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/life-*.json`
- `src/aibridge/pg_runtime.py` · `src/aibridge/app.py` · `src/aibridge/privacy_retention.py` · `src/aibridge/bundle_gc.py`
- `tests/story13_e2e_helpers.py` (`rebuild_app_same_pg` — unused by LIFE suite)
- Gate: `…/task-aibridge-31-t04-story-gate/acceptance-verification-….md`

---

## Handoff

- **OPEN gaps:** 0 Critical · **1 Medium** · **1 Low** · **3 Info**
- **Product Story AC/DoD (core):** **PASS** (explicit; ≠ empty gap-list)
- **next:** **P5** (disposition; do not implement in P4)
