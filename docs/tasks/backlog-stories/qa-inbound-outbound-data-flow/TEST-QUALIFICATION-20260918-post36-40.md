# Test qualification — QA suite post stories 36–40

**Date:** 2026-09-18 (post-36–40)  
**Package SSOT:** this file  
**Ops pointer:** [`../../../qa/inbound-outbound/test-qualification-20260918-post36-40.md`](../../../qa/inbound-outbound/test-qualification-20260918-post36-40.md)  
**Prior SSOT:** [`TEST-QUALIFICATION-20260918.md`](./TEST-QUALIFICATION-20260918.md)  
**Method:** [`.cursor/rules/test-qualification.mdc`](../../../../../.cursor/rules/test-qualification.mdc) + analysis.mdc  
**Pytest facts:** [`../../../qa/inbound-outbound/pytest-report-20260918-post36-40.md`](../../../qa/inbound-outbound/pytest-report-20260918-post36-40.md) — **263 passed / 0 skipped** (operator Terminal + disposable PG; honesty included)  
**This wave:** docs only — **no** test/product autofix

---

## 0. Prior findings — closure status (re-verified)

| ID | After 36–40 | Evidence (this review) |
|----|-------------|------------------------|
| **P0-Q1** | **deferred-honest** | `test_n8n_wf_001_pin_deferred_or_sha_bound`: status `deferred` + `defer_reason`; export absent; Layer E = `adapter-contract`. Runtime workflow still not executed. |
| **P2-Q1** | **closed-with-docs** | Pin payload `layer_e_label == adapter-contract`; suite still fixture helpers in `tests/n8n/`. |
| **P0-Q2** | **deferred-honest** | UC ≠ Gate-5 cross-links asserted in `test_gate5_checklist_and_uc_crosslinks`; UC skipped this run (no PG) — when PG up still Recording harness. |
| **P0-Q3** | **deferred-honest** | `test_gate5_program_still_deferred_live_in_default_ci` + evidence index `accepted_pack is False`. Green ≠ live Gate-5 PASS. |
| **P2-Q3** | **accepted** | CI mock-heavy UC documented; Gate-5 remains out-of-CI. |
| **P1-Q1** | **closed** | `test_val_characterization_capture_first`: no `100<=status<600`; explicit `== 200` for VAL-014/018. |
| **P1-Q2** | **closed** | OAI-008/009 channel Option A → 429 `rate_limited` / 503 `transient_failure` via expect fixtures + `char-006-decision` Option A. |
| **P1-Q3** | **deferred-honest** | `test_char008_capture_deferred_or_filled`: defer XOR non-empty capture; export absent → visible `defer_reason`. |
| **P1-Q4** | **closed** | INDEX / STORY-40 DoD: hash_eq integrity-only. |
| **P2-Q2** | **waived** | QUAL-003 WAIVE recorded (STORY-40). |

---

## 1. Inventory (suite + honesty)

| Module | Role |
|--------|------|
| contract / unit TOOL·ACT / n8n / integration / `test_qa_gates_layers_dod.py` | Stories 23–35 core |
| `tests/test_n8n_wf_001_pin_honesty.py` | STORY-36 N8N-WF-001 |
| `tests/test_gate5_evidence_honesty.py` | STORY-37 Gate-5 |
| `tests/test_char008_send_edit_capture_honesty.py` | STORY-39 CHAR-008 |
| OAI integration (+ char-006 fixtures) | STORY-38 |

**Antipattern grep (suite paths):** sole `assert True` / vacuous `100<=status<600` — **none found**.

---

## 2. Findings (post-36–40)

### P0 — NO_FALSE_SUCCESSES / VALIDATE_REAL_FUNCTIONALITY / NO_UNTESTED_CRITICAL_PATHS

| ID | Location | Evidence | Risk | Recommendation |
|----|----------|----------|------|----------------|
| **P0-R1** | Live paths still absent | Export `docs/ops/n8n-channel-workflow/exports/aibridge-telegram-channel-v1.json` **absent**; Gate-5 `accepted_pack` false; CHAR-008 capture deferred | Critical paths (live n8n / Gate-5 / Send-Edit capture) remain **unexecuted** — now **honestly deferred**, not silently «covered» | Operator: pin export → close N8N-WF-001 + CHAR-008; pilot evidence → Gate-5. Not a test greenwash. |
| **P0-R2** | UC / LIFE-live | Was 12 skips in agent; **operator Terminal: 263/0** — UC + LIFE-live **executed** | Cleared for this host | Re-confirm only if PG down again |

**False-success check on honesty modules:** pass conditions require `defer_reason` when deferred and forbid invent (e.g. export present while status deferred fails). **Not** NO_FALSE_SUCCESSES violations.

### P1 — CORRECT_LOGIC

| ID | Location | Evidence | Risk | Recommendation |
|----|----------|----------|------|----------------|
| **P1-R1** | `test_oai_010_timeout_internal_error_dedupe_abort` | Still asserts channel **500** `internal_error` for `TIMEOUT` | Option A closed 429/5xx; timeout path still 500 — may be intentional residual | Confirm vs CHAR-006 scope (RATE_LIMITED/TRANSIENT only) or extend Option A to timeout |
| **P1-R2** | Honesty modules (partial) | Mix of hash_eq promote + markdown string contains + fixture payload XOR | Docs-existence asserts alone would be weak; XOR defer/capture and anti-invent checks raise bar | Keep; do not count hash_eq-only as behavioral for matrix Expected |

### P2 — MINIMAL_MOCK_OVERUSE

| ID | Location | Evidence | Risk | Recommendation |
|----|----------|----------|------|----------------|
| **P2-R1** | [`TEST-MANUAL.md`](../../../qa/inbound-outbound/TEST-MANUAL.md) §4 | Honesty modules were omitted from default command at qualification time | Operators could miss STORY-36/37/39 | **closed in this docs wave:** honesty paths added to TEST-MANUAL §4 |
| **P2-R2** | Integration suite | Still memory + Recording outside UC/LIFE-live | Accepted / QUAL-003 waived | No change unless operator un-waives |

### Explicit «none» / cleared

| Check | Result |
|-------|--------|
| VAL tautology band | **cleared** (QUAL-001) |
| OAI-008/009 channel 500 forever-success | **cleared** (Option A) |
| Gate-5 green = live works | **cleared** (explicit deferred_live + evidence honesty) |
| Sole `assert True` bodies | **none found** |

---

## 3. Cross-walk to pytest facts

| Fact | Qualification note |
|------|-------------------|
| **263 passed / 0 skipped** (operator Terminal + disposable PG) | Authoritative suite green incl. UC + LIFE-live + honesty |
| Agent earlier 251/12 | Environment PG gap only |
| fixture-index 230/230 | Integrity OK |
| Prior 244 with PG | Pre-honesty baseline; delta +19 collected nodes |
| MATRIX-COVERAGE-VERIFICATION.md | **Statement** coverage only (186 IDs · 2026-09-17) — **not** proof of behavioral Expected for all rows; matrix now 190 rows with deferred/fixture/PG-journey classes |

---

## 4. Method statement

Qualification **does not** declare «all OK».  

- Prior P0/P1/P2: largely **closed**, **deferred-honest**, or **waived** (see §0).  
- New findings: **P0 ×2**, **P1 ×2**, **P2 ×2** (of which **P2-R1 closed** by TEST-MANUAL update in this docs wave; **P2-R2** remains waived QUAL-003).  
- Remaining product/ops work is **export pin + Gate-5 pilot**, not greenwash of defer.

**Not done this wave:** pytest/product fixes; inventing export JSON; live TG.

---

## 5. Suggested next operator actions

1. Terminal: `./scripts/start-disposable-pg.sh` → re-run same pytest command → confirm **263 passed / 0 skipped**.  
2. When ready: credential-stripped workflow export → flip N8N-WF-001 + CHAR-008 off deferred.  
3. Gate-5 pilot evidence pack → leave `deferred_live` only until pack accepted.
