# Task: docs — observe n8n outbound Send/Edit + retry dedupe (CHAR-008)

**Status:** Done · 2026-09-18T14:06:43Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md`  
**Parent story:** [`STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md`](../STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md)  
**P1 scaffold:** 2026-09-18T14:03:38Z  
**Maps:** CHAR-008 · P1-Q3 · gaps §39 T01 · N8N-WF-001 pin

## Purpose

Observe pinned export (if present at `docs/ops/n8n-channel-workflow/exports/aibridge-telegram-channel-v1.json`) + ops README §2: map each response state → `send_message` \| `edit_message` and retry dedupe mechanism. If export absent — document **visible** defer (reuse STORY-36 pin pointer status); **no invent** export body.

**Out of this task:** write capture fixture body (t02); behavioral assert (t03); invent live TG / product n8n.

## AC/DoD

- [x] Observation note: per-state Send/Edit map **or** explicit defer linked to pin pointer.
- [x] No invent export JSON / Send-Edit policy without evidence.
- [x] `Skill declared: test-master` present.

## Where to change (execute — not P1)

- ops README §2 · pin pointer · optional export path — **P3**
