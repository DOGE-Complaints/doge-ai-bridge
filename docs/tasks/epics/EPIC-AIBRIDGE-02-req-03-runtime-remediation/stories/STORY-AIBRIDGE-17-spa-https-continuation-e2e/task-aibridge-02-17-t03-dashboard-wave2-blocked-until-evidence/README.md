# Task: docs — dashboard wave-2 blocked until SPA evidence

**Status:** Done  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-17-spa-https-continuation-e2e.md`  
**Parent story:** [`STORY-AIBRIDGE-17-spa-https-continuation-e2e.md`](../STORY-AIBRIDGE-17-spa-https-continuation-e2e.md)  
**P1 scaffold:** 2026-09-13T18:20:16Z
**P3 Done:** 2026-09-13T18:23:58Z  
**Maps:** Target #2

## Purpose

Make `aibridge-mvp-dashboard` (and package INDEX as needed) treat **wave-2 residents** as blocked until R3-P1-08 evidence is linked — Target AC #2 — without claiming spa E2E PASS.

## Code Facts (verified exists — P1)

1. Dashboard SSOT: `docs/tasks/aibridge-mvp-dashboard.md` (§Now / Deferred / Remaining).
2. Package INDEX: `docs/tasks/backlog-stories/req-03-runtime-remediation/INDEX.md` lists story 17 Todo.
3. REQ-03 wave-2 residents require P1 gates including R3-P1-08.

## AC/DoD

- [x] Dashboard shows wave-2 / residents path blocked pending STORY-17 evidence (or equivalent clear gate language).
- [x] Link from dashboard to this pipeline story / R3-P1-08 checklist.
- [x] No false PASS for spa HTTPS E2E.
- [x] `Skill declared: test-master` present.

## Where to change

`docs/tasks/aibridge-mvp-dashboard.md`; optionally INDEX progress note (docs/tasks allowed for tracker sync in P3).

## Verification commands

```bash
rg -n "wave-2|residents|STORY-AIBRIDGE-17|R3-P1-08|blocked" doge-ai-bridge/docs/tasks/aibridge-mvp-dashboard.md
```
