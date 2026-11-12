# Task: AC-10-09 accept refuse mock without allow

**Status:** Done · P3 2026-10-16T11:23:50Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md`  
**Parent story:** [`STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md`](../STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md)  
**P1 scaffold:** 2026-10-16T11:18:56Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_53_scaffold_20261016T111732Z.plan.md)  
**Maps:** AC-10-09 accept

## Purpose

Refuse mock on accept before compute (defense in depth).

## AC/DoD

- [x] Gate from Purpose satisfied on disk at P3.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved — mock-without-allow reason string Open until implement (no invent SSOT).
- [x] Siblings 54–55 / channel registry / live OpenAI not claimed.
- [x] No product invent beyond this task DoD.

## Where to change (P3)

- src/aibridge/app.py accept · middleware/gates

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-53-t05-ac-10-09-accept-refuse-mock-without-allow.md`](./acceptance-verification-task-aibridge-53-t05-ac-10-09-accept-refuse-mock-without-allow.md)
