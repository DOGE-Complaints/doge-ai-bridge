# P4 Audit — STORY-AIBRIDGE-16-privacy-retention

| Field | Value |
|-------|-------|
| **Date** | 2026-09-13 |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/STORY-AIBRIDGE-16-privacy-retention/STORY-AIBRIDGE-16-privacy-retention.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-16-privacy-retention.md` |
| **Method** | Read/Glob only; no product patches; no live pytest this pass |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (§6.2 / consumed invariant / ops-only delete)** | **PARTIAL** — library + unit tests PASS · **ASGI/PG wiring residuals** |
| **Bullrun t01–t06 Done** | **Confirmed** vs modules + gate PASS 2026-09-13T17:49:14Z |
| **OPEN gaps** | **2 Medium · 1 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **Unknown**; historical **177 passed / 38 skipped** @ P3 gate (story-16: 11) |

---

## Bullrun touchpoints (отчёт only)

| ID | Claim | P4 fact |
|----|-------|---------|
| Story 16 | 🟢 Done · awaiting P4 | Privacy library Done; idle-expiry + ops-CLI PG residuals |
| t01–t05 | Done | **Confirmed** (`privacy_retention.py`, `ops_session_delete.py`, tests, privacy-pilot) |
| t06 gate | Done | PASS |

---

## AC matrix (`$storyFile` Target · REQ-03 §6.2)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| §6.2 TTL default 604800 | **PASS** | `DEFAULT_SESSION_TTL_SECONDS` / Settings / `.env.example` |
| §6.2 TTL slides on legitimate activity | **PARTIAL** | `SessionActivityClock.touch` on `get_or_create_session`; **in-memory only**; PG hydrate re-touches without durable expiry — **G-01** |
| §6.2 expired narrative minimized | **PARTIAL** | `minimize_narrative` + tests; **`expire_idle_session_narrative` never called from ASGI** — idle path only drops confirm binding — **G-01** |
| §6.2 expired pending tokens purged | **PARTIAL** | `purge_expired_pending_tokens` unit-tested; not scheduled/wired on turns — **G-01** |
| §6.2 ops session-delete authz + tested | **PASS (library)** · **PARTIAL (CLI)** | Bearer fail-closed + audit; CLI uses empty `HistoryStore()` — no live PG wire — **G-02** |
| §6.2 delete covers history / pending / tokens | **PASS** (in-memory ops_delete tests) | `test_ops_delete_covers_history_tokens_confirm` |
| Target 2 consumed unusable | **PASS** | purge keeps CONSUMED; ops delete + `verify_for_consume` → Conflict |
| Target 3 ops-only / no OAS invent | **PASS** | No channel delete path; `test_channel_openapi_has_no_session_delete_path` |
| §6.2 n8n retention separate | **Info** | privacy-pilot §3 checklist unchecked — **G-03** |
| Early delete after stash/cancel | **Info** | Runbook checkbox `[ ]` — not story Target force — **G-03** |

### Scope extras

| Item | Status | Evidence |
|------|--------|----------|
| Tombstone non-PII | **PASS** | `TOMBSTONE_ITEM` · minimize tests |
| HTTP path Unknown | **PASS** | Explicitly not invented |
| PostgresHistoryStore.replace | **PASS** (API) | Exists; unused by ASGI idle path |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | R3-P1-10: expired narrative minimized + tokens purged on TTL. Fact: `expire_idle_session_narrative` exists and is unit-tested but **Grep shows no call from `app`/`channel`/`confirm`**. On idle, `get_or_create_session` only pops in-memory confirm maps — **does not** `minimize_narrative` / purge tokens / clear PG history. `SessionActivityClock` is process-local; after restart `last is None` → `is_expired` False; PG hydrate path always `touch`es without checking durable `updated_at`. Resident narrative can remain in `conversation_history` past pilot TTL. | On expiry (and/or periodic sweep): call `expire_idle_session_narrative` with app `history_store` + tokens; persist TTL SSOT (PG column or clock table); refuse hydrate of expired sessions; disposable-PG tests. |
| **G-02** | **Medium** | Ops session-delete CLI (`ops_session_delete.main`) always constructs empty `HistoryStore()` and never attaches `ConfirmationGuard` / `PostgresHistoryStore` / `DATABASE_URL`. Authz fail-closed works; **production delete against live PG is not executable** via the shipped CLI (runbook even notes «wire DATABASE_URL»). Library API works in unit tests with injected stores. | Wire CLI to settings `DATABASE_URL` + PG history/tokens/confirm (or documented ops script); fail-closed integration test on disposable PG. |
| **G-03** | **Info** | privacy-pilot §2–§3 checkboxes (n8n retention, early delete after stash, backup vs delete) remain unchecked; §6.2 says n8n retention verified separately before residents — docs-only residual. | Ops evidence / separate checklist close before residents; or WAIVE as out-of-code DoD. |

### Non-gaps

| Topic | Note |
|-------|------|
| Inventing channel OpenAPI delete | Correctly avoided |
| Consumed-token invariant in library | Covered by tests |
| Pilot default 604800 | Wired in Settings |

---

## Cited paths

- `src/aibridge/privacy_retention.py`, `ops_session_delete.py`, `confirm.py`, `app.py`, `config.py`
- `src/aibridge/pg_runtime.py` (`PostgresHistoryStore.replace`)
- `docs/runbooks/privacy-pilot.md`
- `tests/test_story_16_privacy_retention.py`
- Gate: `acceptance-verification-task-aibridge-02-16-t06-…md`
- REQ-03 §6.2 R3-P1-10

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Medium), G-03 (Info)
- **Critical:** 0
- **OPEN counts:** Medium **2** · Info **1** · Low **0** · Critical **0**
- **next:** **P5** disposition
