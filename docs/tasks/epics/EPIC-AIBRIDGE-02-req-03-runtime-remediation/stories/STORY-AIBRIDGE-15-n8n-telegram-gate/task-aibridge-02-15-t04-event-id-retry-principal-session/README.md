# Task: docs/tests — event_id retry + principal/session/token binding

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-15-n8n-telegram-gate.md`  
**Parent story:** [`STORY-AIBRIDGE-15-n8n-telegram-gate.md`](../STORY-AIBRIDGE-15-n8n-telegram-gate.md)  
**P1 scaffold:** 2026-09-13T17:28:28Z
**P3 Done:** 2026-09-13T17:34:04Z  
**Maps:** Scope #5–#9 · Target #2 · R3-P1-09

## Purpose

Prove (docs + optional recorded/contract tests) that: `channel` is always `telegram`; `event_id` is deterministic from Telegram update/callback id and **unchanged** across n8n HTTP retries; `from.id`/`chat.id` map to principal; `session_id` stays stable for the active interview; `/actions` callback user/chat match token binding.

## Code Facts (verified exists — P1)

1. Mapping cheat-sheet: `event_id` ← update id; principal ← from.id / chat.id (`docs/ops/n8n-channel-workflow/README.md` §3).
2. REQ-03 §6.1 explicitly forbids minting a new `event_id` on HTTP Request retry.
3. Story 13 E2E covers façade principal/token binding with fakes — live n8n retry expression still needs gate evidence (`tests/test_story_13_*`).

## AC/DoD

- [x] Documented deterministic `event_id` derivation + retry invariance (Target #2).
- [x] Checklist/evidence for `channel=telegram`, principal mapping, stable `session_id`, token-binding match on `/actions`.
- [x] No invented OpenAPI fields.
- [x] `Skill declared: python-pro` present.

## Where to change

`docs/ops/n8n-channel-workflow/README.md` / §6.1 checklist; optional `tests/` helpers that assert façade binding (not live Telegram).

## Verification commands

```bash
rg -n "event_id|principal|session_id|retry" doge-ai-bridge/docs/ops/n8n-channel-workflow/README.md doge-ai-bridge/docs/requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "story_13 or channel or token" --maxfail=5
```
