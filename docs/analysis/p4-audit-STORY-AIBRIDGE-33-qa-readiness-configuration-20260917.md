# P4 Audit — STORY-AIBRIDGE-33-qa-readiness-configuration

| Field | Value |
|-------|-------|
| **Date** | 2026-09-17T21:00:46Z |
| **Mode** | `input_mode=backlog_story` |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** | `…/EPIC-AIBRIDGE-04-…/STORY-AIBRIDGE-33-qa-readiness-configuration/STORY-AIBRIDGE-33-qa-readiness-configuration.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-33-qa-readiness-configuration.md` |
| **Method** | Read/Glob + live pytest `tests/contract/test_readyz_configuration.py`; fixture hash package↔`tests/fixtures/settings`; product `readiness.py` / Settings; no product patches; `hasUxPipeline=false` |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · aibridge-operator-contract §6 |
| **Railway / live Telegram** | **No** Railway SUCCESS · **No** live Telegram PASS invented |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (READY-001…015 · guide §10.11)** | **PASS (core)** — 15 fixtures + suite; **2 Medium** residuals (READY-001 memory vs migrated PG; READY-013 Preference A) |
| **Bullrun t01–t04 Done** | **Confirmed** vs promote copies + gate PASS 2026-09-17T20:57:41Z |
| **OPEN gaps** | **0 Critical · 2 Medium · 1 Low · 2 Info** |
| **Critical OPEN** | **0** |
| **Live pytest** | **17 passed** (`tests/contract/test_readyz_configuration.py`) @ 2026-09-17T21:00:46Z |

---

## Bullrun touchpoints (отчёт — актуализация фактов)

| ID | Bullrun claim | P4 fact |
|----|---------------|---------|
| **STORY-33** | 🟡 Implemented (P3 closed · next P4) · pkg-000030 | **Confirmed** READY suite; gate PASS; **this P4** → next **P5** |
| **t01** | Done — promote seed READY-002 | **Confirmed** `ready-missing-channel-bearer` hash_eq |
| **t02** | Done — generate READY-001…015 | **Confirmed** 15 settings fixtures · matrix_ids complete |
| **t03** | Done — contract /readyz | **Confirmed** 17 passed · residual G-01…G-03 |
| **t04** | Done — story gate PASS | **Confirmed** acceptance 2026-09-17T20:57:41Z · WAIVE notes for READY-001/013 · no Railway/live TG invent |
| **pkg-000030** | Active · 4 paths | YAML present under `aibridge-active-packages/` |
| **TRACEABILITY** | READY-001…015 → story `covered` | **Confirmed** rows; stand-ins → **G-01/G-02** |
| **$storyFile AC** | `[x]` incl. «task-* folders not created until P1» | **Soft contradiction** (folders exist) → **Info G-05** |

---

## AC matrix (`$storyFile` / pipeline · guide §10.11 READY-*)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| READY-001 | Complete valid config + **migrated PostgreSQL** → 200 `ready` | **PARTIAL → G-01** | `test_ready_001` · `ready-ok.json` · `DATABASE_URL=memory` + `AIBRIDGE_ALLOW_MEMORY_STORES` · gate WAIVE live migrated PG |
| READY-002 | Channel Bearer missing → `channel_auth_missing` | **PASS** | parametrize · `ready-missing-channel-bearer` |
| READY-003 | Gateway Bearer missing → `gateway_bearer_missing` | **PASS** | `ready-missing-gateway-bearer` |
| READY-004 | Bearers equal → `channel_gateway_bearer_equal` | **PASS** | `ready-bearers-equal` |
| READY-005 | Gateway URL missing/conflicting/non-HTTPS → bounded reason | **PARTIAL → G-03** | Only `intake_base_url_not_https` (`ready-intake-not-https`); product also emits `intake_base_url_missing` (`readiness.py:117-118`) — **no** story fixture; «conflicting» has no distinct reason code |
| READY-006 | SPA redirect invalid → `draft_redirect_base_invalid` | **PASS** | `ready-redirect-invalid` |
| READY-007 | OpenAI key/model missing → `openai_config_missing` | **PASS** | `ready-openai-missing` |
| READY-008 | OpenAI store true → fails closed | **PASS** | `ValidationError` · `ready-openai-store-true` |
| READY-009 | Live without schema flag → `dry_run_required` | **PASS** | `ready-dry-run-required` |
| READY-010 | Content manifest/hash/path invalid → bundle reason | **PASS (soft)** · **Info G-04** | `reason_contains_any: ["content_"]` · not exact reason |
| READY-011 | Tool gen fails → `tool_gen_failed:*` | **PASS** | `reason_prefix` · `ready-tool-gen-failed` |
| READY-012 | PostgreSQL unreachable → `database_unreachable` | **PASS** | unreachable PG URL + memory inject · `/readyz` hits `_postgres_migration_ok` |
| READY-013 | Migration missing/mismatch → migration reason | **PARTIAL → G-02** | Preference A: `evaluate_readiness` + fake `connect_postgres` → `migration_version_mismatch` only; **not** HTTP `/readyz`; **no** `migrations_missing` / `migration_version_missing` |
| READY-014 | Non-Postgres + memory forbidden → `database_not_postgres` | **PASS** | `ready-database-not-postgres` |
| READY-015 | `/readyz` → no OpenAI gen / no gateway write | **PASS** | Recording engine + `RecordingGatewayTransport` · calls == 0 |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| TRACEABILITY story key | **PASS** | Matrix READY-001…015 `covered` |
| Promote = copy | **PASS** | 15/15 hash_eq package ↔ `tests/fixtures/settings/` |
| Characterization | **N/A** | no READY char IDs in matrix |
| SPA / hasUxPipeline | false | |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Medium** | Guide READY-001 **must**: valid config + **migrated PostgreSQL** → 200. Suite uses memory stores (`ready-ok.json`, `_memory_app`). Gate explicitly WAIVEs live migrated PG. TRACEABILITY still `covered`. | Disposable-PG migrate + `/readyz` 200; or formal P5 WAIVE + align TRACEABILITY/fixture notes to «memory stand-in». |
| **G-02** | **Medium** | READY-013 Preference A: monkeypatch `connect_postgres` + `evaluate_readiness` only (`test_ready_013_migration_mismatch_fake_pg`). No ASGI `/readyz` path; no asserts for `migrations_missing` / `migration_version_missing` (`readiness.py:31-43`). | Fake-PG or disposable-PG `/readyz` for mismatch **and** missing-version cases; or P5 WAIVE Preference A + document characterization. |
| **G-03** | **Low** | READY-005 matrix row lists missing/conflicting/non-HTTPS; story fixtures cover **only** non-HTTPS. `intake_base_url_missing` exists in product and legacy `tests/test_story_12_readyz_env.py`, not in READY story envelope set. No distinct «conflicting» reason in `readiness.py`. | Add missing-URL fixture under story suite; clarify/drop «conflicting» in TRACEABILITY; or mark narrow characterization. |
| **G-04** | **Info** | READY-010 asserts `any(n in reason for n in ["content_"])` — soft prefix, not exact bounded code. | Pin exact `content_bundle_not_ready` / deployment.error; or WAIVE soft prefix. |
| **G-05** | **Info** | Backlog AC still `[x]` «task-* folders not created until P1» while nested task folders exist and are Done. | Docs-only AC checkbox sync. |

### Non-gaps

| Topic | Note |
|-------|------|
| Inventing Railway SUCCESS / live Telegram | Avoided |
| Fixture originals moved | Not done; promote=copy verified (15) |
| Silent product invent | Avoided |
| READY-002…004/006…009/011/012/014/015 core | Present |
| SPA / hasUxPipeline | false |

### Regressions

| Topic | Note |
|-------|------|
| vs gate t04 (17 passed) | **None** — re-run 17 passed @ 2026-09-17T21:00:46Z |

---

## Cited paths

- `tests/contract/test_readyz_configuration.py`
- `tests/fixtures/settings/ready-*.json` (15)
- `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/ready-*.json`
- `src/aibridge/readiness.py` · `src/aibridge/config.py` · `src/aibridge/app.py`
- Gate: `…/task-aibridge-33-t04-story-gate/acceptance-verification-….md`
- Guide §10.11: `docs/tasks/qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`
- TRACEABILITY: `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md`

---

## Handoff

- **OPEN gaps:** 0 Critical · **2 Medium** · **1 Low** · **2 Info**
- **OPEN IDs:** G-01, G-02, G-03, G-04, G-05
- **Product Story AC/DoD (core):** **PASS** (explicit; ≠ empty gap-list)
- **next:** **P5** (disposition; do not implement in P4)
