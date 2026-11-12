# STORY-AIBRIDGE-61 — Interview provider stub + live evidence gates

## Meta
- **Key:** `STORY-AIBRIDGE-61-interview-provider-stub-live-evidence`
- **Status:** **Done** · **Product Done** · pkg-000064 · P8 `05609c2`/`d45d872`/`a8b064c` · live **Explicit Partial** residual · Nested table repaired
- **Parent Epic:** [`EPIC-AIBRIDGE-10-req-12-req15-interview-deepseek-openai-providers.md`](../../EPIC-AIBRIDGE-10-req-12-req15-interview-deepseek-openai-providers.md)
- **source:** `backlog-stories/req-12-req15-interview-deepseek-openai-providers/STORY-AIBRIDGE-61-interview-provider-stub-live-evidence.md`
- **decision_ref:** [`STORY-AIBRIDGE-61-interview-provider-stub-live-evidence.md`](../../../../backlog-stories/req-12-req15-interview-deepseek-openai-providers/STORY-AIBRIDGE-61-interview-provider-stub-live-evidence.md) · [`REQ-12`](../../../../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) · [`03-verify-evidence-coexistence.md`](../../../../architecture/req15-interview-providers/03-verify-evidence-coexistence.md)
- **Package:** [`req-12-req15-interview-deepseek-openai-providers/INDEX.md`](../../../../backlog-stories/req-12-req15-interview-deepseek-openai-providers/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000064-20261101-epic-aibridge-10-story-61-interview-provider-stub-live-evidence.yaml`
- **P1 materialize:** 2026-11-01T21:16:01Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_61_scaffold_20261101T211450Z.plan.md)
- **Depends:** STORY-AIBRIDGE-59 · soft 60 Done
- **OOS:** open ops window · invent live SUCCESS / Railway · adapter re-implement beyond cite

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Verify / evidence / coexistence | [`03-verify-evidence-coexistence.md`](../../../../architecture/req15-interview-providers/03-verify-evidence-coexistence.md) |
| Peer Done | STORY-59 · STORY-60 |
| Env template | [`.env.example`](../../../../../.env.example) §4b |

## Scope
- Stub/harness matrix citing 59/60 tests for AC-01/02/03/05.
- Live runbook per provider; Explicit Partial without ops window.
- INDEX honesty: stub ≠ full AC-04 Done.
- **No** invent live SUCCESS / Railway Pass.

## Вне scope
- Opening live windows / mandatory live this wave.
- Implementing adapters beyond citing harness (60 Done).
- Worker REQ-10 live matrix body; telegram transport; gateway redesign.

## Target / AC
- [x] AC-AIB-12-04 stub side: harness evidence both providers + fail-closed/orthogonality.
- [x] AC-AIB-12-04 live side: runbook per provider Present; **Explicit Partial** (ops window not open).
- [x] Package INDEX honesty note: stub ≠ full AC-04 Done.

## Nested tasks (pkg-000064)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-61-t01-stub-evidence-matrix-59-60-harness](./task-aibridge-61-t01-stub-evidence-matrix-59-60-harness/README.md) | AC-04 stub · arch 03 §1 | Done |
| t02 | [task-aibridge-61-t02-live-pass-runbook-per-provider-partial](./task-aibridge-61-t02-live-pass-runbook-per-provider-partial/README.md) | AC-04 live · arch 03 §1 | Done |
| t03 | [task-aibridge-61-t03-peer-cite-table-worker-req11-req13](./task-aibridge-61-t03-peer-cite-table-worker-req11-req13/README.md) | arch 03 §2 boundary honesty | Done |
| t04 | [task-aibridge-61-t04-package-index-honesty-stub-ne-ac04](./task-aibridge-61-t04-package-index-honesty-stub-ne-ac04/README.md) | process gate · INDEX honesty | Done |
| t08 | [task-aibridge-61-t08-story-gate-checklist](./task-aibridge-61-t08-story-gate-checklist/README.md) | package gate AC-04 | **PASS** |
| t09 | [task-aibridge-61-t09-audit-g02-pipeline-nested-table-repair](./task-aibridge-61-t09-audit-g02-pipeline-nested-table-repair/README.md) | P4 G-02 · Nested table hygiene | Done |
