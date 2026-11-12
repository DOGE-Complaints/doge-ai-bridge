# Task: AC-09-05 prompt isolation invent-refusal

**Status:** Done · P3 2026-10-14T14:40:44Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-50-worker-isolation-harness.md`  
**Parent story:** [`STORY-AIBRIDGE-50-worker-isolation-harness.md`](../STORY-AIBRIDGE-50-worker-isolation-harness.md)  
**P1 scaffold:** 2026-10-14T14:33:55Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_50_scaffold_20261014T143127Z.plan.md)  
**Maps:** T06 · AC-09-05

## Purpose

Assert EN instruction / dedicated prompt path isolation; invent-refusal fixture.

## AC/DoD

- [x] Gate from Purpose satisfied on disk at P3.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved — do **not** invent harness module names / production path SSOT beyond implement choice.
- [x] Live vendor secrets not required as Done gate.

## Where to change (P3)

- `tests/harness/sense_brief_isolation.py` · `tests/test_worker_isolation_harness_story_50.py`

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-50-t06-ac-09-05-prompt-isolation-invent-refusal.md`
