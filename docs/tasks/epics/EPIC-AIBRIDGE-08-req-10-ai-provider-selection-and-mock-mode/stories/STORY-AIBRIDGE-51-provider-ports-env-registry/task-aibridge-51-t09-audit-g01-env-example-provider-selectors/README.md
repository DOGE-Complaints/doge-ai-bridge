# Task: audit G-01 — `.env.example` provider selectors

**Status:** Done · P6 2026-10-16T10:58:46Z  
**Skill declared:** `python-pro`  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-51-provider-ports-env-registry.md`  
**Parent story:** [`STORY-AIBRIDGE-51-provider-ports-env-registry.md`](../STORY-AIBRIDGE-51-provider-ports-env-registry.md)  
**P5 scaffold:** 2026-10-16T10:56:55Z · [p5 APPLIED](../../../../../../../../.cursor/plans/p5_aibridge_51_gap_20261016T105502Z.plan.md)  
**P6 close:** 2026-10-16T10:58:46Z · `run_mode=aibridge_51_audit_20261016`  
**Maps:** P4 G-01 · Low · `run_mode=aibridge_51_audit_20261016`

## Purpose

Document worker provider selectors in `doge-ai-bridge/.env.example` to match Present `config.py` fields (`AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER` / `AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER`); note unset → `mock`.

## AC/DoD

- [x] `.env.example` includes both provider selector knobs near model knobs.
- [x] Comment/note: unset/blank → `mock`; allowed values `mock`|`openai`.
- [x] No accept-pipe wire (52) · no allow-mock (53) · no live OpenAI invoke (54).
- [x] `Skill declared: python-pro` present.

## Where to change (P6)

- `doge-ai-bridge/.env.example` (near `AIBRIDGE_WORKER_*_MODEL`)
- Cite Present: `src/aibridge/config.py` provider fields

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-51-t09-audit-g01-env-example-provider-selectors.md`](./acceptance-verification-task-aibridge-51-t09-audit-g01-env-example-provider-selectors.md)
