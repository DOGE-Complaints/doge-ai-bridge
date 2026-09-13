# P4 Audit — STORY-AIBRIDGE-12-readyz-env-dryrun-gate

| Field | Value |
|-------|-------|
| **Date** | 2026-09-13 |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/STORY-AIBRIDGE-12-readyz-env-dryrun-gate/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md` |
| **Method** | Read/Glob only; no product patches; no live pytest this pass |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story AC #1–#3** | **PASS** on `/readyz` strict core · dry-run gate · bounded 500 · **§5.6 residual** |
| **Bullrun t01–t06 Done** | **Confirmed** vs modules + gate PASS 2026-09-13T16:22:32Z |
| **OPEN gaps** | **1 Medium · 2 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **Unknown**; historical **136 passed / 15 skipped** @ P3 gate |

---

## Bullrun touchpoints (отчёт only)

| ID | Claim | P4 fact |
|----|-------|---------|
| Story 12 | 🟢 Done · awaiting P4 | **readyz/dry-run/500 Done**; knobs enforce residual |
| t01–t05 | Done | **Confirmed** (`config`, `readiness`, app handlers, tests) |
| t06 gate | Done | PASS |

---

## AC matrix (`$storyFile`)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | REQ-03 §5.5 and §5.6 satisfied | **PARTIAL** | **§5.5 mostly PASS** — `evaluate_readiness`: auth, bearers, HTTPS origin, conflict, redirect, OpenAI presence, store:false, dry-run, content when configured, tool path presence, PG migration SELECT. No OpenAI gen / gateway write. **§5.6 PARTIAL** — canonical `DOGESTONIA_API_BASE_URL` + documented alias; Settings **accept** TTL/timeouts/log/rate/budgets; `.env.example` lists names. **Enforceable when set:** mostly **not** wired — **G-01** |
| 2 | Dry-run readiness gate until story 14 P1-03 | **PASS** | `dry_run_required` unless `AIBRIDGE_SCHEMA_VALIDATION_COMPLETE`; `test_dry_run_false_fails_readyz_until_schema_complete` |
| 3 | Unhandled → bounded channel JSON 500 (OpenAPI) | **PASS** | Channel `Exception` handler → `error_body(internal_error)`; `test_unhandled_channel_exception_returns_bounded_500` |

### Scope / §5.5–5.6 extras

| Item | Status | Evidence |
|------|--------|----------|
| Canonical base URL + alias conflict | **PASS** | `resolved_gateway_base_url` / `gateway_base_url_conflict`; executor uses canonical; tests |
| PG connectivity + migration version | **PASS** | `_postgres_migration_ok` SELECT-only |
| Tool generation + strict schema | **Info residual** | `_tool_schema_ok` = file non-empty if path set; **no** `generate_strict_tool` — **G-02** |
| Optional probes read-only | **PASS** | Migration check is SELECT; no gateway POST |
| `.env.example` parity | **PASS** (names) | Alias docs + dry-run + schema flag + knobs |
| Backlog Verified current state | **Info** | Still P1 soft wording — **G-03** |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | REQ-03 §5.6: knobs «wired and enforceable when set». Fact: Settings parse TTL, max response bytes, HTTP connect/total timeouts, log level, rate limits, LLM budgets (`config.py`). Runtime: Grep `src/aibridge` shows **no** consumers of `aibridge_session_ttl_seconds`, `aibridge_action_token_ttl_seconds`, `aibridge_http_connect_timeout_ms`, `aibridge_http_total_timeout_ms`, `aibridge_max_response_bytes`, `aibridge_log_level`, rate limits, or budget fields except `aibridge_openai_timeout_ms` on `ProductionResponsesClient`. `InterviewEngine.budgets` stays unset in `create_app`. Setting knobs has no effect. | Wire BudgetGuard/token TTL/timeouts/max response/log/rate from Settings when non-None; unit tests that env values change behavior; rate-limit 429 may align with R3-P1-02 but budget/TTL/timeouts fit this story. |
| **G-02** | **Info** | §5.5 lists «tool generation and strict schema». Fact: readiness only checks tool schema **file presence** when path set; empty path → ready. Does not run `generate_strict_tool` / strict object checks. | Optional: call generate/strict verify when content+tool paths configured; or document file-presence as interim until 14. |
| **G-03** | **Info** | `$storyFile` §Verified current state still describes soft `/readyz` and «gate vs readiness not yet» while post-P3 code contradicts. | Sync backlog verified-state to post-P3 facts (docs-only). |

### Non-gaps

| Topic | Note |
|-------|------|
| Full schema validation / live stash readiness | Out of scope → STORY-14 (R3-P1-03); lift via `AIBRIDGE_SCHEMA_VALIDATION_COMPLETE` |
| Inventing numeric budget defaults | Explicitly out of scope |
| Dry-run false → 503 | Covered |

---

## Cited paths

- `src/aibridge/readiness.py`, `config.py`, `app.py`, `gateway.py`
- `.env.example`
- `tests/test_story_12_readyz_env.py`
- Gate: `acceptance-verification-task-aibridge-02-12-t06-…md`
- REQ-03 §2 · §5.5 · §5.6 · P0-11

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Info), G-03 (Info)
- **Critical:** 0
- **OPEN counts:** Medium **1** · Info **2** · Low **0** · Critical **0**
- **next:** **P5** disposition
