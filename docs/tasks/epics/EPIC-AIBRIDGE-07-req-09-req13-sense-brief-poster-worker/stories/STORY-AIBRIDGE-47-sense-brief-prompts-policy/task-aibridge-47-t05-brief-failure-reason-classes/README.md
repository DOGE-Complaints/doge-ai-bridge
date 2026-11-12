# Task: brief failure reason classes

**Status:** Done · 2026-10-14T13:14:47Z
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-47-sense-brief-prompts-policy.md`  
**Parent story:** [`STORY-AIBRIDGE-47-sense-brief-prompts-policy.md`](../STORY-AIBRIDGE-47-sense-brief-prompts-policy.md)  
**P1 scaffold:** 2026-10-14T12:46:03Z · [p1 draft](../../../../../../../../.cursor/plans/p1_aibridge_47_scaffold_20261014T124254Z.plan.md)  
**Maps:** T05 · DP9

## Purpose

Map failures to logical classes `corpus_insufficient` / `brief_generation_failed` (arch DP9). Exact wire **strings** remain **Open**.

## AC/DoD

- [x] Insufficient corpus / generation abort surfaces explicit class (no fake brief).
- [x] Exact wire enum not frozen as SSOT.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved.
- [x] Full bind client (49) not claimed.

## Where to change (P3)

- Brief pipeline error surface — wire strings **Open**.


## Implement names (chosen P3; were Open)

| Kind | Value |
|------|-------|
| Module | `src/aibridge/sense_brief/` |
| Prompts | `src/aibridge/sense_brief/prompts/system_en.md` |
| Env text-brief | `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` |
| JSON L2 | `title`, `summary.{et,ru,en}`, `problem`, `context`, `severity`, `audience`, `desired_outcome`, `evidence_refs` |
| Fail classes | `corpus_insufficient`, `brief_generation_failed` |

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-47-t05-brief-failure-reason-classes.md`](./acceptance-verification-task-aibridge-47-t05-brief-failure-reason-classes.md)
