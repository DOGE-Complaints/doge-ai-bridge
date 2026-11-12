# STORY-AIBRIDGE-50 — Contract + isolation harness (AC-09 proof)

## Meta
- **Key:** `STORY-AIBRIDGE-50-worker-isolation-harness`
- **Status:** P6 Done · t09 Done · WAIVED G-02/G-03 · pkg-000053 · next **P7** · 2026-10-14T14:53:46Z
- **Parent Epic:** [`EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker.md`](../../EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker.md)
- **source:** `backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-50-worker-isolation-harness.md`
- **decision_ref:** [`STORY-AIBRIDGE-50-….md`](../../../../backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-50-worker-isolation-harness.md) · [`REQ-09`](../../../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) · [`03-storage-bind-verify.md`](../../../../architecture/sense-brief-poster-worker/03-storage-bind-verify.md)
- **Package:** [`req-09-req13-sense-brief-poster-worker/INDEX.md`](../../../../backlog-stories/req-09-req13-sense-brief-poster-worker/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000053-20261014-epic-aibridge-07-story-50-worker-isolation-harness.yaml`
- **P1 materialize:** 2026-10-14T14:33:55Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_50_scaffold_20261014T143127Z.plan.md)
- **P3 Execute:** 2026-10-14T14:40:44Z · [p3](../../../../run-reports/run-summary-20261014-1440-story-aibridge-50-p3.md)
- **P4 Audit:** 2026-10-14T14:45:44Z · [p4](../../../../analysis/p4-audit-STORY-AIBRIDGE-50-worker-isolation-harness-20261014.md)
- **P5 APPLY:** 2026-10-14T14:50:21Z · [p5](../../../../run-reports/run-summary-20261014-1450-story-aibridge-50-p5-disposition.md)
- **P6 Execute:** 2026-10-14T14:53:46Z · [p6](../../../../run-reports/run-summary-20261014-1453-story-aibridge-50-p6.md)
- **Gate:** [t08](./task-aibridge-50-t08-package-gate-checklist/README.md) · **PASS**
- **Depends:** STORY-AIBRIDGE-46 · 47 · 48 · 49

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Isolation harness / DP8 | [`03-storage-bind-verify.md`](../../../../architecture/sense-brief-poster-worker/03-storage-bind-verify.md) |
| Implement | `tests/harness/sense_brief_isolation.py` · `tests/test_worker_isolation_harness_story_50.py` |

## Scope
- Automated isolation harness (mocks OK): AC-09-01…06.
- Live LLM/image/bucket smoke = optional ops residual — not merge gate.

## Вне scope
- Live OpenAI/bucket secrets in CI; SPA E2E; invent production path SSOT.

## Context
46–49 Present. Isolation harness — **Present** (P3).

## Target / AC
- [x] Harness proves AC-09-01…06 per arch AC map (isolation).
- [x] No dependency on live vendor for package merge gate.
- [x] Nested tasks Done at execute

**Implement names (P3):** `tests/harness/sense_brief_isolation.py` · `tests/test_worker_isolation_harness_story_50.py` · `tests/__init__.py` · `pyproject.toml` pythonpath `.`

## Nested tasks (pkg-000053)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-50-t01-harness-skeleton-mocks](./task-aibridge-50-t01-harness-skeleton-mocks/README.md) | T01 · DP8 | **Done** |
| t02 | [task-aibridge-50-t02-ac-09-01-channel-bearer-reject](./task-aibridge-50-t02-ac-09-01-channel-bearer-reject/README.md) | T02 · AC-09-01 | **Done** |
| t03 | [task-aibridge-50-t03-ac-09-02-logical-l2-brief](./task-aibridge-50-t03-ac-09-02-logical-l2-brief/README.md) | T03 · AC-09-02 | **Done** |
| t04 | [task-aibridge-50-t04-ac-09-03-upload-https-mock](./task-aibridge-50-t04-ac-09-03-upload-https-mock/README.md) | T04 · AC-09-03 | **Done** |
| t05 | [task-aibridge-50-t05-ac-09-04-fail-bind-reason-class](./task-aibridge-50-t05-ac-09-04-fail-bind-reason-class/README.md) | T05 · AC-09-04 | **Done** |
| t06 | [task-aibridge-50-t06-ac-09-05-prompt-isolation-invent-refusal](./task-aibridge-50-t06-ac-09-05-prompt-isolation-invent-refusal/README.md) | T06 · AC-09-05 | **Done** |
| t07 | [task-aibridge-50-t07-ac-09-06-idempotent-and-version-bump](./task-aibridge-50-t07-ac-09-06-idempotent-and-version-bump/README.md) | T07 · AC-09-06 | **Done** |
| t08 | [task-aibridge-50-t08-package-gate-checklist](./task-aibridge-50-t08-package-gate-checklist/README.md) | T08 · package gate | **PASS** |
| t09 | [task-aibridge-50-t09-audit-g01-sync-scope-open](./task-aibridge-50-t09-audit-g01-sync-scope-open/README.md) | P4 G-01 | **Done** |
