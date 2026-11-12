# pytest report — QA inbound/outbound (stories 23–35)

**Date:** 2026-09-18  
**Host:** local macOS · `doge-ai-bridge` · Python 3.11.4 · pytest 9.1.1  
**Method:** analysis.mdc — claims from this run only (curl + pytest stdout)  
**Manual:** [`TEST-MANUAL.md`](./TEST-MANUAL.md) · **Matrices:** [`TRACEABILITY-MATRIX.md`](./TRACEABILITY-MATRIX.md)

---

## 1. Server smoke

| Step | Result (fact) |
|------|----------------|
| Start | `PORT=18080` · `AIBRIDGE_ALLOW_MEMORY_STORES=true` · Channel ≠ Gateway Bearer · `AIBRIDGE_DRY_RUN=true` · `python -m aibridge` |
| `GET /healthz` | **200** `{"status":"ok"}` |
| `GET /readyz` | **200** `{"status":"ready"}` |
| Stop | Process on `:18080` terminated after suite |

Note: memory-stores smoke is **not** a Postgres readiness proof.

---

## 2. Pytest command

```bash
cd doge-ai-bridge
.venv/bin/pytest -ra --tb=line \
  tests/contract/ \
  tests/unit/test_tool_call_validation.py \
  tests/unit/test_action_token_fsm.py \
  tests/n8n/ \
  tests/integration/ \
  tests/test_qa_gates_layers_dod.py
```

| Metric | Value |
|--------|------:|
| Collected | 244 |
| **Passed** | **232** |
| **Failed** | **0** |
| **Skipped** | **12** |
| Errors | 0 |
| Exit code | 0 |
| Duration | ~1.15s |
| Warnings | 2 (Starlette/httpx TestClient deprecation — tooling, not product AC) |

---

## 3. Skips (all environment — disposable Postgres)

| # | Node / location | Reason (pytest) |
|---|-----------------|-----------------|
| 1 | `tests/integration/test_lifecycle_retention.py:557` `test_g01_life_rebuild_app_same_pg_live` | disposable Postgres not running |
| 2–12 | `tests/integration/test_product_journey_scenarios.py` (module `pytestmark` + 11 tests: fixture pack hash_eq + UC-01…10) | disposable Postgres (`.pgdata-test`) not running — `./scripts/start-disposable-pg.sh` |

**Attempt to start PG during this run:** `bash scripts/start-disposable-pg.sh` failed. Log fact:

```text
FATAL: pre-existing shared memory block (key 212010891, ID 131074) is still in use
HINT: Terminate any old server processes associated with data directory ".../doge-ai-bridge/.pgdata-test"
```

`pg_available()` remained **False**. UC-01…10 and the live `rebuild_app_same_pg` LIFE probe were **not executed** in this environment.

---

## 4. Story × layer map (this run)

| Story | Layer / modules | This run |
|-------|-----------------|----------|
| 23 AUTH | `tests/contract/test_auth_ops_boundaries.py` | green (passed within contract block) |
| 24 VAL | `tests/contract/test_json_schema_boundary.py` | green |
| 25 N8N | `tests/n8n/test_n8n_telegram_mapping.py` | green |
| 26 IDEM | `tests/integration/test_idempotency_concurrency.py` | green |
| 27 OAI | `tests/integration/test_openai_prompt_behavior.py` | green |
| 28 TOOL | `tests/unit/test_tool_call_validation.py` | green |
| 29 ACT | `tests/unit/test_action_token_fsm.py` + `tests/integration/test_action_token_fsm_http.py` | green |
| 30 GW | `tests/integration/test_gateway_continuation.py` | green |
| 31 LIFE | `tests/integration/test_lifecycle_retention.py` | **partial** — 1 skip (`rebuild_app_same_pg_live`); other LIFE tests passed on memory/Recording paths |
| 32 SEC | `tests/integration/test_privacy_observability.py` | green |
| 33 READY | `tests/contract/test_readyz_configuration.py` | green |
| 34 UC | `tests/integration/test_product_journey_scenarios.py` | **all 11 collected tests skipped** (no disposable PG) |
| 35 Gates/DoD | `tests/test_qa_gates_layers_dod.py` | green (includes Gate-5 / Layer F **deferred_live** asserts) |

---

## 5. Fixture index vs disk (fact)

| Check | Result |
|-------|--------|
| `tests/fixtures/meta/fixture-index.json` rows | 224 |
| Paths present on disk | **224 / 224** (missing 0) |
| Cluster dirs | `channel`, `content`, `gateway`, `meta`, `n8n`, `openai`, `settings`, `spies`, `telegram` |
| `*.json` under `tests/fixtures/` | 227 (index + extras e.g. content / bad-tool-gen) |

No index↔disk gap in this tree.

---

## 6. Gaps / недоработки (actionable)

### P0 — blocked on this host (ops)

1. **Disposable Postgres stale shm** — `.pgdata-test` cannot start (`shared memory block still in use`). Until cleaned/restarted, **story 34 (UC-01…10)** and **LIFE live rebuild** stay skipped.  
   - Operator action: terminate leftover `postgres` for that datadir, then `./scripts/start-disposable-pg.sh`, re-run integration UC + `test_g01_life_rebuild_app_same_pg_live`.

### P1 — coverage / product gaps (from suite design, not fails)

2. **Gate-5 / Layer F live channel** — explicitly `deferred_live` in gates suite (no live Telegram/Railway in default CI). Still a **program gap** until pilot evidence exists.  
3. **Layer D container** — deferred + bound to Dockerfile/STORY-21/22 proofs in gates tests; not exercised as image smoke in this run.  
4. **CHAR-008** — suite requires `defer_reason` (no Send/Edit fixture yet) — characterization still open product/workflow decision.  
5. **Statement matrix = 186 IDs** vs **244 pytest nodes** — many IDs map to parametrized/multiple tests; conversely **UC journey automation did not run here**. Do not claim “186 automated green” from this report alone.

### P2 — hygiene

6. **Starlette/httpx TestClient deprecation** — 2 warnings; upgrade path when FastAPI/Starlette allow (`httpx2`).  
7. **Memory `/readyz` ready** in smoke with `AIBRIDGE_ALLOW_MEMORY_STORES=true` — useful for process up, but **not** SSOT for production Postgres readiness (READY-012/013 need real PG).

### Not gaps (verified green in this run)

- Contract AUTH/VAL/READY, unit TOOL/ACT, n8n mapping, IDEM/OAI/GW/SEC integration (non-PG-skip paths), gates checklist suite, fixture promote index integrity.

---

## 7. What this wave did **not** do

- Fix product/runtime code to “make skips pass”.  
- Clear/restart disposable Postgres shm (ops on host).  
- Live Gate-5 pilot.  
- Push / commit (unless separately requested).

---

## 8. Recommended next operator steps

1. Clear stale PG on `.pgdata-test` → start script → re-run:

```bash
.venv/bin/pytest -ra --tb=short \
  tests/integration/test_product_journey_scenarios.py \
  tests/integration/test_lifecycle_retention.py::test_g01_life_rebuild_app_same_pg_live
```

2. Attach results as `pytest-report-YYYYMMDD-pg.md` beside this file.  
3. Schedule Gate-5 live pilot evidence under runbook (out of default CI).
