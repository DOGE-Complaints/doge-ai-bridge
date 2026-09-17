# P4 Audit — STORY-AIBRIDGE-32-qa-privacy-logs-observability

| Field | Value |
|-------|-------|
| **Date** | 2026-09-17T20:35:51Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-04-…/STORY-AIBRIDGE-32-qa-privacy-logs-observability/STORY-AIBRIDGE-32-qa-privacy-logs-observability.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-32-qa-privacy-logs-observability.md` |
| **Method** | Read/Glob + live pytest `tests/integration/test_privacy_observability.py`; fixture hash package↔`tests/fixtures/{spies,channel}`; product `audit`/`metrics`/`redact_secrets`/`PostgresActionTokenStore`/`tool_gen`; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway / live Telegram** | **No** Railway SUCCESS · **No** live Telegram PASS invented |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (SEC-001…010 · guide §10.10)** | **PASS (core)** — 11 fixtures + suite; **1 Medium** residual on SEC-006 PostgreSQL hash-only depth |
| **Bullrun t01–t04 Done** | **Confirmed** vs promote copies + gate PASS 2026-09-17T20:33:31Z |
| **OPEN gaps** | **0 Critical · 1 Medium · 1 Low · 3 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **11 passed** (`tests/integration/test_privacy_observability.py`) @ 2026-09-17T20:35:51Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-32** | 🟢 Implemented (P3 · next P4) · pkg-000029 | **Confirmed** SEC suite; gate PASS; **this P4** → next **P5** |
| **t01** | Done — generate SEC-* spy envelopes | **Confirmed** 10 spies + 1 channel package fixtures |
| **t02** | Done — promote=copy | **Confirmed** 11 hash_eq |
| **t03** | Done — integration privacy/obs | **Confirmed** 11 passed · residual G-01/G-02 |
| **t04** | Done — story gate PASS | **Confirmed** acceptance 2026-09-17T20:33:31Z · no Railway/live TG invent |
| **pkg-000029** | Active · 4 paths | YAML present under `aibridge-active-packages/` |
| **TRACEABILITY** | SEC-001…010 → story `covered` | **Confirmed** |
| **$story pipeline Verified/Target** | «fixtures/suite absent» · Target AC `[ ]` | **Drift** → **Info G-05** (tasks Done; gate PASS) |
| **$storyFile AC** | mostly `[x]` · one checkbox still says folders «not created until P1» | **Soft contradiction** (folders exist) → fold **G-05** |

---

## AC matrix (`$storyFile` / pipeline · guide §10.10 SEC-*)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| SEC-001 | Narrative PII absent from audit + metrics | **PASS** | `test_sec_001` · spy forbid email/phone/name · `get_audit_buffer` + `/metrics` |
| SEC-002 | Secret redacted from response/logs | **PASS** | `redact_secrets` + `ProductionResponsesClient` · channel 500 bounded body (`unhandled_channel_exception`) · audit forbid |
| SEC-003 | Channel audit bounded; no Bearer/narrative | **PASS** | `test_sec_003` · forbid list · records have `event`; no CHANNEL/`Bearer ` in detail |
| SEC-004 | `/metrics` counts only; scrub secrets/IDs/text | **PASS** | `test_sec_004` · require metric prefix · forbid list |
| SEC-005 | Error envelope + `request_id` | **PASS** | unauth `/turns` · spy error_keys · no CHANNEL/GATEWAY |
| SEC-006 | PostgreSQL token inspection — hash only | **PARTIAL → G-01** | in-memory `ActionTokenStore` only; fixture notes say PostgreSQL; **no** `PostgresActionTokenStore` |
| SEC-007 | OpenAI capture `store=false`; no secrets | **PASS** | `RecordingResponsesClient.calls[0]` · store false · forbid GATEWAY/CHANNEL |
| SEC-008 | Gateway Bearer only; no Channel | **PASS (soft)** · **Info G-04** | transport Authorization = `Bearer {GATEWAY}`; CHANNEL absent; consume result multi-OR soft |
| SEC-009 | n8n workflow export secret-free | **PASS (narrow)** · **Info G-03** | scans `docs/ops/n8n-channel-workflow/**` markdown/checklist — **not** workflow JSON export |
| SEC-010 | Prompt injection → allowlisted tool only; server-owned origin/path | **PASS (soft)** · **Low G-02** | harness **injects** single tool; asserts only that name in capture; does not prove `tool_gen` refuse evil tools from injection |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| TRACEABILITY story key | **PASS** | Matrix SEC-001…010 `covered` |
| Promote = copy | **PASS** | 11 FIXTURE_NAMES hash_eq |
| Characterization | **N/A** | no SEC char IDs in matrix |
| SPA / hasUxPipeline | false | |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | Guide SEC-006 **must**: PostgreSQL token inspection — only hash stored. `test_sec_006` uses in-memory `ActionTokenStore` (`raw not in _by_hash`). Product `PostgresActionTokenStore` (`pg_runtime.py`) unexercised. Spy notes say PostgreSQL; TRACEABILITY marks `covered` while PG branch is documentary. | Disposable-PG / fake-conn `PostgresActionTokenStore` hash-only INSERT/select + raw forbid; or mark characterization memory-only and align TRACEABILITY. |
| **G-02** | **Low** | SEC-010: InterviewEngine receives a **pre-built** single allowlisted tool; injection text is only message content. Does not exercise `tool_gen` / schema generation refusing arbitrary URL/tool. Channel fixture `forbid_narrative_substrings` unread (SEC-001/003 use spy lists only). | Drive SEC-010 from generated tool surface (+ negative evil tool); assert channel fixture forbid list; or mark soft harness characterization. |
| **G-03** | **Info** | SEC-009 scans ops docs under `docs/ops/n8n-channel-workflow/` — not an n8n workflow export JSON. Forbid list is mostly synthetic story tokens. | Optional export artifact scan; or WAIVE docs-as-proxy for package DoD. |
| **G-04** | **Info** | SEC-008 consume assert is soft multi-OR (`ok` / outcome set / `"outcome" in result` / `state`). | Tighten expected stashed/dry_run outcome; or WAIVE bearer capture as SSOT. |
| **G-05** | **Info** | Pipeline «Verified current state» still says fixtures/suite **absent**; Target AC checkboxes `[ ]`; backlog checkbox still claims folders not created until P1 while Done. | Docs-only sync Meta/Verified/AC. |

### Non-gaps

| Topic | Note |
|-------|------|
| Inventing Railway SUCCESS / live Telegram | Avoided |
| Fixture originals moved | Not done; promote=copy verified (11) |
| Silent product invent | Avoided |
| SEC-001…005/007 core asserts | Present |
| SPA / hasUxPipeline | false |

### Regressions

| Topic | Note |
|-------|------|
| vs gate t04 (11 passed) | **None** — re-run 11 passed @ 2026-09-17T20:35:51Z |

---

## Cited paths

- `tests/integration/test_privacy_observability.py`
- `tests/fixtures/spies/sec-*.json` · `tests/fixtures/channel/sec-turns-pii-narrative.json`
- `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/sec-*.json`
- `src/aibridge/audit.py` · `src/aibridge/metrics.py` · `src/aibridge/responses_client.py` · `src/aibridge/pg_runtime.py` · `src/aibridge/tool_gen.py` · `src/aibridge/app.py`
- Gate: `…/task-aibridge-32-t04-story-gate/acceptance-verification-….md`

---

## Handoff

- **OPEN gaps:** 0 Critical · **1 Medium** · **1 Low** · **3 Info**
- **Product Story AC/DoD (core):** **PASS** (explicit; ≠ empty gap-list)
- **next:** **P5** (disposition; do not implement in P4)
