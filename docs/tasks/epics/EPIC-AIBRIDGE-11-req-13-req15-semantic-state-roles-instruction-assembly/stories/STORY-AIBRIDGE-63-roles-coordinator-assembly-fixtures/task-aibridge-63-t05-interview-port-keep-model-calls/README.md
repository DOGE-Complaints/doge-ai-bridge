# Task: Model calls via interview port Keep

**Status:** Done · P3 2026-11-02T09:16:58Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md`  
**Parent story:** [`STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md`](../STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md)  
**P1 scaffold:** 2026-11-02T09:05:07Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_63_scaffold_20261102T090322Z.plan.md) · pkg-000066  
**Maps:** t05 · STORY-63

## Purpose

Role/model invokes go through interview_providers Keep — not worker providers/.

## AC/DoD

- [x] Model path uses REQ-12 interview port Keep.
- [x] No merge into worker providers/.
- [x] Skill declared: python-pro present.

## Where changed (P3)

- `src/aibridge/roles/invoke.py · interview_providers Keep`

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-63-t05-interview-port-keep-model-calls.md`](./acceptance-verification-task-aibridge-63-t05-interview-port-keep-model-calls.md)
