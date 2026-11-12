# Task: docs — backlog verified-state + store:false env hygiene (G-03)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_03_audit_20260912`  
**Gap:** G-03 (Info) — P4 audit 2026-09-12  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-03-responses-tool-budgets-20260912.md`  
**Parent story:** [`STORY-AIBRIDGE-03-responses-tool-budgets.md`](../STORY-AIBRIDGE-03-responses-tool-budgets.md)  
**P5 scaffold:** 2026-09-12T21:27:29Z  
**P6 Done:** 2026-09-12T21:30:01Z

## Purpose

(a) Sync backlog `$storyFile` §Verified current state to match P3 modules.  
(b) Reject `OPENAI_STORE_RESPONSES=true` at settings load (assemble always forces `store:false`).

**Out of this task:** Live OpenAI HTTP; Postgres history (07).

## Code Facts (verified exists — post P6)

1. Backlog Verified updated — `STORY-AIBRIDGE-03-responses-tool-budgets.md`.
2. `Settings._reject_store_true` + `responses_store_false_enforced` — `config.py`.
3. Tests — `tests/test_store_responses_env.py`.

## AC/DoD

- [x] Backlog story Verified section reflects modules + Recording client (live HTTP Absent).
- [x] `OPENAI_STORE_RESPONSES=true` rejected at settings load.
- [x] `Skill declared: python-pro` present.

## Where to change

- `docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-03-responses-tool-budgets.md`
- `src/aibridge/config.py`
- `tests/test_store_responses_env.py`

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_store_responses_env.py
```
