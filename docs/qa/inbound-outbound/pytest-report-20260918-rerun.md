# pytest report — QA inbound/outbound re-run (stories 23–35)

**Date:** 2026-09-18 (re-run)  
**Host:** local macOS · `doge-ai-bridge` · Python 3.11.4 · pytest 9.1.1  
**Method:** analysis.mdc — claims from captured stdout only  
**Baseline:** [`pytest-report-20260918.md`](./pytest-report-20260918.md) (232 passed / 12 skipped, no disposable PG)  
**Manual:** [`TEST-MANUAL.md`](./TEST-MANUAL.md)

---

## 1. Environment facts

| Check | Result |
|-------|--------|
| Disposable PG script | `./scripts/start-disposable-pg.sh` — operator Terminal (outside agent sandbox); agent sandbox still hits `shmget: Operation not permitted` |
| Authoritative suite host | Operator shell: **244 passed, 0 skipped** |
| Agent re-capture (same command) | **232 passed, 12 skipped** — `pg_available()` False under sandbox (cannot attach/start `.pgdata-test`) |
| Optional smoke | `GET http://127.0.0.1:8080/healthz` → `{"status":"ok"}` (process already up; not a Postgres proof) |

**Что не чинили в этой волне:** product/runtime/test code; только docs-отчёты.

---

## 2. Pytest command

```bash
cd doge-ai-bridge
./scripts/start-disposable-pg.sh   # operator Terminal; verify pg_available True
.venv/bin/pytest -ra --tb=line \
  tests/contract/ \
  tests/unit/test_tool_call_validation.py \
  tests/unit/test_action_token_fsm.py \
  tests/n8n/ \
  tests/integration/ \
  tests/test_qa_gates_layers_dod.py
```

### 2a. Authoritative run (operator Terminal — with disposable PG)

Источник: локальный Terminal session после start-disposable-pg (stdout зафиксирован).

| Metric | Value |
|--------|------:|
| Collected | 244 |
| **Passed** | **244** |
| Failed | 0 |
| Skipped | 0 |
| Errors | 0 |
| Exit code | 0 |
| Duration | ~2.24s (`-ra`) / ~2.38s (`-q`) |
| Warnings | 2 (Starlette/httpx TestClient deprecation) |

Per-module (все точки = pass):

| Module | Outcome |
|--------|---------|
| `tests/contract/test_auth_ops_boundaries.py` | 16 pass |
| `tests/contract/test_json_schema_boundary.py` | 21 pass |
| `tests/contract/test_readyz_configuration.py` | 21 pass |
| `tests/unit/test_tool_call_validation.py` | 18 pass |
| `tests/unit/test_action_token_fsm.py` | 22 pass |
| `tests/n8n/test_n8n_telegram_mapping.py` | 19 pass |
| `tests/integration/test_action_token_fsm_http.py` | 7 pass |
| `tests/integration/test_gateway_continuation.py` | 23 pass |
| `tests/integration/test_idempotency_concurrency.py` | 13 pass |
| `tests/integration/test_lifecycle_retention.py` | 18 pass (incl. live rebuild) |
| `tests/integration/test_openai_prompt_behavior.py` | 18 pass |
| `tests/integration/test_privacy_observability.py` | 12 pass |
| `tests/integration/test_product_journey_scenarios.py` | 11 pass (UC packs + UC-01…10) |
| `tests/test_qa_gates_layers_dod.py` | 25 pass |

### 2b. Agent re-capture (sandbox — no disposable PG)

| Metric | Value |
|--------|------:|
| Collected | 244 |
| Passed | 232 |
| Failed | 0 |
| Skipped | 12 |
| Errors | 0 |
| Exit code | 0 |
| Duration | ~1.09s |

Skips (все — disposable PG):

| # | Node | Reason |
|---|------|--------|
| 1 | `tests/integration/test_lifecycle_retention.py:557` `test_g01_life_rebuild_app_same_pg_live` | disposable Postgres not running |
| 2–12 | `tests/integration/test_product_journey_scenarios.py` (module `pytestmark` + 11 tests) | disposable Postgres (`.pgdata-test`) not running — `./scripts/start-disposable-pg.sh` |

---

## 3. Comparison vs baseline [`pytest-report-20260918.md`](./pytest-report-20260918.md)

| | Baseline (no PG) | Re-run authoritative (with PG) | Delta |
|--|-----------------:|-------------------------------:|------|
| Passed | 232 | **244** | **+12** |
| Skipped | 12 | **0** | **−12** |
| Failed | 0 | 0 | 0 |
| UC-01…10 + fixture hash_eq | skipped | **executed / passed** | unblocked |
| LIFE `rebuild_app_same_pg_live` | skipped | **passed** | unblocked |

Baseline root cause (stale shm / PG down) resolved on operator host via improved `start-disposable-pg.sh` + Terminal (not agent sandbox).

---

## 4. Story × layer × результат (authoritative)

| Story | Layer / modules | Authoritative re-run |
|-------|-----------------|----------------------|
| 23 AUTH | `tests/contract/test_auth_ops_boundaries.py` | pass |
| 24 VAL | `tests/contract/test_json_schema_boundary.py` | pass |
| 25 N8N | `tests/n8n/test_n8n_telegram_mapping.py` | pass |
| 26 IDEM | `tests/integration/test_idempotency_concurrency.py` | pass |
| 27 OAI | `tests/integration/test_openai_prompt_behavior.py` | pass |
| 28 TOOL | `tests/unit/test_tool_call_validation.py` | pass |
| 29 ACT | `tests/unit/test_action_token_fsm.py` + `tests/integration/test_action_token_fsm_http.py` | pass |
| 30 GW | `tests/integration/test_gateway_continuation.py` | pass |
| 31 LIFE | `tests/integration/test_lifecycle_retention.py` | pass (incl. live rebuild on disposable PG) |
| 32 SEC | `tests/integration/test_privacy_observability.py` | pass |
| 33 READY | `tests/contract/test_readyz_configuration.py` | pass |
| 34 UC | `tests/integration/test_product_journey_scenarios.py` | pass (11/11) |
| 35 Gates/DoD | `tests/test_qa_gates_layers_dod.py` | pass (Gate-5 / Layer F still **deferred_live** by design) |

---

## 5. Fixture index vs disk

| Check | Result |
|-------|--------|
| Index rows (`tests/fixtures/meta/fixture-index.json`) | 224 |
| Paths present on disk | **224 / 224** (missing **0**) |

---

## 6. Fail table

| Failures | — |
|----------|---|
| None | 0 failed / 0 errors on both authoritative and agent captures |

---

## 7. Explicit non-claims

- Green pytest ≠ live Telegram / Railway Gate-5 (still `deferred_live` in gates suite).
- Green UC journeys ≠ live Bot API; harness uses Recording OpenAI/Gateway + disposable PG.
- Agent sandbox stdout alone must not be cited as «PG unavailable forever» — operator run proves PG path works.
- No product/test fixes applied in this docs wave.
