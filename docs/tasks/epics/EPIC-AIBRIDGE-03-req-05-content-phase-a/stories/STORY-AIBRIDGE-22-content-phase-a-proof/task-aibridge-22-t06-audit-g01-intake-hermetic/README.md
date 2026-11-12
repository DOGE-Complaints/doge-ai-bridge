# Task: test — hermetic intake pin for Phase A proof (G-01)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_22_audit_g01_intake`  
**Gap:** G-01 (Medium) — P4 audit 2026-09-16  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-22-content-phase-a-proof-20260916.md`  
**Parent story:** [`STORY-AIBRIDGE-22-content-phase-a-proof.md`](../STORY-AIBRIDGE-22-content-phase-a-proof.md)  
**P5 scaffold:** 2026-09-16T13:47:10Z  
**P6 Done:** 2026-09-16T13:49:48Z  
**Gate:** [acceptance-verification-task-aibridge-22-t06-audit-g01-intake-hermetic.md](./acceptance-verification-task-aibridge-22-t06-audit-g01-intake-hermetic.md) PASS

## Purpose

In `tests/test_story_22_phase_a_proof.py` `_full_dump_settings`: replace dead `DOGESTONIA_API_BASE_URL` with `DOGESTONIA_INTAKE_BASE_URL=https://gateway.example.invalid`; prefer isolate ambient `.env` (`_env_file=None` / equivalent) so proof tests do not rely on local intake. Keep story-22 proof suite green.

**Out of this task:** invent Railway SUCCESS; rewrite `test_story_19_engine_wire.py` helper; change `config.py` aliases; fill smoke checklist `[ ]` boxes (G-02 WAIVED).

## Code Facts (verified exists — post P6)

1. Helper pins intake: `tests/test_story_22_phase_a_proof.py` · `DOGESTONIA_INTAKE_BASE_URL` · `Settings(_env_file=None, **base)`.
2. Intake SSOT: `src/aibridge/config.py` · `DOGESTONIA_INTAKE_BASE_URL`.
3. No dead `DOGESTONIA_API_BASE_URL` kwarg in story-22 helper.
4. pytest story-22: 6 passed @ 2026-09-16T13:49:48Z.

## AC/DoD

- [x] `_full_dump_settings` uses `DOGESTONIA_INTAKE_BASE_URL` (no dead `API_BASE` kwarg).
- [x] Ambient `.env` isolation for Settings construction where supported (`_env_file=None` or equivalent).
- [x] `tests/test_story_22_phase_a_proof.py` still passes (DATABASE_URL=memory + `--noconftest`).
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/tests/test_story_22_phase_a_proof.py` — **Done**

## Verification commands (P6)

```bash
rg -n 'DOGESTONIA_API_BASE_URL|DOGESTONIA_INTAKE_BASE_URL|_env_file' \
  doge-ai-bridge/tests/test_story_22_phase_a_proof.py
cd doge-ai-bridge && DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/test_story_22_phase_a_proof.py -q --noconftest
```
