# Test qualification — QA suite stories 23–35

**Date:** 2026-09-18  
**Package SSOT:** this file · **Ops pointer:** [`../../../qa/inbound-outbound/test-qualification-20260918.md`](../../../qa/inbound-outbound/test-qualification-20260918.md)  
**Method:** [`.cursor/rules/test-qualification.mdc`](../../../../../.cursor/rules/test-qualification.mdc) + analysis.mdc (evidence = source asserts / skips; green ≠ qualified)  
**Suite scope:** same paths as ops [`TEST-MANUAL.md`](../../../qa/inbound-outbound/TEST-MANUAL.md) / [`pytest-report-20260918-rerun.md`](../../../qa/inbound-outbound/pytest-report-20260918-rerun.md)  
**Authoritative green facts:** 244 passed / 0 skipped (operator Terminal + disposable PG)  
**This wave (2026-09-18 transfer):** docs only — **no** test/product autofix; gap closure owned by stories **36–40**

---

## 0. Gap → story map

| Finding | Priority | Closure story | Status (2026-09-18T13:03:40Z) |
|---------|----------|---------------|-------------------------------|
| P0-Q1 | P0 | [`STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty`](./STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md) | See STORY-36 wave |
| P2-Q1 | P2 | STORY-36 | See STORY-36 wave |
| P0-Q2 | P0 | [`STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence`](./STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md) | **closed-with-defer** (UC≠Gate-5 honesty + Gate-5 evidence deferred explicit · pkg-000036) |
| P0-Q3 | P0 | STORY-37 | **closed-with-defer** (`deferred_live` recorded · live pack not accepted · no invent) |
| P2-Q3 | P2 | STORY-37 | **closed-with-defer** (CI mock-heavy accepted · Gate-5 remains out-of-CI) |
| P1-Q2 | P1 | [`STORY-AIBRIDGE-38-qa-oai-channel-error-outcome`](./STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md) (CHAR-006) | **closed** (Option A · P3 2026-09-18T13:43:00Z) |
| P1-Q3 | P1 | [`STORY-AIBRIDGE-39-qa-char008-send-edit-capture`](./STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md) (CHAR-008) | Closed-with-defer (P3 2026-09-18T14:06:43Z · export absent) |
| P1-Q1 | P1 | [`STORY-AIBRIDGE-40-qa-suite-assert-hygiene`](./STORY-AIBRIDGE-40-qa-suite-assert-hygiene.md) | **closed** (VAL band removed · P3 2026-09-18T14:28:02Z) |
| P1-Q4 | P1 | STORY-40 | **closed** (hash_eq integrity-only DoD · P3 2026-09-18T14:28:02Z) |
| P2-Q2 | P2 | STORY-40 | **closed-with-waive** (QUAL-003 WAIVE gaps §40 · P3 2026-09-18T14:28:02Z) |

---

## 1. Inventory

| Module | Role | Claimed matrix / story |
|--------|------|------------------------|
| `tests/contract/test_auth_ops_boundaries.py` | HTTP auth/ops boundaries | AUTH-* (STORY-23) |
| `tests/contract/test_json_schema_boundary.py` | `/turns` schema / VAL | VAL-* (STORY-24) |
| `tests/contract/test_readyz_configuration.py` | `/readyz` config | READY-* (STORY-33) |
| `tests/unit/test_tool_call_validation.py` | Tool-call validation | TOOL-* (STORY-28) |
| `tests/unit/test_action_token_fsm.py` | Action token FSM (unit) | ACT-* (STORY-29) |
| `tests/integration/test_action_token_fsm_http.py` | ACT over HTTP | ACT-* (STORY-29) |
| `tests/n8n/test_n8n_telegram_mapping.py` | Fixture mapping ↔ N8N matrix | N8N-001…018 (STORY-25) |
| `tests/integration/test_idempotency_concurrency.py` | IDEM | IDEM-* (STORY-26) |
| `tests/integration/test_openai_prompt_behavior.py` | OAI | OAI-* (STORY-27) |
| `tests/integration/test_gateway_continuation.py` | GW + RecordingGatewayTransport | GW-* (STORY-30) |
| `tests/integration/test_lifecycle_retention.py` | LIFE (+ 1 live PG rebuild) | LIFE-* (STORY-31) |
| `tests/integration/test_privacy_observability.py` | SEC | SEC-* (STORY-32) |
| `tests/integration/test_product_journey_scenarios.py` | UC-01…10 E2EHarness + real disposable PG | UC-* (STORY-34) |
| `tests/test_qa_gates_layers_dod.py` | Gates / layers / CHAR meta | Gate-1…5, CHAR-*, Layer A–F (STORY-35) |

**Antipattern grep (suite paths):** `assert True` — none as sole body; `hash_eq` promote tests — present in most modules; `DATABASE_URL=memory` + `RecordingGatewayTransport` — dominant outside UC/LIFE-live; Gate-5 `deferred_live` — explicit.

---

## 2. Per-module review (summary)

| Module | What actually asserts | Mis-level / mock risk | Verdict seed |
|--------|----------------------|----------------------|--------------|
| AUTH contract | Status, error codes, bearer absence in body/metrics | Memory stores; no live PG | OK for contract; not e2e |
| VAL contract | Schema 4xx/2xx from fixtures; 2 characterization cases | **band removed** · VAL-014/018 explicit `== 200` (was tautology `100<=status<600` → **closed P1-Q1 / STORY-40 P3**) | See P1-Q1 |
| READY contract | ready/not-ready reasons, hash_eq package | Memory + Recording GW for some probes | OK contract |
| TOOL / ACT unit | FSM/tool logic + Recording GW | Unit correctly leveled | OK |
| ACT HTTP | HTTP + Recording | Integration-lite | OK |
| N8N | Fixture JSON + pure Python helpers (`render_outbound_keyboard`, timeline sim) | **No n8n workflow binary / no Bot API** — matrix Expected is workflow behavior | See P0-Q1, P2-Q1 |
| IDEM / OAI / SEC / GW | ASGI + memory + Recording doubles | Strong for channel contract; not live OAI/GW | See P2-Q2; OAI char → P1-Q2 |
| LIFE | Mix: Fake PG conn, memory, **one** live `rebuild_app_same_pg` | Live path now green with disposable PG | Live path OK when PG up |
| UC journey | Real disposable PG + Recording OAI/GW; some `dry_run_gateway=True` | Labeled E2E but **not** live Telegram/Railway | See P0-Q2, P2-Q3 |
| Gates/DoD | Index JSON status, file existence of refs/bound_tests | Gate-5 / Layer F / Layer D / CHAR-008 **documented defer** that still pass | See P0-Q3, P1-Q3 |

---

## 3. Findings (priority table)

### P0 — NO_FALSE_SUCCESSES / VALIDATE_REAL_FUNCTIONALITY / NO_UNTESTED_CRITICAL_PATHS

| ID | Location | Evidence | Risk | Recommendation (no autofix this wave) |
|----|----------|----------|------|----------------------------------------|
| **P0-Q1** | `tests/n8n/test_n8n_telegram_mapping.py` — e.g. `test_edited_message_characterization_capture_first`, `test_unsupported_media_no_turns`, `test_message_flow_maps_to_turns` | Asserts fixture flags (`must_not_map_as_ordinary_message`, `workflow_supports_edited is False`, keyboard helpers) — **never executes n8n workflow JSON / Telegram API**. Matrix Expected (TRACEABILITY N8N-001…018) describes live adapter behavior. | Suite can stay green while production n8n graph diverges → **false confidence** that STORY-25 is e2e-covered. | Keep layer label honest (`E_n8n` fixture contract). Add Gate-5 / workflow export snapshot or documented pilot checklist before claiming N8N «covered» as runtime. → **STORY-36** |
| **P0-Q2** | `tests/integration/test_product_journey_scenarios.py` module docstring + UC tests | Doc: «no live Telegram/Railway». Harness: Recording OpenAI + Gateway; several UC use `dry_run_gateway=True`. Matrix UC rows marked `covered` after pytest green. | Critical path «resident Telegram → aibridge → gateway publish» **untested end-to-end**; green UC ≠ Gate-5. | **closed-with-defer (STORY-37 P3/P6):** UC = PG-journey only; Gate-5 owned by evidence index `deferred` + checklist out-of-CI; do not invent live PASS. |
| **P0-Q3** | `tests/test_qa_gates_layers_dod.py`::`test_gate5_live_deferred_out_of_default_ci` | Asserts `gate5["status"] == "deferred_live"` and `LAYER_DIRS["F_live"] is None` — **passing means defer is recorded**, not that live channel works. | NO_UNTESTED_CRITICAL_PATHS: live TG/Railway remain open while Gate-5 row can look «handled». | **closed-with-defer (STORY-37):** keep `deferred_live` until accepted pack; residual live proof = operator pilot (WAIVED invent). |

### P1 — CORRECT_LOGIC

| ID | Location | Evidence | Risk | Recommendation |
|----|----------|----------|------|----------------|
| **P1-Q1** | `tests/contract/test_json_schema_boundary.py`::`test_val_characterization_capture_first` | Was: `assert 100 <= status < 600` then `== 200`. | Broad band tautology risk. | **closed (STORY-40 P3):** band removed; VAL-014/018 keep explicit `== 200`. |
| **P1-Q2** | `tests/integration/test_openai_prompt_behavior.py`::`test_oai_008_*` / `test_oai_009_*` | Transport asserts `RATE_LIMITED` / `TRANSIENT_FAILURE`; channel maps Option A → 429 `rate_limited` / 503 `transient_failure` (STORY-38). | Was: green locked 500 characterization. | **closed (STORY-38 P3):** decision fixture Option A + product handler + channel expects. |
| **P1-Q3** | `tests/test_qa_gates_layers_dod.py`::`test_char_capture_first_bound_refs_or_defer` (esp. CHAR-008) + `tests/test_char008_send_edit_capture_honesty.py` | Meta-gate: refs/bound_tests + optional `defer_reason`. Honesty suite: deferred envelope XOR filled capture (export ABSENT → visible defer). | Residual: Send vs Edit / retry dedupe unanswered until export capture (G-01 WAIVED invent). | **closed-with-defer (STORY-39 P3/P6):** ownership + honesty bind Done; capture answer remains deferred until credential-stripped export. |
| **P1-Q4** | Promote `*_hash_eq*` across modules (e.g. `test_seed_originals_intact_hash_eq`, `test_uc_fixture_packs_promoted_hash_eq`) | Assert SHA256(package)==SHA256(tests copy) and matrix_id membership. | Alone does not validate runtime; OK as **integrity**, dangerous if counted as behavioral coverage. | **closed (STORY-40 P3):** INDEX + gaps §40 DoD — integrity-only; never sole matrix Expected. |

### P2 — MINIMAL_MOCK_OVERUSE

| ID | Location | Evidence | Risk | Recommendation |
|----|----------|----------|------|----------------|
| **P2-Q1** | Entire `tests/n8n/` | Fixture-only + local Python simulation (`simulate_post_ack_failure_timeline`) | Over-mock relative to «n8n layer» name | Rename/docs: adapter-contract tests; workflow smoke elsewhere → **STORY-36** |
| **P2-Q2** | GW / IDEM / SEC / OAI integration helpers | Default `DATABASE_URL="memory"` + `RecordingGatewayTransport` / Recording OpenAI | Strong isolation; weak against real PG concurrency / real HTTPS gateway | **closed-with-waive (STORY-40 P3):** QUAL-003 WAIVE — UC+LIFE-live cover PG; Recording GW sufficient; optional non-Recording probe not Gate-5. |
| **P2-Q3** | UC harness | Recording doubles + disposable PG | Correct for default CI; still mock-heavy vs pilot | **closed-with-defer (STORY-37):** accept for CI; Gate-5 remains out-of-CI / deferred evidence |

### Explicit «none» checks

| Check | Result |
|-------|--------|
| Sole `assert True` / empty `pass` bodies in suite | **none found** |
| hash_eq-only as **only** test for a story | Not sole for any story 23–35 (behavioral tests coexist) |
| Skip used to hide fail (authoritative PG run) | **none** — 0 skipped |

---

## 4. Cross-walk to pytest facts

| Fact | Qualification note |
|------|-------------------|
| 244 passed with disposable PG | Proves UC + LIFE-live **execute** under PG; does **not** clear P0-Q1/Q2/Q3 |
| Prior 12 skips without PG | Environment gap, not false success — skip reasons honest |
| Gate-5 deferred_live still green | By design; P0-Q3 **closed-with-defer** (STORY-37) — live pack still absent |
| Fixture index 225/225 present | Integrity OK; not behavioral qualification |

---

## 5. Method statement (required)

Qualification **does not** declare «all OK». Findings above: **P0 ×3**, **P1 ×4**, **P2 ×3**. Empty subclasses would be stated as «none found» with method — here subclasses are non-empty.

**Not done in qualification wave:** changing asserts, inventing live Gate-5, fixing OAI 500 channel mapping, executing real n8n.

**Closure owners:** Scaffolded stories **36–40** in this package ([`INDEX.md`](./INDEX.md)).

---

## 6. Suggested next waves (operator only)

1. STORY-39 **closed-with-defer** (P3/P6) — CHAR-008 honesty + visible export-absent defer; optional later: place export → fill capture (no invent).  
2. Optional operator: Gate-5 **live pilot** capture when env available (STORY-37 residual G-01 WAIVED — do not invent TG/Railway SUCCESS).  
3. STORY-40 **closed** (P3) — QUAL-001/002 covered · QUAL-003 WAIVED (gaps §40).  
4. STORY-36 / STORY-37 / STORY-38 / STORY-39 / STORY-40 core waves executed.
