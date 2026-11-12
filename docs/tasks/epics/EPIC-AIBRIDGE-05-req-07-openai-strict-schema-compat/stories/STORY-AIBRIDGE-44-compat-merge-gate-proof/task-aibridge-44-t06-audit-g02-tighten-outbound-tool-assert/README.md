# Task: fix — tighten outbound tool mutation assert (G-02)

**Status:** Done · P6 2026-09-24T12:01:55Z  
**Skill declared:** test-master  
**Wave:** `run_mode=aibridge_44_audit_20260924`  
**Gap:** G-02 (Low) — P4 audit 2026-09-24 → **CLOSED**  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-44-compat-merge-gate-proof-20260924.md`  
**Parent story:** [`STORY-AIBRIDGE-44-compat-merge-gate-proof.md`](../STORY-AIBRIDGE-44-compat-merge-gate-proof.md)  
**P5 scaffold:** 2026-09-24T12:00:00Z  
**P6 closed:** 2026-09-24T12:01:55Z  
**Maps:** G-02 · merge-gate §5.1 #1 · `test_req07_merge_gate.py`

## Purpose

Tighten `test_merge_gate_responses_tools_payload_no_uniqueitems`: replace soft OR with strict `assert tool == outbound`.

## AC/DoD

- [x] Soft OR removed; `assert tool == outbound`.
- [x] Merge-gate suite still green under filter.
- [x] No invent live TG / Railway.
- [x] `Skill declared: test-master` present.

## Where changed (P6)

- `tests/test_req07_merge_gate.py` — `test_merge_gate_responses_tools_payload_no_uniqueitems`
