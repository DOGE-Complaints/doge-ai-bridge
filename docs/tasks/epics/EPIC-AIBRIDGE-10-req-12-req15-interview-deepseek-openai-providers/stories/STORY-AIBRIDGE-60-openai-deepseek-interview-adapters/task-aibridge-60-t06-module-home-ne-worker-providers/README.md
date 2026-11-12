# Task: module home ne worker providers

**Status:** Done · P3 2026-11-01T20:58:34Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-12-req15-interview-deepseek-openai-providers/STORY-AIBRIDGE-60-openai-deepseek-interview-adapters.md`  
**Parent story:** [`STORY-AIBRIDGE-60-openai-deepseek-interview-adapters.md`](../STORY-AIBRIDGE-60-openai-deepseek-interview-adapters.md)  
**P1 scaffold:** 2026-11-01T20:51:31Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_60_scaffold_20261101T204955Z.plan.md)  
**Maps:** AC-02 boundary · arch 02 §4

## Purpose

Module home ≠ src/aibridge/providers/; HTTP helper reuse OK without worker ids

## AC/DoD

- [x] Gate from Purpose satisfied on disk at P3.
- [x] `Skill declared: python-pro` present.
- [x] No silent OpenAI when provider=`deepseek`.
- [x] Interview adapter home ≠ `src/aibridge/providers/`.
- [x] Keep InterviewEngine (D3) — port supplies backend only.
- [x] OOS preserved: Merge worker registry.
- [x] No invent AC beyond story Target / tech table.
- [x] No product invent beyond this task DoD · OOS 59/61.

## Where changed (P3)

- interview_providers/ ≠ providers/ · tests t06

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-60-t06-module-home-ne-worker-providers.md`](./acceptance-verification-task-aibridge-60-t06-module-home-ne-worker-providers.md)
