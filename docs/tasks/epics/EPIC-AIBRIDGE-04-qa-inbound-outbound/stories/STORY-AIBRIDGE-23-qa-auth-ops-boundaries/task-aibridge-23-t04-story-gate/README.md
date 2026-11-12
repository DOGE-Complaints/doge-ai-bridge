# Task: story gate — AUTH-* coverage + originals intact

**Status:** Done  
**P3 closed:** 2026-09-17T14:02:23Z  
**Gate:** [acceptance-verification-task-aibridge-23-t04-story-gate.md](../acceptance-verification-task-aibridge-23-t04-story-gate.md) PASS  

**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md`  
**Parent story:** [`STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md`](../STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md)  
**P1 scaffold:** 2026-09-17T13:59:06Z  
**Maps:** Story Acceptance criteria · TRACEABILITY AUTH-*

## Purpose

Story acceptance gate: all AUTH-001…012 covered by fixtures+tests; TRACEABILITY story key; no Bearer leakage asserts; package `fixtures/` originals intact. Write acceptance-verification after live verify in P3.

**Out of this task:** invent characterization as product invent; Railway SUCCESS invent.

## Code Facts (verified exists — P1)

1. AC from `$storyFile` Acceptance criteria (5 checkboxes).
2. TRACEABILITY-MATRIX AUTH-001…012 → `STORY-AIBRIDGE-23-qa-auth-ops-boundaries`.
3. Gate Date: only after live verify in P3 session.

## AC/DoD

- [x] Every AUTH-* matrix ID evidenced (tests + fixtures copies).
- [x] Package originals still under package `fixtures/`.
- [x] Acceptance verification artifact PASS with live Date.
- [x] `Skill declared: test-master` present.

## Where to change

- This folder / story: `acceptance-verification-task-aibridge-23-t04-story-gate.md` (P3)
- Pipeline / backlog AC checkboxes (P3)

## Verification commands

```bash
ls doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/turns-valid-private.json
cd doge-ai-bridge && DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
  .venv/bin/pytest tests/contract/ -q --noconftest 2>/dev/null || true
```
