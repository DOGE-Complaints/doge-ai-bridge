# Task: ops — pilot preflight /readyz checklist (§15)

**Status:** Done · P3 2026-09-24T12:11:06Z  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-45-compat-live-telegram-verify.md`  
**Parent story:** [`STORY-AIBRIDGE-45-compat-live-telegram-verify.md`](../STORY-AIBRIDGE-45-compat-live-telegram-verify.md)  
**P1 scaffold:** 2026-09-24T12:07:46Z  
**P3 closed:** 2026-09-24T12:11:06Z  
**Maps:** REQ-07 §15 · TECH-ARCH §5.2 · AC-09 preflight

## Purpose

Pilot preflight checklist before any live turn: deployed image SHA includes STORY-41–44; deployed `/readyz` ready (§15.1); pilot runbook available. **Do not invent** Railway /readyz SUCCESS — record only observed facts or defer.

## AC/DoD

- [x] Checklist items documented (deploy SHA / image with 41–44; `/readyz` ready when env present; runbook pointer).
- [x] Claims from ops facts only — no invent Railway SUCCESS.
- [x] If no pilot env: hand off to t03 defer path (do not fake PASS).
- [x] `Skill declared: test-master` present.

## Where changed

- `docs/ops/req-07-ac09-pilot-preflight-checklist-20260924.md`

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-45-t01-pilot-preflight-readyz-checklist.md`](./acceptance-verification-task-aibridge-45-t01-pilot-preflight-readyz-checklist.md)
