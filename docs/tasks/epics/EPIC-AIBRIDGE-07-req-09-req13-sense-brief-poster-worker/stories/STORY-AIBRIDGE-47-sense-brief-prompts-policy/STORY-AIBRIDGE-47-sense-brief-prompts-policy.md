# STORY-AIBRIDGE-47 — Sense brief + dedicated prompts + policy

## Meta
- **Key:** `STORY-AIBRIDGE-47-sense-brief-prompts-policy`
- **Status:** P6 Done · t08 Done · pkg-000050 · next **P7** · `run_mode=aibridge_47_audit_20261014` · 2026-10-14T13:31:42Z
- **Parent Epic:** [`EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker.md`](../../EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker.md)
- **source:** `backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-47-sense-brief-prompts-policy.md`
- **decision_ref:** [`STORY-AIBRIDGE-47-….md`](../../../../backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-47-sense-brief-prompts-policy.md) · [`REQ-09`](../../../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) §§1.1,2,4.2,5 AC-02/05,8.3 · [`02-brief-poster-pipeline.md`](../../../../architecture/sense-brief-poster-worker/02-brief-poster-pipeline.md)
- **Package:** [`req-09-req13-sense-brief-poster-worker/INDEX.md`](../../../../backlog-stories/req-09-req13-sense-brief-poster-worker/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000050-20261014-epic-aibridge-07-story-47-sense-brief-prompts-policy.yaml`
- **P1 materialize:** 2026-10-14T12:46:03Z · [p1 draft](../../../../../../.cursor/plans/p1_aibridge_47_scaffold_20261014T124254Z.plan.md)
- **Gate:** [t07](./task-aibridge-47-t07-story-gate/README.md) · **PASS** · [p3](../../../../run-reports/run-summary-20261014-1314-story-aibridge-47-p3.md)
- **Depends:** STORY-AIBRIDGE-46

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-09 | [`REQ-09`](../../../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) |
| Brief / prompts / slots | [`02-brief-poster-pipeline.md`](../../../../architecture/sense-brief-poster-worker/02-brief-poster-pipeline.md) |
| Overview DP4/DP6/DP7 | [`00-overview.md`](../../../../architecture/sense-brief-poster-worker/00-overview.md) |
| Worker accept (46) | [`worker_accept.py`](../../../../../../src/aibridge/worker_accept.py) · `POST /v1/worker/sense-brief/accept` |

## Scope
- Corpus → structured sense brief (logical L2): title ≤80; summary et/ru/en; problem/context/severity/audience/desired_outcome/evidence_refs (exact JSON keys Open).
- Dedicated worker prompt module (EN instructions); not interview/content templates as SSOT.
- text-brief capability slot; model id via env (no model catalog SSOT).
- Refuse inventing civic facts beyond corpus (AC-09-05 / L11).
- PII-safe logging hooks for job/Issue (bodies/secrets out).

## Вне scope
- Poster image / storage (48); bind-in (49); harness suite (50).
- Public raw brief blob on gateway (gateway DP4).
- Inventing final model IDs / JSON key spellings as SSOT.
- Wiring through `InterviewEngine` channel turns as entry.

## Context
Worker accept Present (46). Issue sense-brief pipeline Present (47): `src/aibridge/sense_brief/`. Interview/content prompts Present — not civic SSOT.

## Target / AC
- [x] AC-09-02: Successful brief has title ≤80 and summary et/ru/en.
- [x] AC-09-05: EN instruction language; no invented addresses/agencies beyond corpus.
- [x] Prompts live in dedicated worker module (not interview templates).
- [x] text-brief slot fail-closed if unset when worker enabled.
- [x] Nested tasks Done at execute

**Implement names (P3):** `src/aibridge/sense_brief/` · `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` · L2 JSON keys above · fail classes `corpus_insufficient` / `brief_generation_failed`.

## Nested tasks (pkg-000050)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-47-t01-logical-l2-brief-model](./task-aibridge-47-t01-logical-l2-brief-model/README.md) | T01 · AC-09-02 | Done |
| t02 | [task-aibridge-47-t02-dedicated-prompt-module](./task-aibridge-47-t02-dedicated-prompt-module/README.md) | T02 · DP7 | Done |
| t03 | [task-aibridge-47-t03-text-brief-capability-slot](./task-aibridge-47-t03-text-brief-capability-slot/README.md) | T03 · DP6 | Done |
| t04 | [task-aibridge-47-t04-corpus-brief-no-invent-policy](./task-aibridge-47-t04-corpus-brief-no-invent-policy/README.md) | T04 · AC-09-05 | Done |
| t05 | [task-aibridge-47-t05-brief-failure-reason-classes](./task-aibridge-47-t05-brief-failure-reason-classes/README.md) | T05 · DP9 | Done |
| t06 | [task-aibridge-47-t06-golden-l2-invent-refusal-fixtures](./task-aibridge-47-t06-golden-l2-invent-refusal-fixtures/README.md) | T06 fixtures | Done |
| t07 | [task-aibridge-47-t07-story-gate](./task-aibridge-47-t07-story-gate/README.md) | story AC gate | PASS |
| t08 | [task-aibridge-47-t08-audit-g01-sync-code-points](./task-aibridge-47-t08-audit-g01-sync-code-points/README.md) | P4 G-01 | Done |
