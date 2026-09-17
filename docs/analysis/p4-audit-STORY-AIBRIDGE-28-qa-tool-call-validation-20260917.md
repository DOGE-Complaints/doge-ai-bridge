# P4 Audit — STORY-AIBRIDGE-28-qa-tool-call-validation

| Field | Value |
|-------|-------|
| **Date** | 2026-09-17T19:09:56Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-04-…/STORY-AIBRIDGE-28-qa-tool-call-validation/STORY-AIBRIDGE-28-qa-tool-call-validation.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-28-qa-tool-call-validation.md` |
| **Method** | Read/Glob + live pytest unit TOOL; fixture hash package↔`tests/fixtures`; product `coordinator`/`request_assembly`/`confirm`; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway / live Telegram** | **No** Railway SUCCESS · **No** live Telegram PASS invented |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (TOOL-001…014 · guide §10.6)** | **PASS (core)** — unit suite + fixtures; TOOL-014 characterization; **1 Medium** residual on TOOL-013 persist fail-closed |
| **Bullrun t01–t04 Done** | **Confirmed** vs promote copies + gate PASS 2026-09-17T19:07:11Z |
| **OPEN gaps** | **0 Critical · 1 Medium · 1 Low · 3 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **17 passed** (`tests/unit/test_tool_call_validation.py`) @ 2026-09-17T19:09:56Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-28** | 🟢 Implemented (P3 · next P4) · pkg-000025 | **Confirmed** TOOL suite; gate PASS; **this P4** → next **P5** |
| **t01** | Done — generate TOOL envelopes | **Confirmed** package `tool-fc-*` / gateway tool fixtures |
| **t02** | Done — promote copy | **Confirmed** openai/gateway hash_eq |
| **t03** | Done — unit tests | **Confirmed** `tests/unit/test_tool_call_validation.py` · 17 passed |
| **t04** | Done — story gate PASS | **Confirmed** t04 acceptance · no Railway/live TG invent |
| **pkg-000025** | Active | `--verify` **ok 4 paths** |
| **TRACEABILITY** | TOOL-001…014 → story `covered` | **Confirmed** |
| **$storyFile AC** | checkboxes `[x]` · tasks Done | **Aligned** (no backlog AC drift this wave) |

---

## AC matrix (`$storyFile` / pipeline · guide §10.6 TOOL-*)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| TOOL-001 | FC before Looks right → blocked; no Send/gw | **PASS** | `build_turn` · actions=[] · blocked text · transport=[] · no freeze |
| TOOL-002 | One allowlisted after confirm → gates+freeze+Send | **PASS (soft)** · **Info G-04** | Looks right consume · freeze+Send labels · transport=[]; **no** explicit three-gate spy |
| TOOL-003 | Two FCs rejected | **PASS** | `ToolValidationError` «Exactly one» · build_turn reject sample |
| TOOL-004 | Unknown tool rejected | **PASS** | «not allowlisted» |
| TOOL-005 | Missing call_id rejected | **PASS** | «missing call_id» |
| TOOL-006 | Malformed args rejected | **PASS** | «Malformed» |
| TOOL-007 | Args array/**scalar** rejected | **PASS (array)** · **Low G-02** | `tool-fc-args-array` only; scalar works in product probe, **unfixtured** |
| TOOL-008 | Gate1 type/required/enum/const/bounds | **PASS (required)** · **Info G-03** | missing narrative → gate1; other Gate1 modes **unfixtured** |
| TOOL-009 | Missing structured_payload → gate2 | **PASS** | match `gate2` |
| TOOL-010 | Pack schema violate → gate2 | **PASS** | match `gate2` |
| TOOL-011 | Wire schema violate → gate3 | **PASS** | `strict_wire=True` · match `gate3` |
| TOOL-012 | Server-owned fields stripped/replaced | **PASS** | schema_version/binding/origin constants · no `gateway_url` |
| TOOL-013 | Persist fail → no Send; fail closed | **PARTIAL → G-01** | raise before `offer_send`; gw=[]; **in-memory** `frozen_tool_intent`+`pending_call_id` remain |
| TOOL-014 | Same call_id replay → no duplicate consequential | **PASS (capture)** · **Info G-05** | remint → `IllegalTransitionError` · gw=[]; `register_session_call` unwired · `__name__` tautology |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| TRACEABILITY story key | **PASS** | Matrix TOOL-001…014 `covered` |
| Characterization TOOL-014 | **PASS (mark)** | docstring + gate notes; no invent |
| Promote = copy | **PASS** | listed openai/gateway tool fixtures hash_eq |
| No Send on reject | **PASS (sample)** | `test_reject_paths_expose_no_send_via_build_turn` (subset) |
| Gateway OAS pin | **PASS** | `tool-validation-context` oas_pin path exists |
| SPA / hasUxPipeline | false | |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | Guide TOOL-013 **must**: persist failure → no Send exposed; **fail closed**. `test_tool_013` monkeypatches `_persist_session` → `RuntimeError`; asserts gw=[] and state ≠ `AWAITING_SEND_CONFIRM`. Fact after boom: `frozen_tool_intent` set and `pending_call_id=call_tool_valid` (set in `persist_pending_tool` before persist). No rollback/clear assert; exception is the only fail-closed signal. TRACEABILITY marks TOOL-013 `covered` while durable fail-closed is partial. | Assert clean rollback (or no in-memory freeze) on persist fail; or return `actions=[]` fail-closed without leaking pending freeze; align product/test/TRACEABILITY. |
| **G-02** | **Low** | TOOL-007 wording is array/**scalar**. Suite only fixtures `tool-fc-args-array`. Product rejects scalar (`arguments` must be JSON object) in live probe — unasserted. | Add scalar fixture/parametrize sibling; keep array case. |
| **G-03** | **Info** | TOOL-008 lists type/required/enum/const/bounds; only **missing required** (`tool-fc-gate1-fail`) exercised. | Optional enum/type/bounds fixtures; or WAIVE as representative required sample. |
| **G-04** | **Info** | TOOL-002 expected «Three gates run»; test asserts freeze+Send side effects only — no spy/counter that gate1→2→3 executed (product does call `run_three_gates` in `validate_function_calls`). | Optional gate-order spy; or WAIVE as implicit via successful freeze. |
| **G-05** | **Info** | TOOL-014 characterization: remint FSM + `assert register_session_call.__name__ == "register_session_call"` tautology; PG `register_session_call` not wired into coordinator (noted). | Keep characterization; optional wire/assert real dedupe store later; drop tautology. |

### Non-gaps

| Topic | Note |
|-------|------|
| Inventing Railway SUCCESS / live Telegram | Avoided |
| Fixture originals moved | Not done; promote=copy verified |
| Characterization invent (TOOL-014 remint) | Avoided — IllegalTransition capture |
| SPA / hasUxPipeline | false |
| Backlog AC `[ ]` drift | **None** this wave (`[x]` aligned) |

### Regressions

| Check | Result |
|-------|--------|
| Pytest TOOL unit | **17 passed** |
| Fixture originals deleted/moved | **None** |
| `--project aibridge --verify` | **ok 4 paths** |

---

## Cited paths

- `tests/unit/test_tool_call_validation.py`
- `tests/fixtures/openai/tool-fc-*.json`, `tests/fixtures/gateway/tool-validation-context.json`, `tool-stash-201.json`
- `src/aibridge/coordinator.py` (`validate_function_calls`, `persist_pending_tool`, `build_turn_from_engine`), `request_assembly.py` (`run_three_gates`)
- Gate: `…/task-aibridge-28-t04-story-gate/acceptance-verification-task-aibridge-28-t04-story-gate.md`
- Guide §10.6 TOOL-* · TRACEABILITY-MATRIX.md

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Low), G-03/G-04/G-05 (Info)
- **Critical:** 0
- **OPEN counts:** Critical **0** · Medium **1** · Low **1** · Info **3**
- **next:** **P5** disposition
