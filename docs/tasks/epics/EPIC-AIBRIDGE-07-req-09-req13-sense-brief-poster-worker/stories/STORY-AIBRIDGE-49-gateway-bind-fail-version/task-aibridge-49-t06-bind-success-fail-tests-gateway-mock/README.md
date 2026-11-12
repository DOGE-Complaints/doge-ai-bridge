# Task: bind success/fail tests vs gateway mock

**Status:** Done · P3 2026-10-14T14:13:53Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-49-gateway-bind-fail-version.md`  
**Parent story:** [`STORY-AIBRIDGE-49-gateway-bind-fail-version.md`](../STORY-AIBRIDGE-49-gateway-bind-fail-version.md)  
**P1 scaffold:** 2026-10-14T14:08:54Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_49_scaffold_20261014T140705Z.plan.md)  
**Maps:** T06 fixtures

## Purpose

Isolation tests: success shape; fail class; mock reject → bind_rejected. No live gateway.

## AC/DoD

- [x] Gate from Purpose satisfied on disk at P3.
- [ ] `Skill declared: python-pro` present.
- [ ] Open markers preserved — do **not** invent bind path/JSON keys/DP9 wire SSOT.
- [ ] Sibling 57 apply / SPA / STORY-50 harness not claimed.
- [ ] No live gateway required as Done gate.

## Where to change (P3)

- tests/ near bind client.

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-49-t06-bind-success-fail-tests-gateway-mock.md` (create at P3 close)
