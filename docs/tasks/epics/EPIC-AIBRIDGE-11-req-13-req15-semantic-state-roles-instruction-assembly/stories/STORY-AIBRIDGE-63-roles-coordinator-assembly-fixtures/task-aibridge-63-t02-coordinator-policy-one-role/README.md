# Task: Coordinator policy table → one role

**Status:** Done · P3 2026-11-02T09:16:58Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md`  
**Parent story:** [`STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md`](../STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md)  
**P1 scaffold:** 2026-11-02T09:05:07Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_63_scaffold_20261102T090322Z.plan.md) · pkg-000066  
**Maps:** t02 · STORY-63

## Purpose

Policy table (phase/flags) selects exactly one next role; no LLM-router.

## AC/DoD

- [x] Coordinator picks one role from policy table.
- [x] No LLM-as-router / free meta-agent path.
- [x] Concrete rows Open at implement (thin).
- [x] Skill declared: python-pro present.

## Where changed (P3)

- `src/aibridge/roles/policy.py · coordinator re-export`

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-63-t02-coordinator-policy-one-role.md`](./acceptance-verification-task-aibridge-63-t02-coordinator-policy-one-role.md)
