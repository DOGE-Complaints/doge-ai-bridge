# P4 Audit — STORY-AIBRIDGE-01-channel-facade-auth

| Field | Value |
|-------|-------|
| **Date** | 2026-09-12 |
| **Mode** | `input_mode=backlog_story` (aibridge-operator-contract §6) |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** (pipeline) | `…/stories/STORY-AIBRIDGE-01-channel-facade-auth/STORY-AIBRIDGE-01-channel-facade-auth.md` |
| **$storyFile** (backlog AC SSOT) | `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md` |
| **Method** | Read/Glob only vs `src/aibridge/` + `tests/`; no product patches; no live pytest this pass |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story AC (backlog Target / AC #1–#6)** | **PASS** — факт-код и test assertions закрывают все 6 пунктов |
| **Bullrun story/task Done labels** | **Согласованы** с pipeline nested tasks + gate PASS artifact |
| **OPEN gaps (actionable)** | **1 Low** + **1 Info** (не блокируют AC Done, но требуют disposition в P5) |
| **Live pytest this pass** | **Unknown** (не запускался); gate artifact claims 21 passed @ 2026-09-12T20:35:41Z; file inventory = 21 `def test_*` |

---

## Bullrun touchpoints (статусы в отчёте — product index не переписывался)

Источник строк: `$bullrun` §STORY-AIBRIDGE-01 + pipeline nested tasks table.

| ID | Path / label | Bullrun claim | P4 fact status |
|----|--------------|---------------|----------------|
| Story | STORY-AIBRIDGE-01-channel-facade-auth | 🟢 Done | **Confirmed Done** (AC #1–#6 evidence below) |
| t01 | task-aibridge-01-01-t01-asgi-health-skeleton | Done | **Confirmed** — `app.py` `/healthz`/`/readyz`; `config.py` `PORT`; `tests/test_health.py` |
| t02 | task-aibridge-01-01-t02-channel-bearer-auth | Done | **Confirmed** — `auth.py` + middleware; equal-bearer `readyz` 503; `tests/test_auth.py` |
| t03 | task-aibridge-01-01-t03-channel-turns-actions | Done | **Confirmed** — routes + `schemas.py` `extra=forbid`; `tests/test_channel.py` |
| t04 | task-aibridge-01-01-t04-event-dedupe | Done | **Confirmed** — `dedupe.py` `get_or_create`; `tests/test_dedupe.py` |
| t05 | task-aibridge-01-01-t05-contract-tests-ack-docs | Done | **Confirmed** — `tests/test_contract_oas.py`; ack order in `docs/ops/n8n-channel-workflow/README.md` §2 + OAS description |
| t06 | task-aibridge-01-01-t06-story-acceptance-verification | Done | **Confirmed artifact** — `acceptance-verification-task-aibridge-01-01-t06-story-acceptance-verification.md` Result PASS |
| Epic | EPIC-AIBRIDGE-01-req-01-runtime | 🟡 In Progress | **Unchanged** — stories 02–06 backlog only (out of this audit scope) |

---

## AC matrix (backlog `$storyFile` Target / AC)

| # | AC (verbatim intent) | Status | Evidence (paths) |
|---|----------------------|--------|------------------|
| 1 | Unauthenticated `/v1/channel/*` → 401 | **PASS** | `src/aibridge/app.py` `channel_bearer_middleware` + `CHANNEL_PATH_PREFIX`; `tests/test_auth.py::test_unauthenticated_channel_returns_401` / `test_invalid_bearer_returns_401` |
| 2 | Valid Bearer + turn → 200 envelope per OAS; no `callback_ack_text` | **PASS** | `schemas.py` `ChannelSuccessResponse`; `channel.py` `build_stub_success`; `tests/test_channel.py::test_valid_turn_200_envelope` asserts keys + absence of `callback_ack_text` |
| 3 | Duplicate `event_id` → same stored response; no second side-effect | **PASS** | `dedupe.py` `EventDedupeStore.get_or_create`; `tests/test_dedupe.py::test_duplicate_event_id_same_response` (`side_effect_count == 1`) |
| 4 | Contract tests vs committed channel OAS | **PASS** (field/required set) | `tests/test_contract_oas.py` vs `docs/openapi/aibridge-channel-v1.openapi.yaml`; see residual **G-01** on HTTP 422 |
| 5 | Equal channel/gateway Bearer when both set → readiness fail | **PASS** | `config.py` `channel_gateway_bearers_equal`; `app.py` `/readyz` reason `channel_gateway_bearer_equal`; `tests/test_auth.py::test_equal_channel_gateway_bearer_readyz_fail` |
| 6 | Task README `Skill declared: python-pro` | **PASS** | All six `task-aibridge-01-01-t0{1-6}-*/README.md` contain `**Skill declared:** python-pro` |

### Scope extras (not numbered AC, verified)

| Scope item | Status | Evidence |
|------------|--------|----------|
| ASGI + `$PORT` | **PASS** | `src/aibridge/__main__.py` reads `PORT`; `config.py` `validation_alias="PORT"` |
| `GET /healthz`, `GET /readyz` (auth present) | **PASS** | `app.py`; `tests/test_health.py` |
| Previous-token overlap | **PASS** | `config.py` `accepted_channel_tokens`; `tests/test_auth.py::test_previous_token_overlap_accepted`; runbook `docs/runbooks/channel-bearer-rotation.md` |
| Constant-time compare | **PASS** | `auth.py` `hmac.compare_digest` / `constant_time_token_match` |
| Telegram IDs decimal strings; unknown fields; size bounds | **PASS** | `schemas.py` `_DECIMAL_ID` + `extra="forbid"`; `BodySizeLimitMiddleware` + body `len(raw)` → 413; `tests/test_channel.py` |
| No CORS | **PASS** | Grep `src/`: only `BodySizeLimitMiddleware` via `add_middleware`; **no** `CORSMiddleware` |
| Operator ack order documented | **PASS** | `docs/ops/n8n-channel-workflow/README.md` §«Operator ack order»; `docs/architecture/runtime/01-channel-facade.md`; OAS `info.description` |
| In-process dedupe only | **In scope for story 01** | Cross-instance persistence = REQ-01 §21 / later stories — **not** story AC failure |

---

## Gaps

| ID | Severity | Area | Finding | How to close (findings only — no implement) |
|----|----------|------|---------|-----------------------------------------------|
| **G-01** | **Low** | Contract / REQ AIB-CH-05 | OAS + REQ list **422** («Semantically invalid channel input»). `src/aibridge/` has **zero** `status_code=422` / `422` literals; validation failures (unknown field, non-decimal id, overlong `action_token`) return **400** (`app.py` turns/actions handlers + `validation_handler`). Contract tests assert field sets, not status matrix. | Map semantic validation to **422** per AIB-CH-05 / OAS; keep **400** for malformed JSON / unknown field if that split is required; extend `tests/test_channel.py` assertions; re-gate t05/t06. |
| **G-02** | **Info** | Docs drift (`$storyFile`) | Backlog `Verified current state` still says runtime module path **Unknown**; pipeline story + code show `src/aibridge/app.py` (`aibridge.app:app`). | Sync backlog verified-state paragraph to match pipeline; no product code change. |

### Non-gaps / out of DoD this wave

| Topic | Disposition note |
|-------|------------------|
| Persistent / multi-instance dedupe | REQ-01 §21; story 01 single-process store OK |
| Full AIB-CH-05 matrix (403/404/409/429/500) | Needs later stories (tokens/FSM/gateway); façade stub correctly returns 200 envelopes |
| Live pytest re-run | Not executed this P4; treat gate date as historical claim until re-verified |

---

## Regressions

None observed relative to story AC and committed module layout under `doge-ai-bridge/src/aibridge/` + `tests/`.

---

## Cited product / test paths

- `doge-ai-bridge/src/aibridge/app.py`
- `doge-ai-bridge/src/aibridge/auth.py`
- `doge-ai-bridge/src/aibridge/channel.py`
- `doge-ai-bridge/src/aibridge/dedupe.py`
- `doge-ai-bridge/src/aibridge/schemas.py`
- `doge-ai-bridge/src/aibridge/config.py`
- `doge-ai-bridge/src/aibridge/__main__.py`
- `doge-ai-bridge/tests/test_auth.py`
- `doge-ai-bridge/tests/test_channel.py`
- `doge-ai-bridge/tests/test_dedupe.py`
- `doge-ai-bridge/tests/test_health.py`
- `doge-ai-bridge/tests/test_contract_oas.py`
- `doge-ai-bridge/tests/conftest.py`
- `doge-ai-bridge/docs/openapi/aibridge-channel-v1.openapi.yaml`
- `doge-ai-bridge/docs/ops/n8n-channel-workflow/README.md`

---

## Handoff

- **OPEN:** G-01 (Low), G-02 (Info)
- **Critical / Medium OPEN:** 0
- **next:** **P5** disposition (CLOSED / TASKED / WAIVED) for G-01/G-02 — do not skip silently
- Product Story Done (AC) **≠** empty residual gap list — both recorded above
