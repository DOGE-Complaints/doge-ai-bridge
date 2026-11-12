# Task: test — SEC-010 tool_gen allowlist (G-02)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_32_audit_20260917`  
**Gap:** G-02 (Low) — P4 audit 2026-09-17  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-32-qa-privacy-logs-observability-20260917.md`  
**Parent story:** [`STORY-AIBRIDGE-32-qa-privacy-logs-observability.md`](../STORY-AIBRIDGE-32-qa-privacy-logs-observability.md)  
**P5 scaffold:** 2026-09-17T20:38:37Z  
**P6 closed:** 2026-09-17T20:42:29Z  
**Gate:** [acceptance-verification-task-aibridge-32-t06-audit-g02-sec010-tool-gen.md](./acceptance-verification-task-aibridge-32-t06-audit-g02-sec010-tool-gen.md) PASS  
**Maps:** SEC-010 · `tool_gen` · channel `forbid_narrative_substrings`

## Purpose

Strengthen SEC-010: drive allowlisted tool surface from `tool_gen` / generated strict tool (+ negative evil tool name/URL must not appear in OpenAI capture tools). Assert channel fixture `forbid_narrative_substrings` on audit/metrics. Prefer assert-only vs existing `tool_gen` seam — **no** silent product invent. **P6 only** — do not implement in P5. **No** live Telegram / Railway invent.

## AC/DoD

- [x] SEC-010 uses generated/`tool_gen` allowlisted tool (not only hand-injected single tool).
- [x] Evil URL/tool name absent from capture tools; channel forbid list asserted.
- [x] No live Telegram / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/integration/test_privacy_observability.py` — **P6 Done**
- `src/aibridge/tool_gen.py` (assert-only)
- channel fixture `sec-turns-pii-narrative.json`
