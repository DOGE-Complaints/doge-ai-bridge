# P4 Audit — STORY-AIBRIDGE-04-dual-confirm-tokens

| Field | Value |
|-------|-------|
| **Date** | 2026-09-12 |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/STORY-AIBRIDGE-04-dual-confirm-tokens/STORY-AIBRIDGE-04-dual-confirm-tokens.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-04-dual-confirm-tokens.md` |
| **Method** | Read/Glob only; no product patches; no live pytest this pass |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story AC #1–#5** | **PASS** (unit + `/actions` HTTP tests) |
| **Bullrun t01–t06 Done** | **Confirmed** vs modules + gate PASS 2026-09-12T21:40:45Z |
| **OPEN gaps** | **1 Medium** + **1 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **Unknown**; historical 70 passed / 1 skipped @ gate |

---

## Bullrun touchpoints (отчёт only)

| ID | Claim | P4 fact |
|----|-------|---------|
| Story 04 | 🟢 Done | **AC Done**; residuals below |
| t01 confirm-fsm-states | Done | **Confirmed** — `confirm_fsm.py`; `tests/test_confirm_fsm.py` |
| t02 interpret-vs-send-gate | Done | **Confirmed** — `confirm.py`; `tests/test_interpret_vs_send.py` |
| t03 action-token-store | Done | **Confirmed** — `action_tokens.py`; `tests/test_action_tokens.py` |
| t04 edit-cancel-ownership | Done | **Confirmed** — `tests/test_edit_cancel_ownership.py` |
| t05 actions-fail-closed-4xx | Done | **Confirmed** — `app.py` `/actions`; `tests/test_actions_fail_closed.py` |
| t06 acceptance | Done | Gate artifact PASS |

---

## AC matrix (`$storyFile`)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | Interpretation confirm produces no gateway HTTP | **PASS** | `consume_action_token` CONFIRM_INTERPRETATION sets `gateway_authorized=False`; no HTTP client; `tests/test_interpret_vs_send.py::test_interpretation_confirm_no_gateway` |
| 2 | Invalid / expired / foreign / consumed → 4xx fail closed | **PASS** | Map 403/404/409 in `confirm.py` + `app.py`; `tests/test_actions_fail_closed.py` |
| 3 | Callback payload opaque token ≤64 UTF-8 bytes | **PASS** | `mint_opaque_token` + assert; OAS `action_token` max 64; `tests/test_action_tokens.py` |
| 4 | Content edit increments revision; invalidates prior Send tokens | **PASS** | `apply_edit` → `revision+=1` + `invalidate_session_revision`; `tests/test_edit_cancel_ownership.py` |
| 5 | Tool intent alone ≠ Send permission | **PASS** | `authorize_from_tool_intent_alone` → `False`; Send requires consume + frozen intent; `tests/test_interpret_vs_send.py` |

### Scope extras

| Item | Status | Evidence |
|------|--------|----------|
| FSM AIB-CONF-01A | **PASS** | `confirm_fsm.py` states/transitions; illegal → fail closed |
| Only Send authorizes gateway call site | **PASS** | `call_gateway` requires `gateway_authorized`; real HTTP **Absent** (story 05) |
| Store hash not raw | **PASS** | `ActionTokenStore` keys by SHA-256 |
| Bind principal / session / revision / expiry | **PASS** (fields present) | `TokenRecord`; residual draft-hash/nonce → **G-02** |
| Persist tokens/sessions across process | **FAIL residual** | See **G-01** |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | `ActionTokenStore` and `ConfirmationGuard._sessions` are **in-process only** (`action_tokens.py`: «Postgres persistence later»). Restart / multi-instance loses pending tokens and confirm FSM; not shared with story-02 session/Postgres adapters. | Persist token hashes + confirm session/revision/state via Sqlite/Postgres adapters; tests for resume after reopen. |
| **G-02** | **Info** | REQ-01 Send binding language includes revision/**hash** and **nonce**; `TokenRecord` binds `revision` + `operation_id` but **no** draft-hash / nonce fields. Story AC #1–#5 still PASS. | Extend token bind domain (draft hash + nonce) when wiring Send → gateway (story 05) or pointed follow-up. |

### Non-gaps

| Topic | Note |
|-------|------|
| Live gateway HTTP | Explicitly out of scope (05); call-site counter only |
| Interview auto-offer of confirm buttons | Wave-1 helper APIs exist; channel turns create session without auto-mint — not AC fail |
| Full SPA E2E | Arch wave-2 |

---

## Cited paths

- `src/aibridge/confirm_fsm.py`, `action_tokens.py`, `confirm.py`, `channel.py`, `app.py`, `schemas.py`
- `tests/test_confirm_fsm.py`, `test_interpret_vs_send.py`, `test_action_tokens.py`, `test_edit_cancel_ownership.py`, `test_actions_fail_closed.py`

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Info)
- **Critical:** 0
- **next:** **P5** disposition
