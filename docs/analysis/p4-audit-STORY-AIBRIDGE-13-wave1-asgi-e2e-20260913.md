# P4 Audit — STORY-AIBRIDGE-13-wave1-asgi-e2e

| Field | Value |
|-------|-------|
| **Date** | 2026-09-13 |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/STORY-AIBRIDGE-13-wave1-asgi-e2e/STORY-AIBRIDGE-13-wave1-asgi-e2e.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md` |
| **Method** | Read/Glob only; no product patches; no live pytest this pass |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (suite / §4 #1–#9 / zero real stash)** | **PASS** on serial ASGI E2E happy path · **residuals** below |
| **Bullrun t01–t06 Done** | **Confirmed** vs tests + gate PASS 2026-09-13T16:49:42Z |
| **OPEN gaps** | **1 Medium · 2 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **Unknown**; historical **170 passed / 1 skipped** @ P3 gate |

---

## Bullrun touchpoints (отчёт only)

| ID | Claim | P4 fact |
|----|-------|---------|
| Story 13 | 🟢 Done · awaiting P4 | Harness + AC suite present; PG ASGI dedupe residual |
| t01–t05 | Done | **Confirmed** (`story13_e2e_helpers.py`, `test_story_13_wave1_asgi_e2e.py`) |
| t06 gate | Done | PASS · 170/1 · verify 6 paths |

---

## AC matrix (`$storyFile` Target · REQ-03 §4 #1–#9)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| Target 1 | E2E green without `"Received:"` | **PASS** | `test_story_13_e2e_turns_interview_not_received` |
| §4 #1 | `/turns` interview reply, not `Received:` | **PASS** | Same + `RecordingResponsesClient` scripted text |
| §4 #2 | Same `(channel, event_id)` → no 2nd Responses; stored body; restart | **PASS (serial)** · **PARTIAL residual** | `test_story_13_e2e_transport_replay_stored_status_body` + `…_replay_survives_restart`. **G-01**: ASGI+`PostgresEventDedupeStore` has no `try_begin` — peek-then-engine; concurrent / crash-before-insert not covered |
| §4 #3 | FC allowlist + three gates + `call_id` + no gateway until Send | **PASS** | Harness sets `ValidationContext`; FC → `AWAITING_SEND_CONFIRM` + `pending_call_id` / assembled args; `transport.calls == []` until Send |
| §4 #4 | Interpretation → state only, no gateway | **PASS** | `test_story_13_e2e_fc_interpretation_no_gateway` |
| §4 #5 | Send checks + atomic consume + ≤1 attempt + frozen body | **PASS (happy path)** · **Info** | Fake Send → one transport call + stash. Owner/hash/double-consume negatives stay in story 11 unit — **G-03** |
| §4 #6 | 201 → stashed/`draft_id`/url + FCO + no publish claim; dry-run zero HTTPS | **PASS** | `test_story_13_e2e_send_fake_stash_and_fco` · `…_send_dryrun_zero_real_https`; origin `gateway.example.invalid` |
| §4 #7 | Restart pending-confirm preserves buttons/state | **PASS** | `test_story_13_e2e_restart_pending_confirm_preserves_state` (PG session + pre-restart Send token) |
| §4 #8 | Restart indeterminate delivery → no auto-resend | **PASS** | `test_story_13_e2e_restart_unknown_outcome_no_auto_resend`; `create_app` → `recover_all_executing_attempts` |
| §4 #9 | Every success/replay/non-2xx conforms to channel OpenAPI | **PASS (subset)** · **Info** | `assert_channel_success_conforms` / `_error_conforms` vs OAS required keys; non-2xx sample = **401 only** — **G-02** |
| Target 3 | Zero real gateway stash in wave-1 proof | **PASS** | `RecordingGatewayTransport` / dry-run; no live Railway |

### Scope extras

| Item | Status | Evidence |
|------|--------|----------|
| Disposable Postgres harness | **PASS** | `.pgdata-test` · `scripts/start-disposable-pg.sh` · `pytest.mark.skipif(not pg_available())` |
| OpenAPI SSOT path | **PASS** | `docs/openapi/aibridge-channel-v1.openapi.yaml` loaded in helpers |
| `GatewayAttemptStore.get` / `list_executing` commit | **PASS** | `pg_runtime.py` `finally: commit` (TRUNCATE-safe) |
| Live Telegram / real gateway / SPA | Out of scope | → 15 / 14 / 17 |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | REQ-03 §4 #2 + R3-P0-12 ASGI+Postgres: production ASGI uses `process_turn_async` + `PostgresEventDedupeStore`. In-memory `EventDedupeStore` has `try_begin`/`complete` (story 11 G-03). **PG store has neither** — async path takes «Legacy stores: peek then proceed». Serial E2E replay/restart **PASS**; concurrent same `event_id` can double-call Responses; crash between engine and `get_or_create` loses claim-before-insert. Also: turn route always `JSONResponse(status_code=200)` — stored `http_status` from PG row is not applied on replay (vacuous while turns are always 200). | Add `try_begin`/`complete`/`abort` (or equivalent row lease) on `PostgresEventDedupeStore`; wire ASGI to claim before engine; optional concurrent E2E; optionally return stored status from peek. |
| **G-02** | **Info** | §4 #9 claims OpenAPI conformance for success/replay/non-2xx. Fact: helpers assert required key sets (+ action style enum) against OAS `required`, not full JSON Schema / response code matrix. Suite samples non-2xx only via unauthenticated **401**. | Optional: jsonschema against components; add 409/429/500 samples if wave-1 proof must cite full matrix. |
| **G-03** | **Info** | §4 #5 «owner/chat/session/…/atomic consume» demonstrated only as happy-path Send in E2E. Fail-closed facets (wrong owner, expired token, second consume, mutated frozen body) remain story-11 unit coverage, not wave-1 ASGI+PG. | Optional E2E negatives on disposable PG; or document dependence on STORY-11 tests in Verified state. |

### Non-gaps

| Topic | Note |
|-------|------|
| Real `POST /story-drafts` / live n8n / SPA device | Out of scope (14 / 15 / 17) |
| Three gates library wiring | In scope of 11; E2E injects `ValidationContext` and freezes assembled body |
| Turn lock across HTTPS | Closed in 11 P7 (`finish_deferred_gateway` after hold) |
| Suite skip without `.pgdata-test` | Expected gate precondition; P3 ran with PG up |

---

## Cited paths

- `tests/story13_e2e_helpers.py`, `tests/test_story_13_wave1_asgi_e2e.py`
- `src/aibridge/channel.py` (`process_turn_async`), `app.py`, `pg_runtime.py` (`PostgresEventDedupeStore`, `GatewayAttemptStore`)
- `src/aibridge/dedupe.py` (`try_begin` — memory only)
- `docs/openapi/aibridge-channel-v1.openapi.yaml`
- Gate: `acceptance-verification-task-aibridge-02-13-t06-story-acceptance-verification.md`
- REQ-03 §2 · §4 AC #1–#9 · R3-P0-12

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Info), G-03 (Info)
- **Critical:** 0
- **OPEN counts:** Medium **1** · Info **2** · Low **0** · Critical **0**
- **next:** **P5** disposition
