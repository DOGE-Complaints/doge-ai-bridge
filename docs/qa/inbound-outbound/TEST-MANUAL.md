# TEST MANUAL — QA inbound/outbound (stories 23–35)

**Service:** `doge-ai-bridge`  
**Matrices:** [`TRACEABILITY-MATRIX.md`](./TRACEABILITY-MATRIX.md) · [`MATRIX-COVERAGE-VERIFICATION.md`](./MATRIX-COVERAGE-VERIFICATION.md)  
**Guide:** [`../../tasks/qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../tasks/qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)  
**Tech arch:** [`../../tasks/backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md`](../../tasks/backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md)  
**Package:** [`../../tasks/backlog-stories/qa-inbound-outbound-data-flow/INDEX.md`](../../tasks/backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)

---

## 1. Prefs

```bash
cd doge-ai-bridge
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## 2. Env (minimum for smoke)

Channel Bearer **≠** Gateway Bearer. Prefer values from `.env.example` / Phase A pins when testing `/readyz`.

```bash
export AIBRIDGE_CHANNEL_BEARER_TOKEN='dev-channel-token'
export GATEWAY_SERVICE_API_TOKEN='dev-gateway-token-different'
export AIBRIDGE_DRY_RUN=true
# Optional memory path for process smoke without Postgres:
# export AIBRIDGE_ALLOW_MEMORY_STORES=true
```

Full local/Railway pins: [`../../runbooks/aibridge-web-service-local-railway.md`](../../runbooks/aibridge-web-service-local-railway.md).

## 3. Server smoke

```bash
cd doge-ai-bridge
PORT=8080 PYTHONPATH=src .venv/bin/python -m aibridge
# or:
# PYTHONPATH=src .venv/bin/python -m uvicorn --app-dir src aibridge.app:app --host 127.0.0.1 --port 8080
```

In another shell:

```bash
curl -sS -i http://127.0.0.1:8080/healthz
curl -sS -i http://127.0.0.1:8080/readyz
```

| Expect | Notes |
|--------|--------|
| `/healthz` → **200** `{"status":"ok"}` | No Bearer |
| `/readyz` → **200** ready or **503** + bounded `reason` | Incomplete env is OK for smoke; record the reason |

Most QA pytest modules use `TestClient` + Recording\* doubles — they do **not** need a live server. Server smoke is for process/wiring confidence.

## 4. Pytest — QA suite (23–40)

```bash
cd doge-ai-bridge
.venv/bin/pytest -q \
  tests/contract/ \
  tests/unit/test_tool_call_validation.py \
  tests/unit/test_action_token_fsm.py \
  tests/n8n/ \
  tests/integration/ \
  tests/test_qa_gates_layers_dod.py \
  tests/test_n8n_wf_001_pin_honesty.py \
  tests/test_gate5_evidence_honesty.py \
  tests/test_char008_send_edit_capture_honesty.py
```

Verbose / JUnit-style summary:

```bash
.venv/bin/pytest -ra \
  tests/contract/ \
  tests/unit/test_tool_call_validation.py \
  tests/unit/test_action_token_fsm.py \
  tests/n8n/ \
  tests/integration/ \
  tests/test_qa_gates_layers_dod.py \
  tests/test_n8n_wf_001_pin_honesty.py \
  tests/test_gate5_evidence_honesty.py \
  tests/test_char008_send_edit_capture_honesty.py
```

### Layers ↔ stories (tech-arch §5.1)

| Layer | Paths | Stories |
|-------|-------|---------|
| Contract | `tests/contract/` | 23 AUTH, 24 VAL, 33 READY |
| Unit | `tests/unit/test_tool_call_validation.py`, `test_action_token_fsm.py` | 28 TOOL, 29 ACT |
| n8n | `tests/n8n/` | 25 N8N |
| Integration | `tests/integration/` | 26–32, 34 UC |
| Gates / DoD | `tests/test_qa_gates_layers_dod.py` | 35 |

Fixtures: `tests/fixtures/{telegram,openai,gateway,channel,settings,n8n,spies,meta}/` (envelope v1.0). Loader: `tests/fixture_loader.py`.

## 5. Postgres: две разные штуки

### A) Homebrew / «из коробки» — для локального **сервиса** aibridge

Нужен, если в `.env` стоит обычный `DATABASE_URL=postgresql://…@localhost:5432/…` и вы поднимаете `python -m aibridge`.

```bash
brew services start postgresql@15
# стоп: brew services stop postgresql@15
# статус: brew services list | grep postgres
```

См. также runbook: [`../../runbooks/aibridge-web-service-local-railway.md`](../../runbooks/aibridge-web-service-local-railway.md) §1 (локальный Postgres).

**Это само по себе не снимает skip со story 34.**

### B) Disposable `.pgdata-test` — для **QA pytest** (UC-01…10 / часть LIFE)

Тесты вызывают `pg_available()` → подключение к **отдельному** кластеру в `doge-ai-bridge/.pgdata-test` (порт `55432`), не к Homebrew на `:5432`.

```bash
cd doge-ai-bridge
./scripts/start-disposable-pg.sh
```

Скрипт сам: если порт `55432` занят «осиротевшим» postgres / залип shm — останавливает listener и поднимает кластер заново; в конце проверяет `SELECT 1`.

Если вручную нужно прибить старый процесс:

```bash
lsof -nP -iTCP:55432 -sTCP:LISTEN
# kill -9 <PID>
./scripts/start-disposable-pg.sh
```

**Не запускай скрипт из sandbox-агента Cursor** — там `shmget` часто даёт `Operation not permitted`. Нужен обычный Terminal / iTerm.

Проверка, что UC снова могут бежать:

```bash
.venv/bin/python -c "from tests.story13_e2e_helpers import pg_available; print(pg_available())"
# ожидается: True
.venv/bin/pytest -q tests/integration/test_product_journey_scenarios.py
```

Until `pg_available()` is true, story **34** UC suite and `test_g01_life_rebuild_app_same_pg_live` will **skip**.

Default CI-oriented run (§4) still exercises memory/Recording\* paths for most matrix IDs.

## 6. What not to claim from this manual

- Live Telegram / n8n / Railway SUCCESS (Gate-5 pilot) — out of default suite.
- Statement «186 IDs covered» without matching pytest nodeids — use latest `pytest-report-*.md` in this folder.

## 7. After a run

Write or update `pytest-report-YYYYMMDD.md` here with pass/fail/skip counts and gaps (facts only).
