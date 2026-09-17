# P4 Audit — STORY-AIBRIDGE-27-qa-openai-prompt-behavior

| Field | Value |
|-------|-------|
| **Date** | 2026-09-17T18:50:06Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-04-…/STORY-AIBRIDGE-27-qa-openai-prompt-behavior/STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md` |
| **Method** | Read/Glob + live pytest OAI integration; fixture hash package↔`tests/fixtures`; product `coordinator`/`interview`/`budgets`/`responses_client`; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway / live Telegram** | **No** Railway SUCCESS · **No** live Telegram PASS invented |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (OAI-001…016 · guide §10.5)** | **PASS (core)** — integration suite + fixtures; characterization 008/009/016; **1 Medium** residual on OAI-009 channel depth |
| **Bullrun t01–t04 Done** | **Confirmed** vs promote copies + gate PASS 2026-09-17T18:46:05Z |
| **OPEN gaps** | **0 Critical · 1 Medium · 1 Low · 3 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **18 passed** (`tests/integration/test_openai_prompt_behavior.py`) @ 2026-09-17T18:48:47Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-27** | 🟢 Implemented (P3 · next P4) · pkg-000024 | **Confirmed** OAI suite; gate PASS; **this P4** → next **P5** |
| **t01** | Done — promote seed | **Confirmed** `text-only-ru-clarify.json` hash_eq package |
| **t02** | Done — generate OAI matrix | **Confirmed** OAI-001…016 in openai/channel fixtures; copies hash_eq |
| **t03** | Done — integration tests | **Confirmed** `tests/integration/test_openai_prompt_behavior.py` · 18 passed |
| **t04** | Done — story gate PASS | **Confirmed** t04 acceptance · no Railway/live TG invent |
| **pkg-000024** | Active | `--verify` **ok 4 paths** |
| **TRACEABILITY** | OAI-001…016 → story `covered` | **Confirmed** |
| **$storyFile nested** | Meta Implemented · tasks **Done** · AC still `[ ]` | **Drift → G-03** vs pipeline Done |

---

## AC matrix (`$storyFile` / pipeline · guide §10.5 OAI-*)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| OAI-001 | 200, visible reply, interpretation buttons | **PASS (soft)** · **Low G-02** | 200 · reply contains Уточните/улиц · `actions` len≥1; labels **unasserted** (live: Looks right/Edit/Cancel) |
| OAI-002 | Empty output → bounded fallback | **PASS** | `run_turn` → `Acknowledged.` · no gateway |
| OAI-003 | `Received:` → `Acknowledged.` | **PASS** | channel 200 · `coordinator.py` strip · reply exact |
| OAI-004 | Cached tokens metric | **PASS** | `cached_input_tokens==150` · cache events |
| OAI-005 | `store` true fail-closed | **PASS** | `Settings` ValidationError `store:false` · readiness not `openai_store_not_false` |
| OAI-006 | XOR prefix vs instructions | **PASS** | `assert_prompt_xor` → `DualInstructionsError` |
| OAI-007 | `parallel_tool_calls` false | **PASS** | assemble + RecordingClient call payload false |
| OAI-008 | 429 bounded; no secret/gateway | **PASS (capture)** | transport `RATE_LIMITED` · ASGI 500 `internal_error` · gw=[] · dedupe abort · characterization |
| OAI-009 | 5xx same bounded failure | **PARTIAL → G-01** | transport `TRANSIENT_FAILURE` only; **no** ASGI/channel/gw/secret/dedupe mirror of 008 |
| OAI-010 | timeout 500 retryable; dedupe abort | **PASS** | 500 `internal_error` · store None · retry 200 · openai `oai-timeout.json` payload unused (raise stub) |
| OAI-011 | Invalid body bounded; no history/gateway | **PASS (soft)** · **Info G-05** | transport CLIENT_ERROR + ASGI 500 on `RuntimeError`; `oai-invalid-body` unused; history corruption **unasserted** |
| OAI-012 | Budget breach; no gateway; state preserved | **PASS (turns)** · **Info G-04** | `max_session_turns=0` only; state `interviewing`; input/output/call budgets unexercised |
| OAI-013 | No secret/prompt disclosure | **PASS (soft)** · **Info G-05** | scripted safe reply; forbid on body/calls/audit; no leaky-model filter probe |
| OAI-014 | Tool-looking user text as content | **PASS** | user input contains `function_call` string · no FC outcome · gw=[] |
| OAI-015 | Stable prefix identical across sessions | **PASS** | `build_stable_prefix` hash_eq · engines same system prefix |
| OAI-016 | Bundle change → new pin | **PASS (capture)** | pack_a≠pack_b prefixes; retention branch **not** invented (characterization) |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| TRACEABILITY story key | **PASS** | Matrix OAI-001…016 `covered` |
| Characterization 008/009/016 | **PASS (mark)** · **Medium G-01** on 009 depth | notes + test docstrings; 009 thinner than 008 |
| Promote = copy | **PASS** | openai + channel turns-oai-* hash_eq |
| No secrets in payloads | **PASS (paths)** | `_assert_forbid` on 001/008/011/013 |
| Nested backlog AC checkboxes | **Info G-03** | still `[ ]` while tasks Done / Meta Implemented |
| SPA / hasUxPipeline | false | |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | Guide OAI-009 **must** (same bounded failure as 429): no secret/raw, no gateway. `test_oai_009_5xx_bounded_characterization` only asserts `ProductionResponsesClient` → `TRANSIENT_FAILURE` on 503 transport. Unlike OAI-008, **no** ASGI `/v1/channel/turns` path, gateway spy, secret forbid, or dedupe-abort. TRACEABILITY marks OAI-009 `covered` while channel depth is documentary. | Mirror OAI-008 channel characterization (500 shape / gw=[] / forbid / abort) **or** tighten TRACEABILITY/notes that transport-only is the accepted capture scope. |
| **G-02** | **Low** | OAI-001 expects interpretation buttons on first interviewing response. Test asserts `len(actions) >= 1` only. Live product returns Looks right/Edit/Cancel via `offer_interpretation_confirm` — labels/kinds **unasserted**. | Assert interpretation action labels (or token kind) for first interviewing turn. |
| **G-03** | **Info** | `$storyFile` AC checkboxes still `[ ]` (incl. stale «task-* not until P1») while Meta/tasks Done and pipeline P3 closed. | Sync backlog AC checkboxes to Done (mirror STORY-26/25 pattern). |
| **G-04** | **Info** | OAI-012 wording lists input/output/call/turn budgets; suite only exercises `max_session_turns=0` via `oai-budget-breach`. `BudgetGuard.check_usage` input/output/call paths unexercised here. | Optional sibling budget fixtures; or WAIVE as representative turn-budget sample. |
| **G-05** | **Info** | `oai-invalid-body.json` / `oai-timeout.json` counted in matrix glob coverage but not loaded by behavioral asserts (OAI-011 inline/RuntimeError; OAI-010 `_RaiseClient`). OAI-011 «no history corruption» and OAI-013 leaky-model filter unproven beyond scripted safe reply. | Wire fixtures into asserts; optional history/leak probes; or mark characterization. |

### Non-gaps

| Topic | Note |
|-------|------|
| Inventing Railway SUCCESS / live Telegram | Avoided |
| Fixture originals moved | Not done; promote=copy verified |
| Characterization invent (008/016 retention) | Avoided |
| SPA / hasUxPipeline | false |

### Regressions

| Check | Result |
|-------|--------|
| Pytest OAI integration | **18 passed** |
| Fixture originals deleted/moved | **None** |
| `--project aibridge --verify` | **ok 4 paths** |

---

## Cited paths

- `tests/integration/test_openai_prompt_behavior.py`
- `tests/fixtures/openai/oai-*.json`, `tests/fixtures/channel/turns-oai-*.json`, `text-only-ru-clarify.json`
- `src/aibridge/coordinator.py` (`Received:` → `Acknowledged.`), `interview.py`, `budgets.py`, `confirm.py` (`offer_interpretation_confirm`), `responses_client.py`
- Gate: `…/task-aibridge-27-t04-story-gate/acceptance-verification-task-aibridge-27-t04-story-gate.md`
- Guide §10.5 OAI-* · TRACEABILITY-MATRIX.md

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Low), G-03/G-04/G-05 (Info)
- **Critical:** 0
- **OPEN counts:** Critical **0** · Medium **1** · Low **1** · Info **3**
- **next:** **P5** disposition
