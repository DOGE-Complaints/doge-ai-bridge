# Task: implement — ops-only session-delete fail-closed (no invent OAS)

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-16-privacy-retention.md`  
**Parent story:** [`STORY-AIBRIDGE-16-privacy-retention.md`](../STORY-AIBRIDGE-16-privacy-retention.md)  
**P1 scaffold:** 2026-09-13T17:43:00Z
**P3 Done:** 2026-09-13T17:49:14Z  
**Maps:** Scope #3 · Target #3 · operator decision (ops-only)

## Purpose

Provide an **ops-only** session-delete mechanism that is authenticated, authorized, fail-closed, and audit-logged; covers history, pending intents, and action tokens. Until HTTP path is decided, document fail-closed surface — **do not invent** channel OpenAPI delete fields.

## Code Facts (verified exists — P1)

1. Operator decision (story Meta): session-delete = ops-only; **HTTP path Unknown**.
2. Privacy runbook §2 / §5: operator session-delete must exist and be tested — `docs/runbooks/privacy-pilot.md`.
3. Channel OpenAPI SSOT has no delete path invent mandate: `docs/openapi/aibridge-channel-v1.openapi.yaml`.
4. Concrete CLI / internal admin route: **Unknown** at P1.

## AC/DoD

- [x] Ops delete surface exists **or** is explicitly fail-closed documented until path decision (Target #3).
- [x] When implemented: authenticated + authorized + audit-logged; covers history, pending intents, action tokens.
- [x] **No** new channel OpenAPI delete fields without operator decision.
- [x] Tests prove fail-closed for unauthorized callers (when surface exists).
- [x] `Skill declared: python-pro` present.

## Where to change

Ops CLI/script or internal admin module under `src/aibridge/` / `scripts/`; `docs/runbooks/privacy-pilot.md`; **not** inventing OAS paths.

## Verification commands

```bash
rg -n "session.delete|session_delete|ops.delete|privacy" doge-ai-bridge/docs/runbooks doge-ai-bridge/src doge-ai-bridge/scripts --glob '*.{py,md}' | head -40
rg -n "delete|/session" doge-ai-bridge/docs/openapi/aibridge-channel-v1.openapi.yaml | head -20
```

## Out of scope

Changing channel OpenAPI; inventing Bot/Telegram delete UX.
