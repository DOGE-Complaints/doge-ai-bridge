# Task: HTTP contracts + channel unchanged

**Status:** Done · P3 2026-10-16T11:05:47Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-52-mock-providers-accept-pipe.md`  
**Parent story:** [`STORY-AIBRIDGE-52-mock-providers-accept-pipe.md`](../STORY-AIBRIDGE-52-mock-providers-accept-pipe.md)  
**P1 scaffold:** 2026-10-16T11:03:46Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_52_scaffold_20261016T110222Z.plan.md)  
**P3 close:** 2026-10-16T11:05:47Z · tests **54 passed** (52+46–51)  
**Maps:** OOS guards

## Purpose

Accept/bind HTTP unchanged; channel registry untouched (L10-1).

## AC/DoD

- [x] Gate from Purpose satisfied on disk at P3.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved — upload seam implemented as `poster_bytes=` (no invent SSOT).
- [x] Siblings 53–55 / allow-mock / live OpenAI / channel registry not claimed.
- [x] No product invent beyond this task DoD.

## Where to change (P3)

- app.py accept/bind surfaces · channel paths

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-52-t07-http-contracts-channel-unchanged.md`](./acceptance-verification-task-aibridge-52-t07-http-contracts-channel-unchanged.md)
