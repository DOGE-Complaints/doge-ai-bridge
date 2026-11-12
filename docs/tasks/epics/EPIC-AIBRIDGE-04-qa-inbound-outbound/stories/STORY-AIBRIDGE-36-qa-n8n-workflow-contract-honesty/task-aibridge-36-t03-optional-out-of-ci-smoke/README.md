# Task: docs — optional out-of-CI smoke for pinned export

**Status:** Done · 2026-09-18T12:32:14Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md`  
**Parent story:** [`STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md`](../STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md)  
**P1 scaffold:** 2026-09-18T12:27:40Z  
**Maps:** N8N-WF-001 · out-of-CI · gaps §36 T03

## Purpose

Bind/extend [`r3-p1-09-live-gate-checklist.md`](../../../../../ops/n8n-channel-workflow/r3-p1-09-live-gate-checklist.md) as out-of-CI smoke for the pinned export. **Not** added to default pytest / TEST-MANUAL default CI suite. No live Telegram invent; no Railway SUCCESS invent.

**Out of this task:** Layer E relabel (t01); pin pointer (t02); Gate-5 live pilot (STORY-37); product invent.

## AC/DoD

- [x] Checklist named/bound for pinned-export smoke outside default CI.
- [x] Explicit: not part of default pytest gate.
- [x] No live TG / Railway SUCCESS invent.
- [x] `Skill declared: test-master` present.

## Where to change

- `docs/ops/n8n-channel-workflow/r3-p1-09-live-gate-checklist.md` (and/or package meta pointer) — **P3**
