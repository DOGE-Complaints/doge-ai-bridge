# Task: dedicated prompt module packaging (DP7)

**Status:** Done · 2026-10-14T13:14:47Z
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-47-sense-brief-prompts-policy.md`  
**Parent story:** [`STORY-AIBRIDGE-47-sense-brief-prompts-policy.md`](../STORY-AIBRIDGE-47-sense-brief-prompts-policy.md)  
**P1 scaffold:** 2026-10-14T12:46:03Z · [p1 draft](../../../../../../../../.cursor/plans/p1_aibridge_47_scaffold_20261014T124254Z.plan.md)  
**Maps:** T02 · DP7

## Purpose

Separate EN system/instructions for sense-brief. **Must not** use Telegram interview / content-launch templates as civic SSOT. On-disk path — **Open**; module must ship with worker image.

## AC/DoD

- [x] Brief path loads worker prompts, not interview corpus templates.
- [x] EN instruction language for system/prompts.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved — do **not** invent prompt-path SSOT.
- [x] No external CMS / invent prompt body SSOT in story.

## Where to change (P3)

- Dedicated worker prompt package/files — path **Open**.


## Implement names (chosen P3; were Open)

| Kind | Value |
|------|-------|
| Module | `src/aibridge/sense_brief/` |
| Prompts | `src/aibridge/sense_brief/prompts/system_en.md` |
| Env text-brief | `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` |
| JSON L2 | `title`, `summary.{et,ru,en}`, `problem`, `context`, `severity`, `audience`, `desired_outcome`, `evidence_refs` |
| Fail classes | `corpus_insufficient`, `brief_generation_failed` |

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-47-t02-dedicated-prompt-module.md`](./acceptance-verification-task-aibridge-47-t02-dedicated-prompt-module.md)
