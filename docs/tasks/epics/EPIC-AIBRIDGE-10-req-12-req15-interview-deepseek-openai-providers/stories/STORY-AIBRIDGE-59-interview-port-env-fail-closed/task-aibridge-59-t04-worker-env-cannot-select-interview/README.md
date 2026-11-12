# Task: worker env cannot select interview

**Status:** Done · P3 Execute 2026-11-01T20:34:18Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-12-req15-interview-deepseek-openai-providers/STORY-AIBRIDGE-59-interview-port-env-fail-closed.md`  
**Parent story:** [`STORY-AIBRIDGE-59-interview-port-env-fail-closed.md`](../STORY-AIBRIDGE-59-interview-port-env-fail-closed.md)  
**P1 scaffold:** 2026-11-01T20:23:26Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_59_scaffold_20261101T202103Z.plan.md)  
**Maps:** AC-AIB-12-02

## Purpose

Orthogonality: AIBRIDGE_WORKER_*_PROVIDER cannot select interview

## AC/DoD

- [x] Gate from Purpose satisfied on disk at P3.
- [x] `Skill declared: python-pro` present.
- [x] No silent OpenAI when unset; recording ≠ typed OK provider.
- [x] Interview port/registry home ≠ `src/aibridge/providers/`.
- [x] OOS preserved: Worker REQ-10 registry changes.
- [x] No invent AC beyond story Target / tech table.
- [x] No product invent beyond this task DoD · OOS 60/61.

## Where changed (P3)

- AC-12-02 · registry ignores AIBRIDGE_WORKER_*

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-59-t04-worker-env-cannot-select-interview.md`](./acceptance-verification-task-aibridge-59-t04-worker-env-cannot-select-interview.md)
