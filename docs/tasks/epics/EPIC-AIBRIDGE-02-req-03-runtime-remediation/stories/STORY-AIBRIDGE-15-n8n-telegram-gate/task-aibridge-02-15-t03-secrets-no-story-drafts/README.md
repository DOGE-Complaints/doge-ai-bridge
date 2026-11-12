# Task: docs/ops — n8n secrets boundary (no OpenAI/gateway /story-drafts)

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-15-n8n-telegram-gate.md`  
**Parent story:** [`STORY-AIBRIDGE-15-n8n-telegram-gate.md`](../STORY-AIBRIDGE-15-n8n-telegram-gate.md)  
**P1 scaffold:** 2026-09-13T17:28:28Z
**P3 Done:** 2026-09-13T17:34:04Z  
**Maps:** Scope #4 · R3-P1-09

## Purpose

Evidence that n8n holds only Telegram Bot token + channel Bearer; OpenAI and gateway Bearers are absent; no n8n node calls `/story-drafts`.

## Code Facts (verified exists — P1)

1. Credentials table (names only): `docs/ops/n8n-channel-workflow/README.md` §4 — Bot + channel Header Auth.
2. Hard rules: never gateway `/story-drafts`; never gateway URL/Bearer in workflow (`README.md` §2).
3. Вне scope of this story: mandatory credential-stripped JSON export (P2-04) — do not invent export body.

## AC/DoD

- [x] Checklist/evidence steps verify Bot + channel Bearer only; assert absence of OpenAI/gateway secrets in n8n.
- [x] Checklist asserts no `/story-drafts` node.
- [x] `Skill declared: python-pro` present.

## Where to change

`docs/ops/n8n-channel-workflow/README.md` / §6.1 checklist; evidence notes for live proof (no secrets in git).

## Verification commands

```bash
rg -n "story-drafts|OpenAI|gateway Bearer|CHANNEL_BEARER" doge-ai-bridge/docs/ops/n8n-channel-workflow/README.md
test ! -f doge-ai-bridge/docs/ops/n8n-channel-workflow/exports/aibridge-telegram-channel-v1.json
```
