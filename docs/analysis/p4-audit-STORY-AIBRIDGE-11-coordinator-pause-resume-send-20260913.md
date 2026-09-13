# P4 Audit — STORY-AIBRIDGE-11-coordinator-pause-resume-send

| Field | Value |
|-------|-------|
| **Date** | 2026-09-13 |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/STORY-AIBRIDGE-11-coordinator-pause-resume-send/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md` |
| **Method** | Read/Glob only; no product patches; no live pytest this pass |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (REQ-03 §4 #1,#3–#6,#8 + txn/pending)** | **PASS** on coordinator wire / pause-persist / interpret / Send frozen / stash+FCO / unknown_outcome · **residuals** below |
| **Bullrun t01–t07 Done** | **Confirmed** vs modules + gate PASS 2026-09-13T16:03:23Z |
| **OPEN gaps** | **2 Medium · 1 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **Unknown**; historical **122 passed / 14 skipped** @ P3 gate |

---

## Bullrun touchpoints (отчёт only)

| ID | Claim | P4 fact |
|----|-------|---------|
| Story 11 | 🟢 Done · awaiting P4 | **Coordinator path Done**; gates/lock residuals |
| t01–t06 | Done | **Confirmed** (`coordinator.py`, `channel.py`, `confirm.py`, tests) |
| t07 gate | Done | PASS — evidence does not cover `run_three_gates` or lock-across-HTTPS |

---

## AC matrix (`$storyFile` Target / REQ-03 §4)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| §4 #1 | `/turns` interview reply, not `Received:` | **PASS** | `process_turn_async` → `build_turn_from_engine`; `test_turn_returns_interview_not_received`; strip of `Received:` in coordinator |
| §4 #3 | FC allowlisted + **three validation gates** + persist `call_id` + no gateway before Send | **PARTIAL** | Allowlist + JSON parse + FSM state in `validate_function_calls`; persist before actions. **`run_three_gates` (AIB-REQ-02) never called from coordinator/confirm** — **G-01** |
| §4 #4 | Interpretation = state only, no gateway HTTP | **PASS** | `CONFIRM_INTERPRETATION` path; `test_interpretation_confirm_no_gateway_http` |
| §4 #5 | Send checks + atomic consume + ≤1 attempt + frozen body | **PASS** (library) | Token verify + `call_gateway` + frozen `arguments`; `test_send_uses_frozen_body_only`; attempt uniqueness via PG store (story 09) |
| §4 #6 | 201 → stashed/draft_id/url + `function_call_output` + no publish claim | **PASS** | `test_stashed_then_function_call_output_with_call_id`; `STASH_REPLY` |
| §4 #8 | Restart indeterminate delivery → no auto resend | **PASS** | `recover_stale_executing` / `recover_all_executing_attempts` on PG boot; `test_recover_stale_executing_blocks_auto_resend` |
| Target | No PG txn/lock across gateway HTTPS | **FAIL residual** | `gateway_attempt` commit-before-HTTPS OK; **`PostgresTurnLock.hold` wraps `process_action` → `call_gateway` HTTPS** — **G-02** |
| Target | Pending confirm survives separate HTTP / restart (09 store) | **PASS** (hydrate) · **Info** | Fields on `ConfirmSession` + `_persist`/`_hydrate`; memory rehydrate test — no disposable-PG restart suite for pending — **G-03** |

### Scope extras

| Item | Status | Evidence |
|------|--------|----------|
| Wire turns → engine (no stub) | **PASS** | `app.py` InterviewEngine + `channel.process_turn_async` |
| Pause before actions return | **PASS** | `persist_pending_tool` before `offer_send_confirm` |
| Wave-1 dry-run/fake only | **PASS** | Tests use Recording*; real POST out of scope → 14 |
| `process_turn_async` dedupe ordering | **Info residual** | Engine runs **before** `event_dedupe` insert — **G-03** |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | REQ-03 §4 #3: function_call «проходит три validation gate». Fact: `request_assembly.run_three_gates` / `validate_gate1/2/3` exist and are unit-tested, but Grep shows **no** call from `coordinator.py` / `confirm.py` / `channel.py`. Freeze/Send uses only allowlist + JSON + FSM. Story 03 deferred Send wiring; story 11 is that wire and still skips gates. | Call `run_three_gates` (or equivalent) when freezing FC / before Send with tool+pack+wire schemas from deployment bundle; fail-closed; tests with bad payload. |
| **G-02** | **Medium** | Target AC: no PG lock across gateway HTTPS. Fact: `process_action` holds `turn_lock.hold(session_id)` around `_work()` which includes `consume_action_token` → `call_gateway` → transport HTTPS. `create_executing` commits separately (good), but **row lock in `session_turn_lock` stays held for the whole HTTPS**. | Release turn lock before gateway HTTPS (or never acquire for Send HTTPS segment); keep one-active-turn via shorter critical section; test that lock row absent during transport.request. |
| **G-03** | **Info** | (a) `process_turn_async`: OpenAI/`arun_turn` runs, then `get_or_create` stores body — concurrent same `event_id` can double-call Responses; crash window loses replay. Sync `process_turn` is insert-once OK. (b) Pending restart evidence is in-memory hydrate, not disposable PG ConfirmSessionStore round-trip. | Claim-or-insert dedupe before engine (or transactional lease); add PG pending restart test. |

### Non-gaps

| Topic | Note |
|-------|------|
| Real `POST /story-drafts` / live n8n | Out of scope (14 / 15) |
| REQ-03 §4 #2 / #7 / #9 | Not in this story Target AC (09 / 13 / later) |
| Interpretation no gateway | Covered |

---

## Cited paths

- `src/aibridge/coordinator.py`, `channel.py`, `app.py`, `confirm.py`, `interview.py`, `gateway.py`, `request_assembly.py`
- `tests/test_story_11_coordinator.py`, `tests/test_gateway_attempt_before_https.py`, `tests/test_request_assembly.py`
- Gate: `acceptance-verification-task-aibridge-02-11-t07-…md`
- REQ-03 §4 #1,#3–#6,#8 · §5.2 · §5.3

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Medium), G-03 (Info)
- **Critical:** 0
- **OPEN counts:** Medium **2** · Info **1** · Low **0** · Critical **0**
- **next:** **P5** disposition
