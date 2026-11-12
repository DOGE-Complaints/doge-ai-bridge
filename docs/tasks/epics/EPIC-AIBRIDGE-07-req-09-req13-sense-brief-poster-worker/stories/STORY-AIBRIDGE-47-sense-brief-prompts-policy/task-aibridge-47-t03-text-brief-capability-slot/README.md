# Task: text-brief capability slot (DP6)

**Status:** Done · 2026-10-14T13:14:47Z
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-47-sense-brief-prompts-policy.md`  
**Parent story:** [`STORY-AIBRIDGE-47-sense-brief-prompts-policy.md`](../STORY-AIBRIDGE-47-sense-brief-prompts-policy.md)  
**P1 scaffold:** 2026-10-14T12:46:03Z · [p1 draft](../../../../../../../../.cursor/plans/p1_aibridge_47_scaffold_20261014T124254Z.plan.md)  
**Maps:** T03 · DP6 fail-closed

## Purpose

Bind text-brief model/vendor id via env/config only (no model catalog SSOT). Worker enabled ⇒ text-brief configured or **fail-closed**.

## AC/DoD

- [x] Missing text-brief id when worker enabled → fail-closed before inventing brief.
- [x] No concrete OpenAI model string locked as SSOT.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved — do **not** invent env name SSOT.
- [x] Multi-provider abstraction v1 not claimed.

## Where to change (P3)

- Near `src/aibridge/config.py` / readiness — env **name** Open.


## Implement names (chosen P3; were Open)

| Kind | Value |
|------|-------|
| Module | `src/aibridge/sense_brief/` |
| Prompts | `src/aibridge/sense_brief/prompts/system_en.md` |
| Env text-brief | `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` |
| JSON L2 | `title`, `summary.{et,ru,en}`, `problem`, `context`, `severity`, `audience`, `desired_outcome`, `evidence_refs` |
| Fail classes | `corpus_insufficient`, `brief_generation_failed` |

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-47-t03-text-brief-capability-slot.md`](./acceptance-verification-task-aibridge-47-t03-text-brief-capability-slot.md)
