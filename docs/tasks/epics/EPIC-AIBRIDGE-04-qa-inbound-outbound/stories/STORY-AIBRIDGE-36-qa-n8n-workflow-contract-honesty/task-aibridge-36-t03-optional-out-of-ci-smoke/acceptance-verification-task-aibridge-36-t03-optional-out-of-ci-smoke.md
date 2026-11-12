# Acceptance verification — task-aibridge-36-t03-optional-out-of-ci-smoke

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-18T12:32:14Z |
| **Story** | STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty |
| **Pkg** | pkg-000035 |
| **Wave** | P3 Execute |

## AC check

- [x] Checklist named/bound for pinned-export smoke outside default CI.
- [x] Explicit: not part of default pytest gate.
- [x] No live TG / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Evidence

```text
docs/ops/n8n-channel-workflow/r3-p1-09-live-gate-checklist.md
  § N8N-WF-001 pinned export smoke (out of CI)
  anchor #n8n-wf-001-pinned-export-smoke-out-of-ci
pin pointer payload.default_ci=false
payload.out_of_ci_smoke_checklist → r3-p1-09 …#n8n-wf-001-pinned-export-smoke-out-of-ci
WAIVE live TG / Railway invent
```
