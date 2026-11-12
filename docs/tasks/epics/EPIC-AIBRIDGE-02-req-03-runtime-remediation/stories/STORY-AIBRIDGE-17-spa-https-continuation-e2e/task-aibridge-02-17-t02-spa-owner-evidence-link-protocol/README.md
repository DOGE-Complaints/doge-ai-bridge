# Task: docs — SPA owner evidence-link protocol (no spa invent)

**Status:** Done  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-17-spa-https-continuation-e2e.md`  
**Parent story:** [`STORY-AIBRIDGE-17-spa-https-continuation-e2e.md`](../STORY-AIBRIDGE-17-spa-https-continuation-e2e.md)  
**P1 scaffold:** 2026-09-13T18:20:16Z
**P3 Done:** 2026-09-13T18:23:58Z  
**Maps:** Scope #2 · Operator decision

## Purpose

Document how aibridge links spa-owned evidence (`STORY-SPA-*` Done / run-summary / checklist) when the spa package resolves — and keep SPA owner story key **Unknown** until a real spa path exists on disk. **Forbidden:** inventing spa product work or fabricating a spa story id.

## Code Facts (verified exists — P1)

1. Backlog Verified: SPA owner story key **Unknown** at materialize.
2. Operator decision (Meta): SPA profile owns UI/E2E execution and evidence artifact.
3. spa-app has backlog packages under `spa-app/docs/tasks/backlog-stories/` — no aibridge-owned `STORY-SPA-*` key selected in this story yet.
4. aibridge continuation URL is produced in `gateway.py`; SPA `#/story/submit` path is referenced as URL shape only.

## AC/DoD

- [x] Pipeline story / ops checklist records fill-in slots: spa story key, run-summary path, evidence checklist path.
- [x] Explicit rule: leave **Unknown** until operator/spa resolves; do not invent `STORY-SPA-*`.
- [x] Explicit **Вне scope**: no spa frontend implementation in `doge-ai-bridge`.
- [x] `Skill declared: test-master` present.

## Where to change

Pipeline story Verified section; R3-P1-08 ops checklist (t01 artifact); optional pointer in backlog story Meta (keep backlog file).

## Verification commands

```bash
rg -n "Unknown|STORY-SPA|spa owns|evidence" \
  doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/stories/STORY-AIBRIDGE-17-spa-https-continuation-e2e \
  doge-ai-bridge/docs/ops --glob '*.md'
```
