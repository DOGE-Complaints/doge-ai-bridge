# Task: audit G-03 — OpenAI image adapter message

**Status:** Done · P6 2026-10-16T11:13:36Z  
**Skill declared:** `python-pro`  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-52-mock-providers-accept-pipe.md`  
**Parent story:** [`STORY-AIBRIDGE-52-mock-providers-accept-pipe.md`](../STORY-AIBRIDGE-52-mock-providers-accept-pipe.md)  
**P5 scaffold:** 2026-10-16T11:11:33Z · [p5 APPLIED](../../../../../../../../.cursor/plans/p5_aibridge_52_gap_20261016T111035Z.plan.md)  
**P6 close:** 2026-10-16T11:13:36Z · `run_mode=aibridge_52_audit_20261016`  
**Maps:** P4 G-03 · Info · `run_mode=aibridge_52_audit_20261016`

## Purpose

Align `OpenAIImagePosterProvider.generate_poster_bytes` `NotImplementedError` message: stop citing «not STORY-AIBRIDGE-51»; state deferred live image / not this story (post-accept-wire wording).

## AC/DoD

- [x] Message no longer references STORY-AIBRIDGE-51.
- [x] Semantics remain: live image-poster invoke deferred (not invent live image / not STORY-54 text).
- [x] No accept-pipe rewire · no allow-mock (53) · no live OpenAI text (54).
- [x] `Skill declared: python-pro` present.

## Where to change (P6)

- `doge-ai-bridge/src/aibridge/providers/adapters.py` — `OpenAIImagePosterProvider`

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-52-t09-audit-g03-openai-image-adapter-message.md`](./acceptance-verification-task-aibridge-52-t09-audit-g03-openai-image-adapter-message.md)
