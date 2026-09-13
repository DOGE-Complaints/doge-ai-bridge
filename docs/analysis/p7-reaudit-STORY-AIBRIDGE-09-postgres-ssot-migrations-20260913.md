# P7 Re-audit — STORY-AIBRIDGE-09-postgres-ssot-migrations gap wave

| Field | Value |
|-------|-------|
| **Date** | 2026-09-13 |
| **builder_project** | `aibridge` |
| **$auditReport (P4)** | `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-09-postgres-ssot-migrations-20260913.md` |
| **$planFile** | `.cursor/plans/aibridge_builder.plan.md` §`run_mode=aibridge_09_audit_20260913` |
| **Method** | Read/Glob only; no product patches |
| **Thinking** | `.cursor/rules/analysis.mdc` · workflow §P7 |

## Disposition SSOT (P5)

| Gap | P5 disposition | follow_up | Task / story | Completeness |
|-----|----------------|-----------|--------------|--------------|
| G-01 | **TASKED** → claimed CLOSED | none | t08 `task-aibridge-02-09-t08-audit-g01-wire-pg-runtime-app` | OK |
| G-02 | **TASKED** → claimed CLOSED | none | t09 `task-aibridge-02-09-t09-audit-g02-gateway-attempt-before-https` | OK |

**P5_DISPOSITION_INCOMPLETE:** **no**

Sources: `bullrun-launch-index.md` §P5/P6 wave STORY-09; INDEX **P5 APPLY** 2026-09-13T15:29:22Z · **P6 Done** 2026-09-13T15:35:44Z (113 passed / 1 skipped).

---

## Per-gap verification

### G-01 — Wire pg_runtime into create_app (was TASKED → claimed CLOSED)

| Check | Result | Evidence |
|-------|--------|----------|
| Fact-code dedupe | **PASS** | `app.py`: `use_pg_runtime` → `PostgresEventDedupeStore` (+ migrations) |
| Fact-code confirm/tokens | **PASS** | `ConfirmationGuard(tokens=PostgresActionTokenStore, gateway_attempts=…, confirm_sessions=…)` |
| Fact-code turn/history | **PASS** | `app.state.turn_lock` / `history_store`; `channel.process_turn`/`process_action` take `turn_lock` |
| Fail-closed memory | **PASS** | PG path only when `postgresql://` and `AIBRIDGE_ALLOW_MEMORY_STORES=false` |
| Tests | **PASS** | `tests/test_app_pg_runtime_wire.py` — types + TestClient turn replay without manual inject |
| Residual P4 ASGI gap | **gone** | |
| **P7 result** | **CLOSED** | |

### G-02 — GatewayAttempt commit-before-HTTPS (was TASKED → claimed CLOSED)

| Check | Result | Evidence |
|-------|--------|----------|
| Fact-code order | **PASS** | `confirm.call_gateway`: `create_executing` then `execute_stash`; `set_outcome` after (error path marks internal) |
| Fail-closed duplicate | **PASS** | UniqueViolation → no second HTTPS; `test_duplicate_attempt_blocks_second_https` |
| Tests | **PASS** | `tests/test_gateway_attempt_before_https.py` — attempt row exists before transport.request |
| Residual P4 unused store | **gone** on wired Confirm path | |
| **P7 result** | **CLOSED** | |

---

## Wave scoreboard

| Metric | Count |
|--------|------:|
| Gaps in wave | 2 |
| CLOSED | **2** (G-01, G-02) |
| WAIVED | **0** |
| OPEN | **0** |
| Incomplete TASKED | **0** |
| Missing disposition | **0** |

**WAVE COMPLETE:** **yes** (0 OPEN · 0 incomplete TASKED)

Live pytest this P7: **Unknown**; historical P6 claim **113 passed / 1 skipped**.

---

## Handoff

- **next_phase_hint:** **P8**
- No re-P5/P6 for this gap wave
