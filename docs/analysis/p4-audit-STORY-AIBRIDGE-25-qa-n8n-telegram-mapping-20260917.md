# P4 Audit — STORY-AIBRIDGE-25-qa-n8n-telegram-mapping

| Field | Value |
|-------|-------|
| **Date** | 2026-09-17T17:48:03Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-04-…/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md` |
| **Method** | Read/Glob + live pytest `tests/n8n/`; fixture hash package↔tests; ops README §2–§3 cross-check; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway / live Telegram** | **No** Railway SUCCESS · **No** live Telegram PASS invented or claimed |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (N8N-001…018 · guide §10.3)** | **PASS (core)** — fixture-driven mapping + ack_order; characterization 009/011; **1 Medium** residual on N8N-014 depth |
| **Bullrun t01–t04 Done** | **Confirmed** vs promote copies + gate PASS 2026-09-17T17:44:23Z |
| **OPEN gaps** | **0 Critical · 1 Medium · 1 Low · 3 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **19 passed** (`tests/n8n/` · `--noconftest`) @ 2026-09-17T17:48Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-25** | 🟢 Implemented (P3 · next P4) · pkg-000022 | **Confirmed** N8N fixtures+tests; gate PASS; **this P4** → next **P5** |
| **t01** | Done — promote seed | **Confirmed** `message-private-ru-pothole` + `callback-ack-before-actions` hash_eq; package originals intact |
| **t02** | Done — generate N8N matrix | **Confirmed** telegram/n8n/channel linked envelopes; N8N-001…018 in `matrix_ids`; copies hash_eq |
| **t03** | Done — `tests/n8n/` mapping tests | **Confirmed** `tests/n8n/test_n8n_telegram_mapping.py` · 19 passed; no live TG |
| **t04** | Done — story gate PASS | **Confirmed** `acceptance-verification-task-aibridge-25-t04-story-gate.md` · no Railway/live TG invent |
| **pkg-000022** | Active (story 25 P3 · next P4) | `--verify` **ok 4 paths** |
| **TRACEABILITY** | N8N-001…018 → story key `covered` | **Confirmed** |

---

## AC matrix (`$storyFile` · guide §10.3 N8N-*)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| N8N-001 | Private text → `/turns`; one reply | **PASS (map)** · **Low G-02** | `map-private-text` → `map_telegram_message_to_turns` == `channel.turns-from-private-ru`; `one_reply` **unasserted** |
| N8N-002 | `/start` as ordinary text | **PASS** | `map-start-command` · `expected_turns_text` `/start` |
| N8N-003 | RU unicode preserved | **PASS** | `map-unicode-ru` · text round-trip |
| N8N-004 | ET unicode preserved | **PASS** | `map-unicode-et` |
| N8N-005 | Mixed-lang; hint≠override text | **PASS** | `map-mixed-lang` · `hint_must_not_override_text` |
| N8N-006 | Emoji/combining round-trip | **PASS** | `map-emoji` |
| N8N-007 | Group user A principal | **PASS** | `map-group-user-a` · `expect_principal` |
| N8N-008 | Group user B separate session | **PASS** | `map-group-user-b` · principal ≠ A |
| N8N-009 | Edited ≠ ordinary (characterization) | **PASS** | capture-first; `edited_message` present; skip ordinary turns |
| N8N-010 | Media w/o text → no invalid `/turns` | **PASS (photo)** · **Info G-04** | `map-unsupported-media` photo only; no document/voice fixtures |
| N8N-011 | Caption characterization | **PASS** | no invent caption-as-text; undocumented |
| N8N-012 | Channel post/poll/shipping skip | **PASS (channel_post)** · **Info G-03** | only `update-channel-post`; poll/shipping named in notes only |
| N8N-013 | `answerCallbackQuery` before `/actions` | **PASS** | `callback-ack-before-actions` ack_order index assert + callback→actions map |
| N8N-014 | Slow aibridge after ack → prompt ack | **PARTIAL → G-01** | Fixture boolean only; no simulated latency/error path beyond literals |
| N8N-015 | `actions=[]` → no keyboard | **PASS** | `render_outbound_keyboard([])==[]` |
| N8N-016 | Three actions order/tokens | **PASS** | labels+tokens unchanged |
| N8N-017 | `stashed` → continuation; no publish claim | **PASS** | `claim_published_forbidden`; `should_present_continuation` |
| N8N-018 | Non-stashed accidental URL suppressed | **PASS** | URL present in response; continuation present=false |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| TRACEABILITY story key | **PASS** | Matrix + fixture `story_keys` |
| Characterization 009/011 marked | **PASS** | notes + capture flags; no silent invent |
| Promote = copy; originals intact | **PASS** | linked package↔tests hash_eq (incl. channel) |
| Nested tasks EPIC-04 | **PASS** | t01–t04 + gate |
| No live Telegram / Railway invent | **PASS** | Gate + test module ADR-Q5 docstring; ops live evidence remains BLOCKED artifact |
| Mapper vs ops README §3 | **Aligned (soft)** · **Info G-05** | Test helpers mirror cheat-sheet; not shared module |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | Guide N8N-014 **must**: after callback, Telegram ack stays prompt when aibridge is slow/unavailable; later resident-safe error. Suite only asserts fixture flags (`callback_still_acknowledged_promptly`, `later_resident_safe_error_via`) inside `callback-ack-before-actions` — no timed/ordered simulation of post-ack failure. TRACEABILITY marks N8N-014 `covered` while behavioral depth is documentary. | Add fixture-driven step timeline (ack completes before simulated aibridge fail) **or** mark characterization/out-of-DoD for live timing; align TRACEABILITY. |
| **G-02** | **Low** | N8N-001 fixture sets `outbound_telegram.one_reply: true` but `test_message_flow_maps_to_turns` never reads it; only mapping equality + ack_order prefix. | Assert `one_reply` / single `SendOrEditMessage` in outbound contract for private-text case. |
| **G-03** | **Info** | N8N-012 wording lists channel post, **poll**, **shipping/pre-checkout**; only `telegram.update-channel-post` exists. | Optional sibling fixtures; or WAIVE as representative sample. |
| **G-04** | **Info** | N8N-010 notes claim photo/document/voice; only `message-photo-no-text` fixtured. | Optional document/voice fixtures; or WAIVE representative media sample. |
| **G-05** | **Info** | Mapping helpers live only in `tests/n8n/test_n8n_telegram_mapping.py` (mirror of `docs/ops/n8n-channel-workflow/README.md` §3). No exported workflow JSON (correct — do not invent); drift risk if README changes without test update. | Keep dual-doc discipline / optional shared mapping table SSOT; no live workflow invent. |

### Non-gaps

| Topic | Note |
|-------|------|
| Inventing Railway SUCCESS / live Telegram PASS | Avoided (gate + ADR-Q5; live evidence BLOCKED file untouched as PASS invent) |
| Moving package originals | Not done; promote=copy verified |
| Caption/edit invent | Avoided — characterization |
| Product logic moved into n8n | Not done — fixture/test-local thin mapper only |
| SPA / hasUxPipeline | false — code/fixture audit only |

### Regressions

| Check | Result |
|-------|--------|
| Pytest `tests/n8n/` | **19 passed** |
| Fixture originals deleted/moved | **None** |
| Live Bot API / Railway claims in tests | **None** |

---

## Cited paths

- `tests/n8n/test_n8n_telegram_mapping.py`
- `tests/fixtures/n8n/*`, `tests/fixtures/telegram/*`, `tests/fixtures/channel/turns-from-private-ru.json`, `actions-valid-send.json`
- `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/*`
- `docs/ops/n8n-channel-workflow/README.md` §2–§3
- Gate: `…/task-aibridge-25-t04-story-gate/acceptance-verification-task-aibridge-25-t04-story-gate.md`
- Guide §10.3 N8N-* · TRACEABILITY-MATRIX.md

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Low), G-03/G-04/G-05 (Info)
- **Critical:** 0
- **OPEN counts:** Critical **0** · Medium **1** · Low **1** · Info **3**
- **next:** **P5** disposition
