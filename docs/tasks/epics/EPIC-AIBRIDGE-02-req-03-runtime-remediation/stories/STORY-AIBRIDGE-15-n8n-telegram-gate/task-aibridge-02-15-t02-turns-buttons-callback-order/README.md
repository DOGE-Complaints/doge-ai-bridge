# Task: docs/ops — turns path, inline buttons, callback order

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-15-n8n-telegram-gate.md`  
**Parent story:** [`STORY-AIBRIDGE-15-n8n-telegram-gate.md`](../STORY-AIBRIDGE-15-n8n-telegram-gate.md)  
**P1 scaffold:** 2026-09-13T17:28:28Z
**P3 Done:** 2026-09-13T17:34:04Z  
**Maps:** Scope #1–#3 · R3-P1-09

## Purpose

Lock the live routing shape: Telegram message → n8n → `/v1/channel/turns`; every `actions[]` as inline buttons with `callback_data` = token only; on callback — immediate `answerCallbackQuery` then `/v1/channel/actions` then Send/Edit Message.

## Code Facts (verified exists — P1)

1. Ops contract already states ack-before-actions order: `docs/ops/n8n-channel-workflow/README.md` §2.
2. Mapping cheat-sheet: `actions[].token` → inline `callback_data` (`README.md` §3).
3. Channel OpenAPI defines `actions[]` / turns / actions request shapes: `docs/openapi/aibridge-channel-v1.openapi.yaml`.

## AC/DoD

- [x] Checklist/runbook entries prove Scope #1–#3 (message→turns; buttons=token-only; answerCallbackQuery→actions→Send/Edit).
- [x] No invented channel fields (e.g. no `callback_ack_text`).
- [x] `Skill declared: python-pro` present.

## Where to change

`docs/ops/n8n-channel-workflow/README.md` and/or §6.1 checklist from t01; optional recorded fixtures under `tests/` only if they assert façade contract (not live Telegram).

## Verification commands

```bash
rg -n "answerCallbackQuery|callback_data|/v1/channel/turns|/v1/channel/actions" doge-ai-bridge/docs/ops/n8n-channel-workflow/README.md
```
