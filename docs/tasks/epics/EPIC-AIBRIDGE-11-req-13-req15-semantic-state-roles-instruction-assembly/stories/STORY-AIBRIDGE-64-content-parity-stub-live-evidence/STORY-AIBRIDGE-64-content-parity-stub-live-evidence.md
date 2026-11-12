# STORY-AIBRIDGE-64 — Content volume/parity + stub/live evidence

## Meta
- **Key:** `STORY-AIBRIDGE-64-content-parity-stub-live-evidence`
- **Status:** P3 Execute Done · pkg-000067 · gate **PASS** · AC-05 live **Explicit Partial** · next **P4** · 2026-11-02T10:32:29Z
- **Parent Epic:** [`EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly.md`](../../EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly.md)
- **source:** `backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-64-content-parity-stub-live-evidence.md`
- **decision_ref:** [`STORY-AIBRIDGE-64-….md`](../../../../backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-64-content-parity-stub-live-evidence.md) · [`REQ-13`](../../../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) · [`03-content-volume-parity-verify.md`](../../../../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md)
- **Package:** [`req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md`](../../../../backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000067-20261102-epic-aibridge-11-story-64-content-parity-stub-live-evidence.yaml`
- **P1 materialize:** 2026-11-02T10:28:38Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_64_scaffold_20261102T102522Z.plan.md)
- **Depends:** soft STORY-63 Done · peer GPT-48 for live AC-05 Pass
- **OOS:** GPT-48 authoring/export bodies · open ops window · invent inventory hash SSOT · invent live SUCCESS

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Volume / parity / verify | [`03-content-volume-parity-verify.md`](../../../../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md) |
| Etalon Explicit Partial | STORY-61 · [`08-ac04-interview-stub-live-evidence-gates.md`](../../../../runtime-docs/08-ac04-interview-stub-live-evidence-gates.md) |
| Soft peers | STORY-62 · STORY-63 Done |

## Scope
- Document prod Railway volume path (L13-2); baked `src/instructions/` = fixture/dev.
- Incomplete/mismatched content → fail-closed (AC-06) — broken fixture harness.
- Stub evidence matrix mapping 62/63 → AC-01/02/03/07/08 (+ AC-06 stub).
- Consume parity (AC-05): gate/docs Present; live = **Explicit Partial** without GPT-48 export+window.
- Honesty in package INDEX: stub ≠ live/parity Done.

## Вне scope
- Authoring GPT-48 bodies; opening live window / mandatory export this wave; invent inventory hash SSOT.

## Verified current state
- Content fail-closed patterns Present (`content.py` / readiness — cite at P3).
- GPT UI sync script: **not found** (T1).
- Arch D6 split gate locked.
- Soft 62/63 Product Done.

## Target / AC
- [x] AC-AIB-13-04: prod volume path documented.
- [x] AC-AIB-13-06: incomplete/mismatch → fail-closed (fixture).
- [x] AC-AIB-13-05 stub/docs: parity gate described; live = **Explicit Partial** (Q1).
- [x] Package INDEX honesty note.

## Nested tasks (pkg-000067)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-64-t01-stub-evidence-matrix-62-63-harness](./task-aibridge-64-t01-stub-evidence-matrix-62-63-harness/README.md) | stub matrix 62/63 | Done |
| t02 | [task-aibridge-64-t02-prod-volume-path-l13-2-docs](./task-aibridge-64-t02-prod-volume-path-l13-2-docs/README.md) | AC-04 · L13-2 | Done |
| t03 | [task-aibridge-64-t03-ac06-fail-closed-incomplete-fixture](./task-aibridge-64-t03-ac06-fail-closed-incomplete-fixture/README.md) | AC-06 | Done |
| t04 | [task-aibridge-64-t04-ac05-parity-gate-explicit-partial](./task-aibridge-64-t04-ac05-parity-gate-explicit-partial/README.md) | AC-05 Explicit Partial | Done |
| t05 | [task-aibridge-64-t05-package-index-honesty-stub-ne-ac05](./task-aibridge-64-t05-package-index-honesty-stub-ne-ac05/README.md) | INDEX honesty | Done |
| t08 | [task-aibridge-64-t08-story-gate-checklist](./task-aibridge-64-t08-story-gate-checklist/README.md) | package gate | PASS |

## Code points
- readiness/content gates · thin runtime-docs note (path at P3) · tests 62/63 cite
