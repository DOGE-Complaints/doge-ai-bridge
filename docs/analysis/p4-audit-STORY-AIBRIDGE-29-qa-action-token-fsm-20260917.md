# P4 Audit — STORY-AIBRIDGE-29-qa-action-token-fsm

| Field | Value |
|-------|-------|
| **Date** | 2026-09-17T19:32:26Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-04-…/STORY-AIBRIDGE-29-qa-action-token-fsm/STORY-AIBRIDGE-29-qa-action-token-fsm.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-29-qa-action-token-fsm.md` |
| **Method** | Read/Glob + live pytest unit+integration ACT; fixture hash package↔`tests/fixtures`; product `confirm`/`action_tokens`/`pg_runtime`; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway / live Telegram** | **No** Railway SUCCESS · **No** live Telegram PASS invented |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (ACT-001…018 · guide §10.7)** | **PASS (core)** — unit+HTTP suites + spies; **1 Medium** residual on ACT-017 PG/logs depth |
| **Bullrun t01–t04 Done** | **Confirmed** vs promote copies + gate PASS 2026-09-17T19:30:03Z |
| **OPEN gaps** | **0 Critical · 1 Medium · 1 Low · 3 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **26 passed** (`tests/unit/test_action_token_fsm.py` + `tests/integration/test_action_token_fsm_http.py`) @ 2026-09-17T19:32:26Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-29** | 🟢 Implemented (P3 · next P4) · pkg-000026 | **Confirmed** ACT suites; gate PASS; **this P4** → next **P5** |
| **t01** | Done — generate ACT envelopes | **Confirmed** channel/spies act-* in package fixtures |
| **t02** | Done — promote copy | **Confirmed** hash_eq listed CHANNEL_NAMES/SPIES_NAMES |
| **t03** | Done — unit+integration | **Confirmed** 26 passed |
| **t04** | Done — story gate PASS | **Confirmed** t04 acceptance · no Railway/live TG invent |
| **pkg-000026** | Active | `--verify` **ok 4 paths** |
| **TRACEABILITY** | ACT-001…018 → story `covered` | **Confirmed** |
| **$storyFile AC** | checkboxes `[x]` · tasks Done | **Aligned** |

---

## AC matrix (`$storyFile` / pipeline · guide §10.7 ACT-*)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| ACT-001 | Looks right → 200; interpretation_confirmed; gw=0 | **PASS** | unit + HTTP · spy `act-looks-right-zero-gw` · transport=[] |
| ACT-002 | Edit → interviewing; revision++; siblings 409 | **PASS** | unit · spy `act-edit-no-gw` · sibling 409 · gw=[] |
| ACT-003 | Cancel → cancelled; invalidate; gw=0 | **PASS** | unit · spy `act-cancel-no-gw` |
| ACT-004 | Send → one authorized frozen body | **PASS** | unit · `transport.calls==1` · `json_body==frozen` |
| ACT-005 | Random → 404 not_found | **PASS** | unit + HTTP |
| ACT-006 | Foreign user → 403 | **PASS** | unit + HTTP |
| ACT-007 | Foreign chat → 403 | **PASS** | unit + HTTP |
| ACT-008 | Expired → 409 | **PASS** | unit + HTTP · `expires_at` mutated (not fake clock) |
| ACT-009 | Consumed + new event_id → 409 | **PASS** | unit re-consume · HTTP distinct event_id |
| ACT-010 | Invalidated sibling → 409 | **PASS** | unit after cancel |
| ACT-011 | Revision mismatch → 409 | **PASS** | unit · message contains revision |
| ACT-012 | Expected state mismatch → 409 | **PASS** | unit · message contains state |
| ACT-013 | Deployment mismatch → 409 (Send) | **PASS** | unit Send path · deployment in message |
| ACT-014 | Draft hash mismatch → 409 (Send) | **PASS** | unit · draft in message |
| ACT-015 | Frozen missing → 409; gw=0 | **PASS** | unit · frozen in message · transport=[] |
| ACT-016 | Illegal FSM → 409 | **PASS (soft)** · **Info G-05** | forced `expected_state` rewrite; soft OR on message/code |
| ACT-017 | Raw in PG/logs → fail; hash only | **PARTIAL → G-01** | memory `ActionTokenStore` only; **no** PG/`PostgresActionTokenStore`; **no** logs assert; spy `forbid_substrings_in_store_keys` unread |
| ACT-018 | Token >64 → 422 façade; mint ≤64 | **PASS** | HTTP 422 · unit mint loop ≤64 |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| TRACEABILITY story key | **PASS** | Matrix ACT-001…018 `covered` |
| Promote = copy | **PASS** | CHANNEL_NAMES + SPIES_NAMES hash_eq |
| Zero gw Looks right/Edit/Cancel | **PASS** | transport.calls==[] |
| HTTP façade breadth | **Info G-03** | HTTP covers 001/005–009/018 only |
| Channel PLACEHOLDER envelopes | **Low G-02** | many `act-*.json` only hash/matrix; behavioral mints live tokens |
| Fake clock harness claim | **Info G-04** | TTL via direct `expires_at` mutation |
| SPA / hasUxPipeline | false | |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | Guide ACT-017 **must**: raw token in **PostgreSQL/logs** fails security test; only hash persists. `test_act_017` uses in-memory `ActionTokenStore` (`raw not in _by_hash`). Product has `PostgresActionTokenStore` (`pg_runtime.py`) — **unexercised** here. Spy `act-hash-only-persist` declares `forbid_substrings_in_store_keys` but test never reads it; **no** audit/log bag assert. TRACEABILITY marks ACT-017 `covered` while PG+logs branch is documentary. | Disposable-PG hash-only insert/select + log forbid of raw token; assert spy fields; or mark characterization memory-only and align TRACEABILITY. |
| **G-02** | **Low** | Channel fixtures `act-edit`…`act-illegal-fsm` etc. carry `action_token: PLACEHOLDER_TOKEN` and expect blocks, but behavioral tests mint live tokens and ignore those bodies (except coverage hash_eq). Fixture expect SSOT unused. | Drive HTTP/unit from fixture expect after mint-replace; or mark envelopes matrix-only. |
| **G-03** | **Info** | Story layer names unit+integration; HTTP suite omits ACT-002/003/004/010–016 (unit-only). | Optional HTTP siblings; or WAIVE unit depth sufficient. |
| **G-04** | **Info** | Story harness names fake clock for TTL; ACT-008 mutates `expires_at` in-place. | Optional injectable clock; or WAIVE mutation as sufficient TTL proof. |
| **G-05** | **Info** | ACT-016 setup rewrites `rec.expected_state` to force illegal transition; assert allows message «transition» **or** generic conflict code. | Tighten FSM path without rewriting expected_state; or mark characterization. |

### Non-gaps

| Topic | Note |
|-------|------|
| Inventing Railway SUCCESS / live Telegram | Avoided |
| Fixture originals moved | Not done; promote=copy verified |
| Silent product invent | Avoided |
| SPA / hasUxPipeline | false |
| Backlog AC `[ ]` drift | **None** (`[x]` aligned) |

### Regressions

| Check | Result |
|-------|--------|
| Pytest ACT unit+integration | **26 passed** |
| Fixture originals deleted/moved | **None** |
| `--project aibridge --verify` | **ok 4 paths** |

---

## Cited paths

- `tests/unit/test_action_token_fsm.py`, `tests/integration/test_action_token_fsm_http.py`
- `tests/fixtures/channel/act-*.json`, `tests/fixtures/spies/act-*.json`
- `src/aibridge/confirm.py`, `action_tokens.py`, `pg_runtime.py` (`PostgresActionTokenStore`)
- Gate: `…/task-aibridge-29-t04-story-gate/acceptance-verification-task-aibridge-29-t04-story-gate.md`
- Guide §10.7 ACT-* · TRACEABILITY-MATRIX.md

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Low), G-03/G-04/G-05 (Info)
- **Critical:** 0
- **OPEN counts:** Critical **0** · Medium **1** · Low **1** · Info **3**
- **next:** **P5** disposition
