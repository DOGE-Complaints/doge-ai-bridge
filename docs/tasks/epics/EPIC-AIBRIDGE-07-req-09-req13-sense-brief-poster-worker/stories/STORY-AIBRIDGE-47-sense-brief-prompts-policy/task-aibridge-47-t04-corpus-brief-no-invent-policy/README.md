# Task: corpus→brief pipeline + no-invent policy (AC-09-05)

**Status:** Done · 2026-10-14T13:14:47Z
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-47-sense-brief-prompts-policy.md`  
**Parent story:** [`STORY-AIBRIDGE-47-sense-brief-prompts-policy.md`](../STORY-AIBRIDGE-47-sense-brief-prompts-policy.md)  
**P1 scaffold:** 2026-10-14T12:46:03Z · [p1 draft](../../../../../../../../.cursor/plans/p1_aibridge_47_scaffold_20261014T124254Z.plan.md)  
**Maps:** T04 · AC-09-05

## Purpose

Generate structured brief from accept corpus; EN instruction language; i18n outputs allowed. Refuse inventing addresses/agencies/events beyond corpus. PII-safe logging: job/Issue ids OK; no citizen message bodies/secrets.

## AC/DoD

- [x] Fixture corpus with missing civic facts does not invent them.
- [x] Must not wire through `InterviewEngine` channel turns as entry.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved.
- [x] Poster bytes (48) / bind-in (49) not claimed.

## Where to change (P3)

- Worker brief pipeline module — path **Open**; hook from accept corpus.


## Implement names (chosen P3; were Open)

| Kind | Value |
|------|-------|
| Module | `src/aibridge/sense_brief/` |
| Prompts | `src/aibridge/sense_brief/prompts/system_en.md` |
| Env text-brief | `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` |
| JSON L2 | `title`, `summary.{et,ru,en}`, `problem`, `context`, `severity`, `audience`, `desired_outcome`, `evidence_refs` |
| Fail classes | `corpus_insufficient`, `brief_generation_failed` |

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-47-t04-corpus-brief-no-invent-policy.md`](./acceptance-verification-task-aibridge-47-t04-corpus-brief-no-invent-policy.md)
