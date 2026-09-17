# P4 Audit — STORY-AIBRIDGE-23-qa-auth-ops-boundaries

| Field | Value |
|-------|-------|
| **Date** | 2026-09-17T14:10:42Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-04-…/STORY-AIBRIDGE-23-qa-auth-ops-boundaries/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md` |
| **Method** | Read/Glob + live pytest contract AUTH; fixture hash originals↔copies; product `auth.py`/`app.py`/`readiness.py`; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway** | **No** live Railway SUCCESS invented or claimed |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (AUTH-001…012 · guide §10.1)** | **PASS (core)** — fixtures + contract tests + TRACEABILITY; 1 Medium residual on AUTH-009 logs |
| **Bullrun t01–t04 Done** | **Confirmed** vs promote copies + gate PASS 2026-09-17T14:02:23Z |
| **OPEN gaps** | **0 Critical · 1 Medium · 1 Low · 3 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **15 passed** (`tests/contract/test_auth_ops_boundaries.py` · `--noconftest`) @ 2026-09-17T14:08–14:10Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-23** | 🟢 Implemented (P3 · next P4) · pkg-000020 | **Confirmed** AUTH contract; gate PASS; **this P4** → next **P5** |
| **t01** | Done — promote seed | **Confirmed** `tests/fixtures/channel/turns-valid-private.json` **hash_eq** package `fixtures/turns-valid-private.json`; original intact |
| **t02** | Done — generate AUTH matrix fixtures | **Confirmed** 13 auth envelopes in package `fixtures/` + copies under `tests/fixtures/{channel,settings,spies}/` (all hash_eq) |
| **t03** | Done — contract AUTH tests | **Confirmed** `tests/contract/test_auth_ops_boundaries.py` · 15 passed; AUTH-001…012 parametrized + 008 equals + 009 leak + seed intact |
| **t04** | Done — story gate PASS | **Confirmed** `acceptance-verification-task-aibridge-23-t04-story-gate.md` · no Railway SUCCESS |
| **pkg-000020** | Active (story 23 P3 · next P4) | `--verify` **ok 4 paths** |
| **TRACEABILITY** | AUTH-001…012 → story key `covered` | **Confirmed** `TRACEABILITY-MATRIX.md` lines for AUTH-001…012 |

---

## AC matrix (`$storyFile` · guide §10.1 AUTH-*)

| ID | Expected (story) | Status | Evidence |
|----|------------------|--------|----------|
| AUTH-001 | Valid Channel Bearer → reaches validation/processing | **PASS** | Fixture `channel/auth-valid-current` → POST `/v1/channel/turns` **200**; live probe: dry_run turn body with `state`/`actions` (processing beyond auth) |
| AUTH-002 | Previous Bearer accepted | **PASS** | `auth-previous-bearer` + `Settings.accepted_channel_tokens()` includes previous |
| AUTH-003 | Missing Authorization → 401 `unauthorized`, redacted | **PASS** | 401 + `error.code==unauthorized`; `CHANNEL not in response.text` |
| AUTH-004 | Wrong scheme (`Basic`) → 401 | **PASS** | `auth-basic-scheme` |
| AUTH-005 | `Bearer` without value → 401 | **PASS** | `auth-bearer-empty`; `extract_bearer` rejects empty token |
| AUTH-006 | Wrong same-length token → 401 | **PASS** | `auth-wrong-same-length` (len 46==46) |
| AUTH-007 | Wrong diff-length → 401 without timing-dependent **functional** difference | **PASS (functional)** · **Info residual G-03** | Same 401/`unauthorized` path; product `constant_time_token_match` in `src/aibridge/auth.py`; **no** wall-clock timing assert in tests |
| AUTH-008 | Gateway Bearer on channel → 401; equal bearers → readyz reject | **PASS** | `auth-gateway-as-channel` 401; `settings/auth-channel-equals-gateway` → `/readyz` 503 `channel_gateway_bearer_equal` (`readiness.py`) |
| AUTH-009 | Channel Bearer absent from logs/metrics/error | **PARTIAL → G-01** | Error body + `/metrics` forbid token; fixture field `forbid_substrings_in_logs` **never read** by test |
| AUTH-010 | `/healthz` no Bearer → 200 `{"status":"ok"}` | **PASS** | `auth-healthz-no-bearer`; middleware only on `CHANNEL_PATH_PREFIX` |
| AUTH-011 | `/readyz` no Bearer → 200\|503; no generation/write | **PASS (gen)** · **Info G-04** | status in {200,503}; `no_generation` via `engine.client.calls==[]`; gateway write not separately spied |
| AUTH-012 | `/metrics` private test → Prometheus; no PII/secrets | **PASS (text/secrets)** · **Info G-02** | 200 `text/plain`; forbid channel/gateway tokens; **no** in-app private-network ACL |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| TRACEABILITY story key on every AUTH-* | **PASS** | Matrix + fixture `story_keys` |
| Nested tasks materialized EPIC-04 | **PASS** | t01–t04 folders + gate |
| Promote = **copy**; originals intact | **PASS** | 14/14 hash_eq package↔tests |
| Channel ≠ Gateway default Settings | **PASS** | `_base_settings` assert `not channel_gateway_bearers_equal()` |
| Live Railway SUCCESS | **Not claimed** | Gate AC + this audit |
| `/metrics` without Channel Bearer middleware | **PASS (fact)** | `channel_bearer_middleware` gated on `/v1/channel/` only (`app.py`) |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | AUTH-009: `tests/fixtures/spies/auth-forbid-bearer-leak.json` declares `forbid_substrings_in_logs`, but `test_auth_009_channel_bearer_absent_from_error_and_metrics` only asserts error body + `/metrics`. Guide §10.1 / t03 purpose require logs. TRACEABILITY marks AUTH-009 `covered` while logs branch is unexercised. | Capture structured/app logs during 401 (or fail-closed spy bag); assert fixture `forbid_substrings_in_logs` needles absent; keep error+metrics asserts. |
| **G-02** | **Info** | Guide §2.1 + story Context: `/metrics` **must stay private-network-only**. Product only documents assumption (`app.py` metrics docstring; `metrics.py` «private network assumed») — **no** IP/CIDR middleware. AUTH-012 TestClient proves Prometheus + no secrets, not network ACL. | Ops/deploy ACL evidence or characterization WAIVE; optional future network-boundary test outside default CI. |
| **G-03** | **Info** | AUTH-007 expected wording includes timing; suite asserts functional 401 only. Product already uses `hmac.compare_digest` + dummy compare on length mismatch (`auth.py`). | Optional micro-benchmark characterization; or WAIVE as functional-equivalence already met. |
| **G-04** | **Info** | AUTH-011 `no_generation` asserted; «no write» not asserted via `RecordingGatewayTransport.calls`. `evaluate_readiness` path has no gateway POST by construction. | Optional assert gateway `calls==[]` on `/readyz` when recording transport injected; or WAIVE. |
| **G-05** | **Low** | `channel_rate_limit_middleware` (`app.py`) sets `principal_key = auth[:24]` → in-memory key includes Bearer token prefix (`Bearer channel-token-aaa`) when rate limits enabled. Not rendered in `/metrics`; hygiene adjacent to AUTH-009. | Hash/HMAC principal key (no raw Authorization prefix) before storing in `RateLimiter._principal`. |

### Non-gaps

| Topic | Note |
|-------|------|
| Inventing Railway SUCCESS | Avoided in gate + this P4 |
| Live Telegram / n8n | Out of story scope |
| Moving package fixture originals | Not done; promote=copy verified |
| SPA / hasUxPipeline | false — code audit only |
| Channel Bearer on `/healthz`/`readyz`/`metrics` | Correctly **not** required |

### Regressions

| Check | Result |
|-------|--------|
| Pytest AUTH contract | **15 passed** (no fail) |
| Fixture originals deleted/moved | **None** |
| Channel Bearer accepted as Gateway default | **None** — default pins unequal; equal → readyz 503 |
| Middleware accidentally gating ops endpoints | **None** — prefix `/v1/channel/` only |

---

## Cited paths

- `tests/contract/test_auth_ops_boundaries.py`
- `tests/fixtures/channel/*auth*`, `turns-valid-private.json`
- `tests/fixtures/settings/auth-channel-equals-gateway.json`
- `tests/fixtures/spies/auth-forbid-bearer-leak.json`
- `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/*` (originals)
- `src/aibridge/auth.py`, `app.py`, `config.py`, `readiness.py`, `metrics.py`, `rate_limit.py`
- Gate: `acceptance-verification-task-aibridge-23-t04-story-gate.md`
- Guide §2.1 · §4.1 · §10.1 AUTH-* · TRACEABILITY-MATRIX.md

---

## Handoff

- **OPEN:** G-01 (Medium), G-05 (Low), G-02/G-03/G-04 (Info)
- **Critical:** 0
- **OPEN counts:** Critical **0** · Medium **1** · Low **1** · Info **3**
- **next:** **P5** disposition
