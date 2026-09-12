# P4 Audit — STORY-AIBRIDGE-03-responses-tool-budgets

| Field | Value |
|-------|-------|
| **Date** | 2026-09-12 |
| **Mode** | `input_mode=backlog_story` (aibridge-operator-contract §6) |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/STORY-AIBRIDGE-03-responses-tool-budgets/STORY-AIBRIDGE-03-responses-tool-budgets.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-03-responses-tool-budgets.md` |
| **Method** | Read/Glob only; no product patches; no live pytest this pass |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story AC #1–#5** | **PASS** (library + RecordingResponsesClient / unit tests) |
| **Bullrun t01–t06 Done** | **Confirmed** vs modules + gate PASS 2026-09-12T21:23:18Z |
| **OPEN gaps** | **1 Medium** + **2 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **Unknown**; historical 50 passed / 1 skipped @ gate |

---

## Bullrun touchpoints (отчёт only — index not rewritten)

| ID | Claim | P4 fact |
|----|-------|---------|
| Story 03 | 🟢 Done | **AC Done** on offline path; residuals below |
| t01 responses-store-false-history | Done | **Confirmed** — `responses_client.py`, `history.py`, `tests/test_responses_store_false.py` |
| t02 strict-tool-oas-pack | Done | **Confirmed** — `tool_gen.py`, `deployment.py` `tool_gen_failed`, `tests/test_tool_gen.py` |
| t03 turn-serialization | Done | **Confirmed** — `turn_lock.py`, `tests/test_turn_lock.py` |
| t04 llm-budgets-no-gateway | Done | **Confirmed** (turn/token) — `budgets.py`, `interview.py`; timeout residual **G-02** |
| t05 validation-gates-cache-hooks | Done | **Confirmed** — `request_assembly.py`, `tests/test_request_assembly.py` |
| t06 acceptance | Done | Gate artifact PASS |

---

## AC matrix (`$storyFile`)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | Every Responses request has `store: false` | **PASS** | `assemble_responses_request` hardcodes `"store": False`; `RecordingResponsesClient.create` asserts; `tests/test_responses_store_false.py` |
| 2 | Tool schema deterministic; unsupported OAS → fail startup (no silent non-strict) | **PASS** | `tool_gen.py` `UNSUPPORTED_KEYWORDS` → `ToolGenError`; `strict: True`; `deployment.py` → `tool_gen_failed` when `schema_id`+`schema_version` set; `tests/test_tool_gen.py` |
| 3 | Budget breach → resident-safe error, no gateway, redacted metric reason | **PASS** | `interview.py` returns `budget_breach` + `gateway_called: False`; `BudgetGuard._emit` coarse `metric_reason`; `tests/test_budgets.py` |
| 4 | Model cannot override pack / origin / URL / auth | **PASS** | `strip_server_owned_fields` + `assemble_server_body` / `run_three_gates` force server constants; `tests/test_request_assembly.py`, `test_tool_gen.py` |
| 5 | Three validation gates (AIB-REQ-02) before Send-authorized path | **PASS** | `validate_gate1/2/3` + `run_three_gates`; Send execution out of scope (04/05); unit coverage in `tests/test_request_assembly.py` |

### Scope extras

| Item | Status | Evidence |
|------|--------|----------|
| `parallel_tool_calls: false` | **PASS** | `responses_client.py`; interview asserts |
| Turn serialization | **PASS** | `SessionTurnLock` |
| Stable prefix + cache hooks | **PASS** | `build_stable_prefix`, `CacheTelemetry` |
| Channel HTTP → live model loop | **Deferred** (documented) | `channel.py` still façade stub; pipeline verified-state |
| Live OpenAI HTTP client | **Absent** | Only `RecordingResponsesClient` |
| History in Postgres | **FAIL residual** | See **G-01** |
| Timeout env enforcement | **FAIL residual** | See **G-02** |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | Scope: «local replayable history in Postgres (bundle-pinned session)». Fact: `history.py` `HistoryStore` is **in-process only** («Postgres persistence can wrap later»). Multi-instance / restart loses history; not tied to session/Postgres store from story 02. | Persist history keyed by `session_id` (+ pinned `content_bundle_hash`) in Postgres/Sqlite session store; tests for resume across process. |
| **G-02** | **Info** | Scope: enforce budget/**rate**/**timeout** env knobs. `BudgetLimits.openai_timeout_ms` + `config.aibridge_openai_timeout_ms` exist but **never checked** in `BudgetGuard` / `InterviewEngine` / any client. | Enforce timeout on Responses call path (or document WAIVE until live HTTP client); emit redacted metric on breach. |
| **G-03** | **Info** | Backlog `$storyFile` §Verified still «OpenAI client / Responses integration: **Unknown**» while modules exist; `OPENAI_STORE_RESPONSES` in config unused (assemble always forces false — OK for AC #1). | Sync backlog verified-state; optionally assert/reject `OPENAI_STORE_RESPONSES=true`. |

### Non-gaps

| Topic | Note |
|-------|------|
| Unset budget defaults (`None`) | Intentional — out of scope inventing numerics |
| Gates not called from `InterviewEngine` | AC targets Send-authorized path; library + tests suffice for story 03 |
| Full `/metrics` | Story 06 |

---

## Cited paths

- `src/aibridge/responses_client.py`, `history.py`, `interview.py`, `tool_gen.py`, `request_assembly.py`, `budgets.py`, `turn_lock.py`, `deployment.py`, `config.py`, `channel.py`
- `tests/test_responses_store_false.py`, `test_tool_gen.py`, `test_budgets.py`, `test_turn_lock.py`, `test_request_assembly.py`

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Info), G-03 (Info)
- **Critical:** 0
- **next:** **P5** disposition
