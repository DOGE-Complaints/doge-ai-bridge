# Task: implement — outcome map + unknown_outcome no auto-retry

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-05-gateway-outcomes.md`  
**P3 Done:** 2026-09-12T21:54:48Z
**Parent story:** [`STORY-AIBRIDGE-05-gateway-outcomes.md`](../STORY-AIBRIDGE-05-gateway-outcomes.md)

## Purpose

Map gateway results to outcomes incl. `unknown_outcome`, `contract_mismatch`, `blocked_by_confirmation`; ambiguous delivery → `unknown_outcome`; **no** automatic Send retry for the same revision; operator path links to unknown-outcome runbook (AC #4 / Scope #3,#5,#6).

**Out of this task:** inventing gateway reconciliation/lookup API; SPA E2E.

## Code Facts (verified exists)

1. Outcome rules — REQ-01 §15 AIB-HTTP-04/05; arch §5 `unknown_outcome` rules.
2. Runbook — `docs/runbooks/unknown-outcome-reconciliation.md`.
3. FSM — `SessionState.UNKNOWN_OUTCOME` + `MARK_UNKNOWN_OUTCOME` in `confirm_fsm.py`.

## AC/DoD

- [x] Outcome mapping covers required labels (at least unknown / contract_mismatch / blocked_by_confirmation as applicable).
- [x] After `unknown_outcome`, auto Send for same revision is blocked.
- [x] Operator-facing path references unknown-outcome runbook (reply text, metric note, or docs pointer in code path).
- [x] `Skill declared: python-pro` present.

## Where to change

- Outcome mapper; confirm FSM transitions; Send path retry guard.
- Channel/reply copy as needed.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# unknown_outcome → second auto Send same revision blocked
```
