# Task: wire image poster port into accept

**Status:** Done · P3 2026-10-16T11:05:47Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-52-mock-providers-accept-pipe.md`  
**Parent story:** [`STORY-AIBRIDGE-52-mock-providers-accept-pipe.md`](../STORY-AIBRIDGE-52-mock-providers-accept-pipe.md)  
**P1 scaffold:** 2026-10-16T11:03:46Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_52_scaffold_20261016T110222Z.plan.md)  
**P3 close:** 2026-10-16T11:05:47Z · tests **54 passed** (52+46–51)  
**Maps:** Scope wire image

## Purpose

Resolve image port → bytes → Present upload via poster_bytes= on upload_poster_https.

## AC/DoD

- [x] Gate from Purpose satisfied on disk at P3.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved — upload seam implemented as `poster_bytes=` (no invent SSOT).
- [x] Siblings 53–55 / allow-mock / live OpenAI / channel registry not claimed.
- [x] No product invent beyond this task DoD.

## Where to change (P3)

- src/aibridge/app.py · poster/pipeline.py · providers/

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-52-t02-wire-image-poster-port-into-accept.md`](./acceptance-verification-task-aibridge-52-t02-wire-image-poster-port-into-accept.md)
