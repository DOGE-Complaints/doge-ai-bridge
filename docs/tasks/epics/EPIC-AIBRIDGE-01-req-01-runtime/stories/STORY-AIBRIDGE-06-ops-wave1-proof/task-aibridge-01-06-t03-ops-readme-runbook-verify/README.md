# Task: docs — operator README stubs + runbook disk verify

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-06-ops-wave1-proof.md`  
**P3 Done:** 2026-09-12T22:05:00Z
**Parent story:** [`STORY-AIBRIDGE-06-ops-wave1-proof.md`](../STORY-AIBRIDGE-06-ops-wave1-proof.md)

## Purpose

Operator README stubs (private net, n8n mapping, rotation) linking existing runbooks — do not duplicate secrets. Disk-verify Doc pointers paths (AC #4 / Scope #3–#4).

**Out of this task:** Inventing n8n workflow JSON body; secret values in docs.

## Code Facts (verified exists)

1. `docs/runbooks/{privacy-pilot,unknown-outcome-reconciliation,channel-bearer-rotation}.md`
2. `docs/ops/n8n-channel-workflow/README.md`
3. Arch ops — `04-ops-security.md`

## AC/DoD

- [x] Operator stubs exist and link runbooks (no secret duplication).
- [x] `ls`/test verifies Doc pointers paths exist.
- [x] `Skill declared: python-pro` present.

## Where to change

- `doge-ai-bridge/docs/` ops operator stubs (e.g. under `docs/ops/` or `docs/manuals/`).
- Optional path-existence unit/test or checklist in acceptance.

## Verification commands

```bash
ls doge-ai-bridge/docs/runbooks/privacy-pilot.md \
   doge-ai-bridge/docs/runbooks/unknown-outcome-reconciliation.md \
   doge-ai-bridge/docs/runbooks/channel-bearer-rotation.md \
   doge-ai-bridge/docs/ops/n8n-channel-workflow/README.md
```
