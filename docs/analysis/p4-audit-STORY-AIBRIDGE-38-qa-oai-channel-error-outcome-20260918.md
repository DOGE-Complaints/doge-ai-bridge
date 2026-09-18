# P4 Audit — STORY-AIBRIDGE-38-qa-oai-channel-error-outcome

| Field | Value |
|-------|-------|
| **Date** | 2026-09-18T13:48:51Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-04-…/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md` |
| **Method** | Read/Glob + live pytest `tests/integration/test_openai_prompt_behavior.py` (19); product `app.py` handler; decision + expect fixtures hash_eq; TRACEABILITY/QUAL/guide §10.5; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway / live Telegram** | **No** Railway SUCCESS · **No** live Telegram PASS invented |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (CHAR-006 Option A · OAI-008/009)** | **PASS (core)** — decision + handler + channel expects; **1 Medium** residual (parent guide §10.5 stale) |
| **Bullrun t01–t04 Done** | **Confirmed** vs promote copy + gate PASS 2026-09-18T13:43:00Z |
| **OPEN gaps** | **0 Critical · 1 Medium · 3 Low · 2 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **19 passed** (`tests/integration/test_openai_prompt_behavior.py`) @ 2026-09-18T13:48:51Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-38** | 🟢 P3 Done · next P4 · pkg-000037 | **Confirmed** Option A + suite 19; gate PASS; **this P4** → next **P5** |
| **t01** | Done — Option A decision fixture | **Confirmed** `char-006-decision.json` decision=A · hash_eq |
| **t02** | Done — handler + channel asserts | **Confirmed** `responses_transport_channel_error` · OAI-008/009 channel 429/503 |
| **t03** | Done — expects · promote=copy | **Confirmed** 429/503 expect fixtures hash_eq |
| **t04** | Done — TRACEABILITY + P1-Q2 | **Confirmed** covered · QUAL P1-Q2 **closed** |
| **pkg-000037** | Active · 4 paths | YAML under `aibridge-active-packages/` |
| **Note** | OAI suite 19 passed | **Confirmed** this P4 re-run |
| **Guide §10.5** | (not claimed) | Still «Bounded internal channel error» → **Medium G-01** |

---

## AC matrix (`$storyFile` / pipeline · gaps §38 · guide §10.5/§16)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| CHAR-006 | Decision recorded; not forever-500 | **PASS** | `char-006-decision` Option A · program `decision_recorded` · `test_char_006_decision_fixture_option_a` |
| OAI-008 channel | 429 `rate_limited` retryable | **PASS** | Handler + `char-006-channel-429-expect` · `test_oai_008_*` · gw.calls=[] · secrets forbid |
| OAI-009 channel | 503 `transient_failure` retryable | **PASS** | Handler + `char-006-channel-503-expect` · `test_oai_009_*` |
| Transport keep | RATE_LIMITED / TRANSIENT | **PASS** | ProductionResponsesClient + RecordingResponsesTransport raises |
| Secrets absent | bodies/logs | **PASS (body)** | `_assert_forbid` on transport err + channel JSON |
| P1-Q2 closed | QUAL | **PASS** | `TEST-QUALIFICATION` P1-Q2 **closed** |
| TRACEABILITY covered | CHAR-006 · OAI-008/009 | **PASS** | Package + ops row content Option A |
| Parent guide §10.5 | Align with Option A | **FAIL → G-01** | Guide still «Bounded internal channel error» for OAI-008/009 |
| Promote = copy | decision + expects | **PASS** | hash_eq all three openai fixtures |
| Fixture-index | story 38 + CHAR refs | **PASS** | count 229 · has38 · CHAR-006 refs/bound_tests |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| No gateway on OAI errors | **PASS** | `gw.calls == []` · dedupe abort |
| TIMEOUT (OAI-010) | **PASS (explicit)** | Decision TIMEOUT→500 `internal_error`; handler comment; out of 429/5xx fork |
| Middleware RL distinct | **CLAIM** · **Low G-02** | Same status/code; messages differ; **no** suite assert of distinction |
| SPA / hasUxPipeline | false | |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | Parent guide §10.5 OAI-008/009 still describes «Bounded internal channel error under current implementation» while product+TRACEABILITY are Option A **429/503**. SSOT drift vs package. | Relabel guide Expected to Option A channel codes; or note «superseded by STORY-38 / CHAR-006 decision». |
| **G-02** | **Low** | TRACEABILITY claims OpenAI RL «Distinct from client middleware RL», but suite does not assert message/cause (`OpenAI rate limited` vs `Rate limit exceeded`) — only shared `429`/`rate_limited`. | Assert distinct message (or other discriminator); or soften TRACEABILITY wording. |
| **G-03** | **Low** | Channel ASGI path for OAI-008/009 injects via `_RaiseClient(ResponsesTransportError)` — not `ProductionResponsesClient` + scripted HTTP through `create_app`. Transport and handler tested separately; full wire path unproven. | Add ASGI test with Production client wired; or WAIVE as intentional split. |
| **G-04** | **Low** | Ops TRACEABILITY header still `synced … 12:42:35Z` while OAI/CHAR rows updated; stamp stale. | Bump ops sync header timestamp. |
| **G-05** | **Info** | Channel OAS (`docs/openapi/aibridge-channel-v1.openapi.yaml`) has free-string `ChannelErrorBody`; no example/doc of new `transient_failure` / OpenAI-cause `rate_limited`. Story non-goal: invent OAS fields. | Optional OAS examples; or WAIVE per non-goal. |
| **G-06** | **Info** | Gaps §38 Option A prose lists `timeout` among map targets; decision fixture keeps TIMEOUT→500 (OAI-010). Product matches decision. Soft arch wording tension only. | Align §38 table note with decision TIMEOUT carve-out. |

### Non-gaps

| Topic | Note |
|-------|------|
| Forever-500 characterization lock | Removed for RATE_LIMITED / TRANSIENT_FAILURE |
| Invent gateway publish on OAI errors | Avoided |
| Gate-5 / CHAR-008 / Railway / live TG | Out of scope / not invented |
| Fixture originals moved | Not done; promote=copy verified |
| QUAL P1-Q2 | Marked **closed** |
| SPA / hasUxPipeline | false |

### Regressions

| Topic | Note |
|-------|------|
| vs gate t04 (OAI suite 19 passed) | **None** — re-run **19 passed** @ 2026-09-18T13:48:51Z |

---

## Cited paths

- `src/aibridge/app.py` (`responses_transport_channel_error` · middleware RL)
- `src/aibridge/responses_client.py` (`map_http_to_outcome`)
- `tests/integration/test_openai_prompt_behavior.py`
- `tests/fixtures/openai/char-006-decision.json` (+ 429/503 expects) · package promote copies
- `tests/fixtures/meta/fixture-index.json` (CHAR-006 program)
- TRACEABILITY package + ops
- Guide §10.5: `docs/tasks/qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`
- QUAL: `…/TEST-QUALIFICATION-20260918.md`
- Gaps §38: `…/TECHNICAL-ARCHITECTURE-GAPS-36-40.md`
- Gate: `…/task-aibridge-38-t04-story-gate/acceptance-verification-….md`

---

## Handoff

- **OPEN gaps:** 0 Critical · **1 Medium** · **3 Low** · **2 Info**
- **OPEN IDs:** G-01, G-02, G-03, G-04, G-05, G-06
- **Product Story AC/DoD (core):** **PASS** (Option A implemented + tested; ≠ empty gap-list)
- **next:** **P5** (disposition; do not implement in P4)
