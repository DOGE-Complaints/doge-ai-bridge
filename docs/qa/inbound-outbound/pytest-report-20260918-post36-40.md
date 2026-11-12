# pytest report — QA inbound/outbound post stories 36–40

**Date:** 2026-09-18 (post-36–40)  
**Host:** local macOS · `doge-ai-bridge` · Python 3.11.4 · pytest 9.1.1  
**Method:** analysis.mdc — claims from captured stdout only  
**Baselines:** [`pytest-report-20260918-rerun.md`](./pytest-report-20260918-rerun.md) (244 pass / 0 skip with PG · suite without honesty modules)  
**Package:** stories 36–40 Done (P3) per [`INDEX.md`](../../tasks/backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)

---

## 1. Environment facts

| Check | Result |
|-------|--------|
| Authoritative host | **Operator Terminal** after `./scripts/start-disposable-pg.sh` |
| Agent sandbox (earlier) | `shmget` blocked PG → 251 pass / 12 skip |
| Optional smoke | not required for this wave |

**Что не чинили в docs wave:** product/runtime (кроме уже Done 36–40); этот файл — факты прогона.

---

## 2. Pytest command

```bash
cd doge-ai-bridge
./scripts/start-disposable-pg.sh
.venv/bin/pytest -ra --tb=line \
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

### 2a. Authoritative (operator Terminal + disposable PG)

Источник: Terminal session (stdout **263 passed**).

| Metric | Value |
|--------|------:|
| Collected | **263** |
| **Passed** | **263** |
| Failed | **0** |
| Skipped | **0** |
| Errors | 0 |
| Exit code | 0 |
| Duration | ~2.63–2.76s |
| Warnings | 2 (Starlette/httpx TestClient deprecation) |

All modules including LIFE live rebuild, UC-01…10, and honesty 36/37/39 — **pass**.

### 2b. Agent earlier capture (no PG)

| Metric | Value |
|--------|------:|
| Collected | 263 |
| Passed | 251 |
| Skipped | 12 (UC + LIFE live — disposable PG) |
| Exit code | 0 |

---

## 3. Skips / fails (authoritative)

| Failures / skips | — |
|------------------|---|
| None | 0 failed / 0 skipped |

---

## 4. Comparison vs baselines

| | Rerun (PG, no honesty) | Post-36–40 authoritative (PG + honesty) |
|--|-----------------------:|----------------------------------------:|
| Collected | 244 | **263** (+19) |
| Passed | 244 | **263** |
| Skipped | 0 | **0** |
| Failed | 0 | 0 |

---

## 5. Story × layer × результат (authoritative)

| Story | Modules | Result |
|-------|---------|--------|
| 23–33, 35 | contract/unit/n8n/integration/gates | pass |
| 31 LIFE live | `test_g01_life_rebuild_app_same_pg_live` | **pass** |
| 34 UC | `test_product_journey_scenarios.py` (11) | **pass** |
| 36 | `test_n8n_wf_001_pin_honesty.py` | pass |
| 37 | `test_gate5_evidence_honesty.py` | pass |
| 38 | OAI + char-006 | pass |
| 39 | `test_char008_send_edit_capture_honesty.py` | pass |
| 40 | VAL hygiene in contract | pass |

---

## 6. Fixture index vs disk

| Check | Result |
|-------|--------|
| Index rows | **230** |
| Present on disk | **230 / 230** |

---

## 7. Matrix honesty (vs [`MATRIX-COVERAGE-VERIFICATION.md`](../../tasks/backlog-stories/qa-inbound-outbound-data-flow/MATRIX-COVERAGE-VERIFICATION.md))

**MATRIX-COVERAGE-VERIFICATION.md (as-of 2026-09-17)** verifies only **постановка** (186 guide IDs ↔ story bodies) — explicit note: *not test implementation*.

**TRACEABILITY now:** 190 rows. Status mix (parsed from matrix Coverage column):

| Coverage class | Count | Meaning for «полное тестирование Expected» |
|----------------|------:|---------------------------------------------|
| `covered` (strict) | 158 | Automated suite claims behavioral cover |
| `fixture-covered` (N8N-001…018) | 18 | Adapter-contract fixtures — **not** live n8n/Bot API |
| `PG-journey covered` (UC-01…10) | 10 | Disposable PG + Recording OAI/GW — **≠ Gate-5 live** |
| `deferred` | 3 | N8N-WF-001, Gate-5, CHAR-008 — honesty green on defer |
| `waived` | 1 | QUAL-003 |

Export file `docs/ops/n8n-channel-workflow/exports/aibridge-telegram-channel-v1.json`: **absent** (verified).

**Verdict:** **263 passed ≠ full honest e2e of every matrix Expected.** Suite is green and UC/LIFE-live ran under PG; live Telegram / n8n workflow / Gate-5 pilot / CHAR-008 Send-Edit capture remain **deferred or fixture-level** by design.

---

## 8. Explicit non-claims

- Green honesty modules assert **deferred** when export/pilot absent — not Gate-5 PASS / workflow runtime.
- N8N-* fixture-covered ≠ production n8n graph execution.
- UC PG-journey ≠ resident Telegram → Railway live path.
