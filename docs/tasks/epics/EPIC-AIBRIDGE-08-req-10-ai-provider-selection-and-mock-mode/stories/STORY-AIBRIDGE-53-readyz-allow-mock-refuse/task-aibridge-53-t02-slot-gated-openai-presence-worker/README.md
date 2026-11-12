# Task: slot-gated openai presence for worker

**Status:** Done · P3 2026-10-16T11:23:50Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md`  
**Parent story:** [`STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md`](../STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md)  
**P1 scaffold:** 2026-10-16T11:18:56Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_53_scaffold_20261016T111732Z.plan.md)  
**Maps:** L10-7 · arch §4

## Purpose

Worker mock+mock must not force OPENAI_API_KEY via worker gate; channel Present rules OOS.

## AC/DoD

- [x] Gate from Purpose satisfied on disk at P3.
- [x] `Skill declared: python-pro` present.
- [x] Open markers preserved — mock-without-allow reason string Open until implement (no invent SSOT).
- [x] Siblings 54–55 / channel registry / live OpenAI not claimed.
- [x] No product invent beyond this task DoD.

## Where to change (P3)

- src/aibridge/readiness.py · config.py openai_presence_ok / worker gate

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-53-t02-slot-gated-openai-presence-worker.md`](./acceptance-verification-task-aibridge-53-t02-slot-gated-openai-presence-worker.md)
