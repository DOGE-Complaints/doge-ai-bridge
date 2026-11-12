# P4 Audit — STORY-AIBRIDGE-02-content-bundle-registry

| Field | Value |
|-------|-------|
| **Date** | 2026-09-12 |
| **Mode** | `input_mode=backlog_story` (aibridge-operator-contract §6) |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/bullrun-launch-index.md` |
| **$story** (pipeline) | `…/STORY-AIBRIDGE-02-content-bundle-registry/STORY-AIBRIDGE-02-content-bundle-registry.md` |
| **$storyFile** (backlog AC SSOT) | `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-02-content-bundle-registry.md` |
| **Method** | Read/Glob only vs `src/aibridge/` + `tests/`; no product patches; no live pytest this pass |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P4 · contract §6 |

## Verdict

| Axis | Result |
|------|--------|
| **Story AC (backlog Target / AC #1–#5)** | **PASS** on Memory/Sqlite path + unit tests |
| **Bullrun story/task Done (t01–t06)** | **Confirmed** as labels; gate artifact PASS 2026-09-12T21:03:47Z |
| **OPEN gaps (actionable residual)** | **1 Medium** + **1 Info** |
| **Critical OPEN** | **0** |
| **Live pytest this pass** | **Unknown**; historical claim 31 passed @ gate Date; inventory ≈31 `def test_*` across story 01+02 suites |

---

## Bullrun touchpoints (статусы в отчёте — product index не переписывался)

| ID | Bullrun claim | P4 fact status |
|----|---------------|----------------|
| Story STORY-AIBRIDGE-02 | 🟢 Done | **AC Done confirmed**; residual Postgres gap below |
| t01 content-load-hash-pin | Done | **Confirmed** — `content.py`; `tests/test_content.py` |
| t02 postgres-bundle-registry | Done | **Partial vs name** — Memory+Sqlite register-once OK; **Postgres DSN NotImplemented** (G-01) |
| t03 readyz-bundle-verify | Done | **Confirmed** — `deployment.py` + `app.py` `/readyz`; `tests/test_readyz_bundle.py` |
| t04 session-bundle-pin | Done | **Confirmed** — `sessions.py` `resume_bundle`; `tests/test_session_pin.py` |
| t05 bundle-gc-ci-docs | Done | **Confirmed** — `bundle_gc.py`; arch `02-content-packaging.md` §3; `tests/test_bundle_gc.py` |
| t06 story-acceptance-verification | Done | **Confirmed artifact** — gate Result PASS |

---

## AC matrix (`$storyFile` Target / AC)

| # | AC | Status | Evidence |
|---|-----|--------|----------|
| 1 | Missing/mismatched artifacts → `/readyz` not ready | **PASS** | `deployment.py` `verify_and_register_deployment` → error; `app.py` `/readyz` 503 when `content_configured()` and not `dep.ready`; `tests/test_readyz_bundle.py::test_readyz_fails_missing_pack` |
| 2 | Redeploy new bundle does not delete prior hash while session refs it | **PASS** | `bundle_gc.py` skips `active_bundle_hashes()`; `tests/test_bundle_gc.py::test_gc_skips_referenced_and_honors_grace` |
| 3 | Bundle row immutable after register; uniqueness on `bundle_hash` | **PASS** (Memory/Sqlite) | `registry.py` PK + `register_once` returns existing (no UPDATE); `tests/test_registry.py` |
| 4 | No GitHub fetch of instructions at request time | **PASS** | `content.py` local FS only; Grep `src/aibridge`: no `httpx`/`requests`/`urllib`/`github`; `tests/test_content.py::test_loader_has_no_github_fetch_api` |
| 5 | Session resume uses pinned `content_bundle_hash` | **PASS** | `sessions.py` `resume_bundle` loads `registry.get(session.content_bundle_hash)`; `tests/test_session_pin.py` |

### Scope extras

| Item | Status | Evidence |
|------|--------|----------|
| Manifest load + hash + `DOGESTONIA_CONTENT_SOURCE_COMMIT` | **PASS** | `content.py` `load_content_bundle`; `config.py` env aliases |
| Wire OAS `story-intake-actions.openapi.yaml` | **PASS** | Path used in tests; file on disk `docs/openapi/story-intake-actions.openapi.yaml` |
| Register-once after verify | **PASS** | `deployment.py` → `registry.register_once` |
| CI multi-repo → tarball note | **PASS** | `docs/architecture/runtime/02-content-packaging.md` §3 |
| GC grace rule | **PASS** (library) | `bundle_gc.py`; grace env `AIBRIDGE_BUNDLE_GC_GRACE_SECONDS` in `config.py` — **no** call site in `app.py` (Info residual G-02) |
| PostgreSQL as chosen store (arch §4 / story title) | **FAIL residual** | See **G-01** |

---

## Gaps

| ID | Severity | Area | Finding | How to close (findings only) |
|----|----------|------|---------|------------------------------|
| **G-01** | **Medium** | Postgres registry | Story title / arch `02-content-packaging.md` §4 («Chosen store: PostgreSQL», multi-instance share) vs fact: `open_bundle_registry` / `open_session_store` raise `NotImplementedError` for `postgresql://` (`registry.py` ~208–213, `sessions.py` ~206–209). Runtime uses Memory+Sqlite. Pipeline verified-state documents deferral; t02 acceptance passed on Sqlite only. Production Postgres DSN → `_init_stores` fail-closed (`database_adapter_unavailable`) without shared PG registry. | Wire Postgres adapter matching logical SQL shape; integration tests with `postgresql://`; keep fail-closed until ready. |
| **G-02** | **Info** | Ops / docs hygiene | (a) `gc_unreferenced_bundles` has no invocation from `app.py`/lifecycle (library+unit only). (b) t02 README «Code Facts» still says «No Postgres… yet» / DoD checkboxes unchecked while Status Done. | Document operator GC trigger or schedule; refresh t02 README facts to match disk. |

### Non-gaps / out of DoD this wave

| Topic | Note |
|-------|------|
| Channel handlers not creating sessions yet | Story 03 Responses/session engine; AC #5 covered by `SessionStore` API + tests |
| Absolute CI checkout paths | Documented **Unknown**/env — backlog + arch §3 |
| Live pytest re-run | Not executed this P4 |

---

## Regressions

None observed against story 01 channel façade modules still present under `src/aibridge/` + prior tests.

---

## Cited paths

- `doge-ai-bridge/src/aibridge/content.py`
- `doge-ai-bridge/src/aibridge/registry.py`
- `doge-ai-bridge/src/aibridge/sessions.py`
- `doge-ai-bridge/src/aibridge/bundle_gc.py`
- `doge-ai-bridge/src/aibridge/deployment.py`
- `doge-ai-bridge/src/aibridge/app.py`
- `doge-ai-bridge/src/aibridge/config.py`
- `doge-ai-bridge/tests/test_content.py`
- `doge-ai-bridge/tests/test_registry.py`
- `doge-ai-bridge/tests/test_readyz_bundle.py`
- `doge-ai-bridge/tests/test_session_pin.py`
- `doge-ai-bridge/tests/test_bundle_gc.py`
- `doge-ai-bridge/docs/architecture/runtime/02-content-packaging.md`
- `doge-ai-bridge/docs/openapi/story-intake-actions.openapi.yaml`

---

## Handoff

- **OPEN:** G-01 (Medium), G-02 (Info)
- **Critical:** 0
- **next:** **P5** disposition for G-01/G-02
- Product Story AC Done **≠** empty residual gap list — both recorded
