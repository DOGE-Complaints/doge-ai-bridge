# P4 Audit — STORY-AIBRIDGE-24-qa-json-schema-boundary

| Field | Value |
|-------|-------|
| **Date** | 2026-09-17T14:37:33Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-04-…/STORY-AIBRIDGE-24-qa-json-schema-boundary/STORY-AIBRIDGE-24-qa-json-schema-boundary.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-24-qa-json-schema-boundary.md` |
| **Method** | Read/Glob + live pytest VAL contract; fixture hash originals↔copies; product `app.py` BodySizeLimit + parse; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway** | **No** live Railway SUCCESS invented or claimed |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (VAL-001…018 · guide §10.2)** | **PASS (core)** — fixtures + contract; characterization VAL-014/018 capture-first; **1 Medium** residual on VAL-017 negative CL |
| **Bullrun t01–t04 Done** | **Confirmed** vs promote copies + gate PASS 2026-09-17T14:32:38Z |
| **OPEN gaps** | **0 Critical · 1 Medium · 1 Low · 3 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **20 passed** (`tests/contract/test_json_schema_boundary.py`) · contract suite **36 passed** @ 2026-09-17T14:37Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-24** | 🟢 Implemented (P3 · next P4) · pkg-000021 | **Confirmed** VAL contract; gate PASS; **this P4** → next **P5** |
| **t01** | Done — promote seed | **Confirmed** `turns-valid-private.json` package↔`tests/fixtures/channel/` **hash_eq** |
| **t02** | Done — generate VAL fixtures | **Confirmed** 17 `val-*.json` + seed; all **hash_eq**; VAL-001…018 in `matrix_ids` |
| **t03** | Done — schema boundary tests | **Confirmed** `tests/contract/test_json_schema_boundary.py` · 20 passed; must-rows + characterization |
| **t04** | Done — story gate PASS | **Confirmed** `acceptance-verification-task-aibridge-24-t04-story-gate.md` · no Railway SUCCESS |
| **pkg-000021** | Active (story 24 P3 · next P4) | `--verify` **ok 4 paths** |
| **TRACEABILITY** | VAL-001…018 → story key `covered` | **Confirmed** `TRACEABILITY-MATRIX.md` |

---

## AC matrix (`$storyFile` · guide §10.2 VAL-*)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| VAL-001 | Valid `/turns` → 200 | **PASS** | `turns-valid-private` + harness pins Bearer → 200 |
| VAL-002 | Valid `/actions` → 200\|403\|404\|409 | **PASS** | `val-valid-actions` `http_status_in`; live **404** `not_found` |
| VAL-003 | Malformed JSON → 400 `bad_request` | **PASS** | `val-malformed-json` raw |
| VAL-004 | Invalid UTF-8 → 400 | **PASS** | `val-invalid-utf8` raw_b64 |
| VAL-005 | Unknown top-level → 400 | **PASS** | `val-unknown-top-level` |
| VAL-006 | Unknown nested → 400 | **PASS** | `val-unknown-nested` |
| VAL-007 | Missing required → 422 `semantic_invalid` | **PASS** | `val-missing-required` |
| VAL-008 | `channel`≠telegram → 422 | **PASS** | `val-channel-not-telegram` |
| VAL-009 | Empty `event_id` → 422 | **PASS** | `val-empty-event-id` |
| VAL-010 | Numeric Telegram ID → 422 | **PASS** | `val-numeric-telegram-id` |
| VAL-011 | Non-decimal id fields → 422 | **PASS (user_id)** · **Info G-03** | `val-non-decimal-id` only `user_id` |
| VAL-012 | Negative group `chat_id` accepted | **PASS** | `val-negative-chat-id` → 200 |
| VAL-013 | Empty message text → 422 | **PASS** | `val-empty-message-text` |
| VAL-014 | Whitespace-only — characterization | **PASS (capture)** · **Info G-05** | marked characterization; asserts current **200** (no trim invent) |
| VAL-015 | Action token len 65 → 422 | **PASS** | `val-action-token-len-65` |
| VAL-016 | Oversize → 413; no OpenAI/DB side effect | **PASS (413+OpenAI)** · **Low G-02** | `no_openai_calls`; DB `side_effect_count` **not** asserted (probe=0) |
| VAL-017 | Invalid/**negative** Content-Length → 400 | **PARTIAL → G-01** | Non-integer → 400 `bad_request`; **negative `-1` → 422** (not asserted) |
| VAL-018 | Missing Content-Type — characterization | **PASS** | characterization; current **200** |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| TRACEABILITY story key | **PASS** | Matrix + fixture `story_keys` |
| Characterization marked (014/018) | **PASS** | notes + `characterization: true`; no silent trim/CT invent |
| Promote = copy; originals intact | **PASS** | 18/18 hash_eq |
| Nested tasks EPIC-04 | **PASS** | t01–t04 + gate |
| `tests/unit/` layer named in story | **Info G-04** | Only `tests/contract/test_json_schema_boundary.py` |
| Live Railway SUCCESS | **Not claimed** | Gate + this audit |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | Guide VAL-017 **must**: Invalid/**negative** Content-Length → 400. Fixture `val-invalid-content-length` only sends `Content-Length: not-a-number` (400). Live probe `Content-Length: -1` yields **422** `semantic_invalid` — `BodySizeLimitMiddleware` (`app.py`) `int()`-parses negatives and has **no** `length < 0` reject. Notes admit negative not separately asserted. TRACEABILITY marks VAL-017 `covered` while negative branch fails guide expected. | Add fixture/assert for negative CL expecting 400 **or** open product decision/characterization if 422 is intentional; align middleware reject/`TRACEABILITY` accordingly. |
| **G-02** | **Low** | VAL-016 expects no OpenAI/**DB** side effect. Test asserts `no_openai_calls` only. Fact: after 413, `EventDedupeStore.side_effect_count(...)==0` (probe), but unasserted. | Assert `side_effect_count==0` (or equivalent) on 413 path in contract test. |
| **G-03** | **Info** | VAL-011 wording covers `user_id`, `chat_id`, **or** `message_id`; only non-decimal `user_id` fixtured. | Optional sibling fixtures for `chat_id`/`message_id`; or WAIVE as representative OR sample. |
| **G-04** | **Info** | Story/task layer names `tests/unit/` + `tests/contract/`; **no** `tests/unit/` tree — DoD met via contract alone. | WAIVE name≠require unit folder; or add thin unit wrappers — out of core AC. |
| **G-05** | **Info** | VAL-014 capture locks 200; guide § open decision if trimming required — no named follow-up decision artifact. | Record product decision / backlog deferral when operator chooses trim policy; keep characterization until then. |

### Non-gaps

| Topic | Note |
|-------|------|
| Inventing Railway SUCCESS | Avoided |
| Moving package originals | Not done; promote=copy verified |
| Silent trim/CT invent on 014/018 | Avoided — characterization + documented 200 |
| SPA / hasUxPipeline | false — code audit only |
| Regression `tests/contract/` | **36 passed** (AUTH+VAL) |

### Regressions

| Check | Result |
|-------|--------|
| Pytest VAL contract | **20 passed** |
| Full `tests/contract/` | **36 passed** |
| Fixture originals deleted/moved | **None** |
| Characterization inventing trim/CT policy | **None** |

---

## Cited paths

- `tests/contract/test_json_schema_boundary.py`
- `tests/fixtures/channel/val-*.json`, `turns-valid-private.json`
- `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/*`
- `src/aibridge/app.py` (`parse_channel_body`, `BodySizeLimitMiddleware`, `validation_http_status`)
- Gate: `acceptance-verification-task-aibridge-24-t04-story-gate.md`
- Guide §10.2 VAL-* · TRACEABILITY-MATRIX.md

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Low), G-03/G-04/G-05 (Info)
- **Critical:** 0
- **OPEN counts:** Critical **0** · Medium **1** · Low **1** · Info **3**
- **next:** **P5** disposition
