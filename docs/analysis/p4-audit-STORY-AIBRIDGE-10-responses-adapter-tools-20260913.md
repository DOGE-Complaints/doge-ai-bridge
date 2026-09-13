# P4 Audit — STORY-AIBRIDGE-10-responses-adapter-tools

| Field | Value |
|-------|-------|
| **Date** | 2026-09-13 |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/STORY-AIBRIDGE-10-responses-adapter-tools/STORY-AIBRIDGE-10-responses-adapter-tools.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-10-responses-adapter-tools.md` |
| **Method** | Read/Glob only; no product patches; no live pytest this pass |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story AC #1–#4** | **PASS** on library client / tool_gen / prompt xor (+ recorded transport) |
| **Bullrun t01–t05 Done** | **Confirmed** vs modules + gate PASS 2026-09-13T15:46:08Z |
| **§5.1 non-blocking ASGI** | **Partial** — see **G-01** |
| **OPEN gaps** | **1 Medium · 2 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **Unknown**; historical **112 passed / 14 skipped** @ P3 gate |

---

## Bullrun touchpoints (отчёт only)

| ID | Claim | P4 fact |
|----|-------|---------|
| Story 10 | 🟢 Done · awaiting P4 | **Library Done**; ASGI non-block residual |
| t01–t04 | Done | **Confirmed** (`ProductionResponsesClient`, parse, flat tools, xor) |
| t05 gate | Done | PASS — `acreate` evidence overstated (callable-only) |

---

## AC matrix (`$storyFile`)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | Every REQ-03 §5.1 bullet on production client path (fake/recorded OK) | **PASS** (knobs/parse/map/redact) · **residual G-01** | `ProductionResponsesClient`: `store=false`, `parallel_tool_calls=false`, finite `max_output_tokens`, timeouts, parse/replay, 429/timeout map, `redact_secrets`. **ASGI non-block:** `acreate` exists; `InterviewEngine.run_turn` still sync `create` only |
| 2 | Emitted tool schema Responses-flat | **PASS** | `generate_strict_tool` top-level `type`/`name`/`parameters`/`strict`; no nested `"function"`; `test_flat_tool_schema_from_generator`; `to_responses_flat_tool` normalizer |
| 3 | Prompt never duplicates instructions (prefix xor `instructions=`) | **PASS** | `assert_prompt_xor` / `DualInstructionsError`; `InterviewEngine.prompt_channel`; `test_prompt_xor_*` |
| 4 | API key never in logs/exceptions | **PASS** | `redact_secrets` + `_safe_message`; `test_client_maps_429_and_redacts_key` |

### Scope / §5.1 extras

| Item | Status | Evidence |
|------|--------|----------|
| Preserve all output items | **PASS** | `parse_responses_payload` + history append all `output_items`; reasoning kept |
| `function_call` / `call_id` / usage / cache | **PASS** | `FunctionCallItem`; `cached_input_tokens_from_usage` |
| 429 / 5xx / timeouts → bounded outcomes | **PASS** (code) · **Info test hole** | `map_http_to_outcome`; 429+timeout tested; **no** dedicated 5xx test — **G-02** |
| Wire `/turns` → engine | **Out of scope** | Story 11 |
| Live OpenAI smoke | **Deferred** | Policy: fake/recorded OK |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | §5.1: «not block the ASGI event loop». Fact: `ProductionResponsesClient.acreate` present, but gate smoke only asserts `callable(acreate)` (`test_acreate_async_does_not_require_sync_transport`). `InterviewEngine.run_turn` always uses sync `client.create` (blocking `HttpxResponsesTransport` / sync path). When story 11 wires `/turns`, sync engine would block the loop unless fixed here or there. | Prefer: engine async path or documented `to_thread`/`acreate` contract + real async unit test (mock AsyncClient). Do not invent `/turns` wire (11). |
| **G-02** | **Info** | §5.1 maps 5xx → `TRANSIENT_FAILURE`; no test asserts HTTP 5xx outcome (only 429 + timeout). | Add recorded-transport test for status 503 → `transient_failure`. |
| **G-03** | **Info** | `$storyFile` §Verified current state still P1 text (`RecordingResponsesClient` only; nested `"function"`; dual instructions risk) while post-P3 code contradicts. | Sync backlog verified-state to post-P3 facts (docs-only). |

### Non-gaps

| Topic | Note |
|-------|------|
| `/turns` → InterviewEngine | Explicit out of scope → STORY-11 |
| Inventing numeric budget defaults | Out of scope |
| Nested Chat Completions wrap | Removed from `generate_strict_tool`; normalizer remains for migration |

---

## Cited paths

- `src/aibridge/responses_client.py`, `tool_gen.py`, `interview.py`, `request_assembly.py`
- `tests/test_story_10_responses_adapter.py`, `tests/test_tool_gen.py`
- Gate: `acceptance-verification-task-aibridge-02-10-t05-…md`
- REQ-03 §5.1

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Info), G-03 (Info)
- **Critical:** 0
- **OPEN counts:** Medium **1** · Info **2** · Low **0** · Critical **0**
- **next:** **P5** disposition
