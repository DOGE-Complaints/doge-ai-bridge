# Task: golden L2 + invent-refusal fixtures

**Status:** Done · 2026-10-14T13:14:47Z
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-47-sense-brief-prompts-policy.md`  
**Parent story:** [`STORY-AIBRIDGE-47-sense-brief-prompts-policy.md`](../STORY-AIBRIDGE-47-sense-brief-prompts-policy.md)  
**P1 scaffold:** 2026-10-14T12:46:03Z · [p1 draft](../../../../../../../../.cursor/plans/p1_aibridge_47_scaffold_20261014T124254Z.plan.md)  
**Maps:** T06 · AC-09-02/05 fixtures

## Purpose

Golden/fixture brief for logical L2 shape; invent-refusal policy tests. Feeds STORY-50 harness checks for AC-09-02/05. No live vendor required in CI.

## AC/DoD

- [x] Fixtures prove title≤80, summary et/ru/en, no-invent behavior.
- [x] Live OpenAI not required in CI.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved.
- [x] Full STORY-50 harness suite not claimed Done here.

## Where to change (P3)

- `tests/` fixtures near worker brief modules.


## Implement names (chosen P3; were Open)

| Kind | Value |
|------|-------|
| Module | `src/aibridge/sense_brief/` |
| Prompts | `src/aibridge/sense_brief/prompts/system_en.md` |
| Env text-brief | `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` |
| JSON L2 | `title`, `summary.{et,ru,en}`, `problem`, `context`, `severity`, `audience`, `desired_outcome`, `evidence_refs` |
| Fail classes | `corpus_insufficient`, `brief_generation_failed` |

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-47-t06-golden-l2-invent-refusal-fixtures.md`](./acceptance-verification-task-aibridge-47-t06-golden-l2-invent-refusal-fixtures.md)
