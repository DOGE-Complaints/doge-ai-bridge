# P4 Audit — STORY-AIBRIDGE-05-gateway-outcomes

| Field | Value |
|-------|-------|
| **Date** | 2026-09-12 |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/STORY-AIBRIDGE-05-gateway-outcomes/STORY-AIBRIDGE-05-gateway-outcomes.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-05-gateway-outcomes.md` |
| **Method** | Read/Glob only; no product patches; no live pytest this pass |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story AC #1–#6** | **PASS** on library + **injected** `GatewayExecutor` / `RecordingGatewayTransport` tests |
| **Bullrun t01–t06 Done** | **Confirmed** vs modules + gate PASS 2026-09-12T21:54:48Z |
| **Default ASGI production path** | **Incomplete** — see **G-01** / **G-02** |
| **OPEN gaps** | **2 Medium** |
| **Critical OPEN** | **0** |
| **Live pytest** | **Unknown**; historical 83 passed / 1 skipped @ gate |

---

## Bullrun touchpoints (отчёт only)

| ID | Claim | P4 fact |
|----|-------|---------|
| Story 05 | 🟢 Done | **AC library Done**; ASGI wiring residual |
| t01–t05 | Done | **Confirmed** via `gateway.py` + `tests/test_gateway_outcomes.py` |
| t06 gate | Done | PASS artifact |

---

## AC matrix (`$storyFile`)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | Channel Bearer never used as gateway Bearer | **PASS** (library) | `GatewayExecutor.authorization_header` uses `gateway_bearer` only; equal-token refuse; `test_executor_uses_gateway_bearer_never_channel` |
| 2 | Dry-run validates without `POST /story-drafts` | **PASS** (library) | `dry_run` → `DRY_RUN_OK`, `http_posted=False`, zero transport calls; `test_dry_run_validates_without_post` |
| 3 | Malformed 201 → not `stashed` | **PASS** | `map_http_outcome` / `CONTRACT_MISMATCH`; `test_malformed_201_not_stashed` |
| 4 | `unknown_outcome` blocks auto Send same revision | **PASS** | `unknown_outcome_revision` + `send_blocked_for_revision`; timeout tests |
| 5 | Stash copy never claims Story published | **PASS** | `STASH_REPLY` «not a published Story» |
| 6 | Continuation URL only when `stashed` | **PASS** | `build_continuation_url` only on STASHED; `test_non_stashed_has_no_continuation` |

### Scope extras

| Item | Status | Evidence |
|------|--------|----------|
| Outcome map incl. unknown / contract_mismatch / blocked | **PASS** | `GatewayOutcome` + `map_http_outcome` |
| Runbook link | **PASS** | `UNKNOWN_OUTCOME_RUNBOOK` → `docs/runbooks/unknown-outcome-reconciliation.md` (exists) |
| Channel envelope fields | **PASS** | `channel.py` passes outcome / draft_id / continuation_url |
| ASGI wires executor from settings | **FAIL** | See **G-01** |
| Live HTTPS + TLS verify transport | **FAIL** | See **G-02** |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | `create_app` (`app.py`) sets `confirmation_guard` via `reset_confirmation_guard()` with **`executor=None`**. No call to `default_executor_from_settings`. Default ASGI Send path uses story-04 legacy branch (`call_gateway` counter-only; no outcome/`POST`). AC behaviors require an injected executor (as in unit tests). | Wire `GatewayExecutor` from settings into `ConfirmationGuard` at app factory; fail-closed when origin/bearer missing if not dry-run; integration test via `TestClient` without manual inject. |
| **G-02** | **Medium** | Scope: constrained HTTPS + **TLS verify**. Fact: only `RecordingGatewayTransport` + `GatewayTransport` Protocol; Grep `src/aibridge`: **no** httpx/requests/urllib HTTP client with `verify=True`. Production cannot perform real stash yet. | Add live transport (HTTPS, TLS verify, `allow_redirects=False`, timeout); keep Recording for tests; optional `@pytest.mark.integration`. |

### Non-gaps

| Topic | Note |
|-------|------|
| Gateway lookup API | Explicitly out of scope |
| Idempotency extension | Out of scope |
| Recording fixtures for unit AC | Intentional; does not replace G-01/G-02 |

---

## Cited paths

- `src/aibridge/gateway.py`, `confirm.py`, `channel.py`, `app.py`, `config.py`, `confirm_fsm.py`
- `tests/test_gateway_outcomes.py`
- `docs/runbooks/unknown-outcome-reconciliation.md`

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Medium)
- **Critical:** 0
- **next:** **P5** disposition
