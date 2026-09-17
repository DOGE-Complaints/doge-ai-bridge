# P4 Audit — STORY-AIBRIDGE-34-qa-product-journey-scenarios

| Field | Value |
|-------|-------|
| **Date** | 2026-09-17T21:25:55Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-04-…/STORY-AIBRIDGE-34-qa-product-journey-scenarios/STORY-AIBRIDGE-34-qa-product-journey-scenarios.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-34-qa-product-journey-scenarios.md` |
| **Method** | Read/Glob + live pytest `tests/integration/test_product_journey_scenarios.py`; fixture hash package↔`tests/fixtures/{spies,n8n,meta}`; code review UC asserts vs guide §11; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway / live Telegram** | **No** Railway SUCCESS · **No** live Telegram PASS invented |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (UC-01…10 · guide §11)** | **PASS (core)** — 11 envelopes + suite present; **3 Medium** residuals (PG skip gate, LIFE-009 depth, UC-07 restart) |
| **Bullrun t01–t04 Done** | **Confirmed** vs promote copies + gate PASS 2026-09-17T21:23:16Z |
| **OPEN gaps** | **0 Critical · 3 Medium · 2 Low · 3 Info** |
| **Critical OPEN** | **0** |
| **Live pytest (this P4)** | **11 skipped** (`pg_available()=False` · unix socket/`DISPOSABLE_URL`) @ 2026-09-17T21:25:55Z |
| **Gate documentary** | **11 passed** claimed @ 2026-09-17T21:23:16Z — **not reconfirmed** this session |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-34** | ✅ Done (P3 · next P4) · pkg-000033 | **Confirmed** UC packs + suite on disk; gate PASS artifact; **this P4** → next **P5** |
| **t01** | Done — compose UC-01…10 packs | **Confirmed** `uc-journey-index` + 10 UC envelopes in package `fixtures/` |
| **t02** | Done — promote=copy | **Confirmed** 11/11 hash_eq → `tests/fixtures/{spies,n8n,meta}/` |
| **t03** | Done — E2EHarness UC E2E | **Confirmed** suite exists; residual G-01…G-05; **this P4: 11 skipped** without disposable PG |
| **t04** | Done — story gate PASS | **Confirmed** acceptance 2026-09-17T21:23:16Z · UC-06/09 characterization · no Railway/live TG invent |
| **pkg-000033** | Active · 4 paths | YAML present under `aibridge-active-packages/` |
| **TRACEABILITY** | UC-01…10 → story `covered` | **Confirmed** rows; UC-06/09 char not labeled in matrix → **Info G-07** |
| **$storyFile AC** | `[x]` incl. «task-* folders not created until P1» | **Soft contradiction** (folders exist) → **Info G-08** |

---

## AC matrix (`$storyFile` / pipeline · guide §11 UC-*)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| UC-01 | dry_run_ok; zero gateway; stable session; revision after Edit; old tokens invalid | **PASS (soft)** · **Low G-03** | `test_uc_01_normal_interview_dry_run` · outcome/gateway0 · Edit→stale 404/409 · revision assert **tautology** (`!= rev0 or rev0 >= 0`) |
| UC-02 | one gateway; stashed + draft_id + URL; not-published wording | **PASS (narrow)** · **Info G-06** | `test_uc_02` · shorter than «Same as UC-01» (no Edit path) · outcome/state/draft_id/URL/gateway=1 |
| UC-03 | cancelled; no FC; no gateway; pending invalid; **LIFE-009 follow-up** | **PARTIAL → G-02** | cancel + gateway0 + stale tokens; fixture `life009_followup: true` **unread**; no post-cancel `/turns` — only `get_or_create_session` still CANCELLED |
| UC-04 | cancel before Send; no gateway; send tokens invalid; no URL | **PASS** | `test_uc_04` · cancelled · gateway0 · send 404/409 · continuation_url None |
| UC-05 | 403 forbidden; owner token consumable; no gateway | **PASS** | `test_uc_05` · attacker 403 · owner 200 · gateway0 |
| UC-06 | retry storm; one OpenAI; deterministic replay | **PASS (char)** | `characterization: true` · same `event_id` ×8 · openai_call_count=1 · replay reply_text/request_id |
| UC-07 | unknown_outcome; no auto-retry; resend blocked; **restart preserves ambiguity**; runbook | **PARTIAL → G-04** | TimeoutError → unknown_outcome · transport.calls==1 · resend 404/409; **no** rebuild/restart; **no** runbook assert |
| UC-08 | geo_scope_mismatch; no draft/URL; resident-safe message | **PASS (soft)** · **Low G-05** | outcome + draft/url null + state≠stashed; **no** reply_text resident-safe assert |
| UC-09 | adapter must not invent empty `/turns` | **PASS (char)** | fixture cross-ref `map-unsupported-media` + `message-photo-no-text` · capture-first · no product invent |
| UC-10 | raw preserved; not blind language_code; gateway `{et,ru,en}` | **PASS (soft)** · fold **Info G-06** | msgs in openai dump; `language_code` absent from `turn_body`; gateway blob soft OR for langs |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| TRACEABILITY story key | **PASS** | UC-01…10 `covered` |
| Promote = copy | **PASS** | 11/11 hash_eq (index + 10 packs) |
| Characterization marked | **PASS (fixtures)** · **Info G-07** | UC-06/09 `characterization: true` in envelopes/index; TRACEABILITY status column still plain `covered` |
| SPA / hasUxPipeline | false | |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | Entire module `pytestmark = skipif(not pg_available())` (`test_product_journey_scenarios.py:32-35`). Harness/`DISPOSABLE_URL` unix-socket only (`story13_e2e_helpers.py`). **This P4:** 11 skipped · `pg_available=False`. Gate «11 passed» not reconfirmed. Even `test_uc_fixture_packs_promoted_hash_eq` (no PG need) is skipped. No Preference A memory path for UC E2E. | Split hash_eq out of skipif; Preference A / TCP fallback; or require disposable PG in CI gate + document; or P5 WAIVE with TRACEABILITY stand-in. |
| **G-02** | **Medium** | Guide UC-03: following new resident message covered by LIFE-009. Fixture sets `life009_followup: true` but test never reads it; only asserts session still `CANCELLED` via `get_or_create_session` — no post-cancel `/turns`. | Drive LIFE-009 follow-up `/turns` assert (or mark characterization + align fixture); wire `expect.life009_followup`. |
| **G-03** | **Low** | UC-01 guide: revision change after Edit. Assert `sess2.revision != rev0 or rev0 >= 0` is always true when `rev0 >= 0`. | Assert `sess2.revision > rev0` (or ≠) after Edit without tautology OR. |
| **G-04** | **Medium** | UC-07 guide: restart preserves ambiguity; operator runbook required. Suite covers unknown_outcome + no auto-retry + resend blocked only. | `rebuild_app_same_pg` (or equiv.) UNKNOWN_OUTCOME persist; runbook path/string assert; or mark residual characterization / WAIVE. |
| **G-05** | **Low** | UC-08 guide: resident-safe message. Test omits reply_text / forbid success wording beyond outcome/ids. | Assert resident-safe reply substring / forbid «stashed/published»; or mark soft. |
| **G-06** | **Info** | UC-02 is shortened vs guide «Same as UC-01» (no Edit/revision). UC-10 gateway lang check is soft multi-OR on JSON blob. | Optional deepen UC-02 Edit path; tighten `{et,ru,en}` structural assert; or WAIVE info-nonblocking. |
| **G-07** | **Info** | Gate/index mark UC-06/09 characterization; TRACEABILITY status remains `covered` without characterization label. | Docs-only TRACEABILITY status sync. |
| **G-08** | **Info** | Backlog AC still `[x]` «task-* folders not created until P1» while t01–t04 folders exist Done. | Docs-only AC checkbox sync. |

### Non-gaps

| Topic | Note |
|-------|------|
| Inventing Railway SUCCESS / live Telegram | Avoided |
| Fixture originals moved | Not done; promote=copy verified (11) |
| Silent product invent | Avoided |
| UC-04/05/06(char)/09(char) core | Present in suite source |
| SPA / hasUxPipeline | false |

### Regressions

| Topic | Note |
|-------|------|
| vs gate t04 (11 passed) | **Cannot reconfirm** — this P4 **11 skipped** (`pg_available=False`). Not a product regression invent; environment/harness skip → **G-01**. |

---

## Cited paths

- `tests/integration/test_product_journey_scenarios.py`
- `tests/story13_e2e_helpers.py` (`pg_available`, `build_e2e_harness`, `DISPOSABLE_URL`)
- `tests/fixtures/spies/uc-*.json` · `tests/fixtures/n8n/uc-09-*.json` · `tests/fixtures/meta/uc-journey-index.json`
- `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/uc-*.json`
- Guide §11: `docs/tasks/qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`
- TRACEABILITY: `…/TRACEABILITY-MATRIX.md`
- Gate: `…/task-aibridge-34-t04-story-gate/acceptance-verification-….md`

---

## Handoff

- **OPEN gaps:** 0 Critical · **3 Medium** · **2 Low** · **3 Info**
- **OPEN IDs:** G-01, G-02, G-03, G-04, G-05, G-06, G-07, G-08
- **Product Story AC/DoD (core):** **PASS** (explicit; ≠ empty gap-list; suite source covers UC matrix when PG up)
- **next:** **P5** (disposition; do not implement in P4)
