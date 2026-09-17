# P4 Audit — STORY-AIBRIDGE-26-qa-idempotency-concurrency

| Field | Value |
|-------|-------|
| **Date** | 2026-09-17T18:24:20Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-04-…/STORY-AIBRIDGE-26-qa-idempotency-concurrency/STORY-AIBRIDGE-26-qa-idempotency-concurrency.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-26-qa-idempotency-concurrency.md` |
| **Method** | Read/Glob + live pytest IDEM integration; fixture hash; product `dedupe`/`channel`/`turn_lock`; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway / live Telegram** | **No** Railway SUCCESS · **No** live Telegram PASS invented |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (IDEM-001…010 · guide §10.4)** | **PASS (core)** — integration suite + spies; characterization 003/004; **1 Medium** residual on IDEM-008 assert strength |
| **Bullrun t01–t04 Done** | **Confirmed** vs fixtures + gate PASS 2026-09-17T18:21:34Z |
| **OPEN gaps** | **0 Critical · 1 Medium · 1 Low · 3 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **13 passed** (`tests/integration/test_idempotency_concurrency.py`) @ 2026-09-17T18:24Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-26** | 🟢 Implemented (P3 · next P4) · pkg-000023 | **Confirmed** IDEM suite; gate PASS; **this P4** → next **P5** |
| **t01** | Done — promote seed | **Confirmed** spies/channel/openai idem fixtures hash_eq package |
| **t02** | Done — generate IDEM matrix | **Confirmed** IDEM-001…010 in fixtures; copies present |
| **t03** | Done — integration tests | **Confirmed** `tests/integration/test_idempotency_concurrency.py` · 13 passed; barriers used |
| **t04** | Done — story gate PASS | **Confirmed** t04 acceptance · no Railway/live TG invent |
| **pkg-000023** | Active | `--verify` **ok 4 paths** |
| **TRACEABILITY** | IDEM-001…010 → story `covered` | **Confirmed** |
| **$storyFile nested** | Meta Implemented · tasks still **Todo** · AC `[ ]` | **Drift → G-02** vs pipeline Done |

---

## AC matrix (`$storyFile` / pipeline · guide §10.4 IDEM-*)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| IDEM-001 | Same event twice → one OpenAI | **PASS** | `test_idem_001` · `openai.calls==1` · side_effect==1 · equal bodies |
| IDEM-002 | New event_id → second OpenAI (wrong retry demo) | **PASS** | `test_idem_002` · calls==2 |
| IDEM-003 | Same event / different body → first wins | **PASS (capture)** | first-wins + no 2nd side effect; collision-log **not** implemented (characterization) |
| IDEM-004 | Concurrent identical → one OpenAI | **PASS (capture)** | Barrier; calls==1; same `request_id` **or** in-flight text |
| IDEM-005 | OpenAI exception after claim → abort; retry OK | **PASS** | 5xx then 200; side_effect 0→1 |
| IDEM-006 | Callback retry same update → one gateway | **PASS** | equal envelopes · `transport.calls==1` |
| IDEM-007 | Concurrent Send same token → one gateway; other conflict | **PASS (soft)** · **Info G-05** | gateway==1; `409 in statuses or single 200` |
| IDEM-008 | Same session concurrent → serialized; history order | **PARTIAL → G-01** | 2 OpenAI + both 200; assert `is_active(…) is False or True` **tautology**; no history-order proof |
| IDEM-009 | Diff sessions concurrent → independent | **PASS** | Barrier; both 200; calls==2 |
| IDEM-010 | turns+actions same event_id → safe replay | **PASS** | actions returns turns envelope; gateway==0 |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| TRACEABILITY story key | **PASS** | Matrix + fixture `story_keys` |
| Characterization 003/004 | **PASS** | capture-first notes/flags; no invent |
| Promote = copy | **PASS** | idem fixtures hash_eq |
| Barriers not sleep | **PASS** | `threading.Barrier` |
| Spy bag §14 patterns only | **PASS (static)** · **Low G-03** | patterns forbid secrets; `_assert_forbid` never applied to live logs |
| Memory vs disposable PG | **Info G-04** | Suite uses `EventDedupeStore` + injected `SessionTurnLock`; default memory `app.state.turn_lock is None` (PG wires `PostgresTurnLock`) |
| Nested backlog tasks/AC | **Info G-02** | Still Todo / `[ ]` while P3 Done |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | IDEM-008 guide: session lock serializes; history order deterministic. `test_idem_008_same_session_serialized_by_turn_lock` ends with `assert lock.is_active(...) is False or True` (always true). Proves two completions + 2 OpenAI calls only — not lock exclusivity / ordered history. | Assert non-overlapping hold (e.g. max concurrent `_active` / engine history sequence) under barrier; drop tautology. |
| **G-02** | **Info** | `$storyFile` nested tasks still **Todo** and AC checkboxes `[ ]` while Meta/pipeline/bullrun say P3 Done — SSOT drift for operator package. | Sync backlog nested Status/AC to Done (mirror STORY-25/24 pattern). |
| **G-03** | **Low** | `_assert_forbid` defined but never called; spy `forbid_substrings_in_logs` only statically checked for pattern hygiene, not against captured logs during IDEM runs. | Capture log bag on key paths and assert forbid patterns; or drop dead helper. |
| **G-04** | **Info** | Story harness names disposable PG; suite is memory-dedupe + optional in-process lock. Default ASGI memory path has `turn_lock=None` (`app.py`); PG lock path unexercised here. | Optional disposable-PG IDEM matrix; or WAIVE as memory characterization sufficient for story DoD. |
| **G-05** | **Info** | IDEM-007 expected conflict for loser; assert allows `409` **or** sole `200` while requiring `gateway_call_count==1`. | Tighten to require conflict status when product guarantees it; or mark characterization for dual outcome. |

### Non-gaps

| Topic | Note |
|-------|------|
| Inventing Railway SUCCESS / live Telegram | Avoided |
| Fixture originals moved | Not done; promote=copy verified |
| Characterization invent (003/004) | Avoided |
| SPA / hasUxPipeline | false |

### Regressions

| Check | Result |
|-------|--------|
| Pytest IDEM integration | **13 passed** |
| Fixture originals deleted/moved | **None** |

---

## Cited paths

- `tests/integration/test_idempotency_concurrency.py`
- `tests/fixtures/spies/idem-*.json`, `tests/fixtures/channel/*idem*`
- `src/aibridge/dedupe.py`, `channel.py`, `turn_lock.py`, `app.py` (turn_lock wiring)
- Gate: `…/task-aibridge-26-t04-story-gate/acceptance-verification-task-aibridge-26-t04-story-gate.md`
- Guide §10.4 IDEM-* · TRACEABILITY-MATRIX.md

---

## Handoff

- **OPEN:** G-01 (Medium), G-03 (Low), G-02/G-04/G-05 (Info)
- **Critical:** 0
- **OPEN counts:** Critical **0** · Medium **1** · Low **1** · Info **3**
- **next:** **P5** disposition
