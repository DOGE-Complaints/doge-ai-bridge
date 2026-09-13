# P4 Audit — STORY-AIBRIDGE-14-p1-ops-schema-restart

| Field | Value |
|-------|-------|
| **Date** | 2026-09-13 |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/STORY-AIBRIDGE-14-p1-ops-schema-restart/STORY-AIBRIDGE-14-p1-ops-schema-restart.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md` |
| **Method** | Read/Glob only; no product patches; no live pytest this pass |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (P1-01–04,06,07 / dry-run lift / AC #7–#8)** | **PASS** on core knobs · **residuals** below |
| **Bullrun t01–t07 Done** | **Confirmed** vs modules + gate PASS 2026-09-13T17:14:26Z |
| **OPEN gaps** | **2 Medium · 1 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **Unknown**; historical **191 passed / 1 skipped** @ P3 gate |

---

## Bullrun touchpoints (отчёт only)

| ID | Claim | P4 fact |
|----|-------|---------|
| Story 14 | 🟢 Done · awaiting P4 | Shutdown / defaults / schema / knobs / Dockerfile Done; DB race + gateway connect residuals |
| t01–t06 | Done | **Confirmed** (`app.py`, `config.py`, `request_assembly.py`, `gateway.py`, `Dockerfile`, tests) |
| t07 gate | Done | PASS · 191/1 · verify 7 paths |

---

## AC matrix (`$storyFile` Target · REQ-03 §6)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| R3-P1-01 | Graceful shutdown (AIB-OPS-03) | **PASS** | Lifespan drain → `accepting_traffic=False` + `recover_all_executing_attempts`; channel 503 `shutting_down`; `test_story_14_drain_*` / `…_lifespan_marks_executing_unknown_*` |
| R3-P1-02 | Channel 429 / rate defaults + budgets on `/turns` | **PASS** | Finite `DEFAULT_*` in `config.py`; `BudgetGuard` always on `create_app`; 429 when principal limit=1; session-cap budget reply on turns |
| R3-P1-03 | Full schema validation; blocks real gateway readiness | **PASS (validators)** · **Info residual** | `_validate_type` enum/const/min/max/pattern; dry-run lift needs `AIBRIDGE_SCHEMA_VALIDATION_COMPLETE`. `schema_validation_complete()` is keyword-set tautology — **G-03** |
| R3-P1-04 | Restart recovery + **DB** race/restart (Send / pending / unknown) | **PARTIAL** | In-memory `recover_all` / `send_blocked` / timeout→`UNKNOWN_OUTCOME` tests. **No disposable-Postgres race/restart suite in story 14** — **G-01** |
| R3-P1-06 | Gateway response-size + remaining §17 timeout knobs | **PARTIAL** | `max_response_bytes` default + enforce → `CONTRACT_MISMATCH`; total timeout → executor. **`AIBRIDGE_HTTP_CONNECT_TIMEOUT_MS` not applied to gateway httpx** (REQ-01 §17 gateway connect) — **G-02** |
| R3-P1-07 | Dockerfile reproducible deploy | **PASS** | Root `Dockerfile` + `.dockerignore`; uvicorn `aibridge.app:app`; test asserts presence |
| Target 2 | `DRY_RUN=false` readiness only after schema complete proven | **PASS** (flag gate) | `test_story_14_readyz_dry_run_false_after_schema_complete` |
| Target 3 | Restart/race cover AC #7–#8 | **PASS (logic)** · **PARTIAL vs DB claim** | Logic covered; DB facet → **G-01** |

### Scope extras

| Item | Status | Evidence |
|------|--------|----------|
| P1-05 dual instructions | Out of scope | Superseded → P0-13 / story 10 |
| P1-08/09/10 | Out of scope | → 17 / 15 / 16 |
| Connect timeout on OpenAI client | **PASS** (separate) | `app.py` → `ProductionResponsesClient(connect_timeout_ms=…)` — not gateway |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | R3-P1-04 / Target #3 claim «DB race/restart tests» for Send / pending-confirm / `unknown_outcome`. Fact: `tests/test_story_14_ops_schema_restart.py` uses in-memory `_Attempts` / `_sessions` only — no `.pgdata-test`, no concurrent Send on `GatewayAttemptStore` / `PostgresConfirmSessionStore`. Story 13 PG restart is adjacent but does not satisfy this story’s DB-race DoD. | Add disposable-PG restart/race tests (executing→unknown no resend; pending Send token; optional concurrent Send unique attempt); or narrow backlog Verified wording if 13 is accepted as sole DB evidence. |
| **G-02** | **Medium** | R3-P1-06 + REQ-01 §17: `AIBRIDGE_HTTP_CONNECT_TIMEOUT_MS` is Gateway connect timeout. Fact: Settings default exists; OpenAI path uses it; `default_executor_from_settings` / `HttpxGatewayTransport` pass a single `timeout=` float (total only) — connect knob does not constrain gateway HTTPS connect. Test only asserts settings field, not transport connect. | Wire `httpx.Timeout(total=…, connect=connect_ms/1000)` (or equivalent) from Settings into gateway transport; assert in unit test. |
| **G-03** | **Info** | R3-P1-03 readiness helper `schema_validation_complete()` returns True whenever `FULL_SCHEMA_KEYWORDS` lists `"enum"`/`"const"` — always True after ship. Real gate is operator `AIBRIDGE_SCHEMA_VALIDATION_COMPLETE`; validators themselves are real. | Optional: probe validator features (or fixture schema round-trip) instead of frozenset membership; keep env flag as attestation. |

### Non-gaps

| Topic | Note |
|-------|------|
| Live n8n / privacy / SPA E2E | Out of scope → 15 / 16 / 17 |
| Budget soft-stop vs 429 | Rate path is 429; budget path soft reply — matches «budgets on /turns» + separate rate limits |
| Dockerfile Railpack SUCCESS | Correctly not claimed |
| Drain rejects new turns | Covered; in-flight mid-Send during SIGTERM is ops nuance, not failing P1-01 as written |

---

## Cited paths

- `src/aibridge/app.py`, `config.py`, `readiness.py`, `request_assembly.py`, `gateway.py`, `budgets.py`, `rate_limit.py`
- `tests/test_story_14_ops_schema_restart.py`
- `Dockerfile`, `.dockerignore`
- Gate: `acceptance-verification-task-aibridge-02-14-t07-…md`
- REQ-03 §2 · §6 P1-01–04,06,07 · REQ-01 §17

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Medium), G-03 (Info)
- **Critical:** 0
- **OPEN counts:** Medium **2** · Info **1** · Low **0** · Critical **0**
- **next:** **P5** disposition
