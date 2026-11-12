# Task: docs — R3-P1-09 §6.1 executable checklist SSOT

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-15-n8n-telegram-gate.md`  
**Parent story:** [`STORY-AIBRIDGE-15-n8n-telegram-gate.md`](../STORY-AIBRIDGE-15-n8n-telegram-gate.md)  
**P1 scaffold:** 2026-09-13T17:28:28Z
**P3 Done:** 2026-09-13T17:34:04Z  
**Maps:** Scope #1–#9 · Target #1 · R3-P1-09

## Purpose

Publish an executable checklist that mirrors REQ-03 §6.1 verbatim so live n8n/Telegram proof has a single ops SSOT (not only wave-1 partial smoke).

## Code Facts (verified exists — P1)

1. `docs/ops/n8n-channel-workflow/README.md` — mapping, ack order, credential names, smoke §5.
2. `docs/ops/wave1-gate-checklist.md` — partial manual n8n proof; **not** full §6.1 matrix.
3. REQ-03 §6.1 bullet list is the AC source: `docs/requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md`.

## AC/DoD

- [x] Executable §6.1 checklist on disk (new or extended ops artifact) covers every Scope bullet from the parent story.
- [x] Checklist points at channel OpenAPI + n8n README; does not invent OpenAPI fields.
- [x] `Skill declared: python-pro` present.

## Where to change

`docs/ops/` (e.g. n8n-channel-workflow checklist / dedicated R3-P1-09 gate file), optionally cross-link from `wave1-gate-checklist.md` without replacing it.

## Verification commands

```bash
test -f doge-ai-bridge/docs/ops/n8n-channel-workflow/README.md
rg -n "answerCallbackQuery|event_id|story-drafts|channel Bearer" doge-ai-bridge/docs/ops --glob '*.md'
```
